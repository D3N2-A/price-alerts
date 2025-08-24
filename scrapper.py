import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from browser_use import Agent, ChatGoogle
from curl_cffi import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import db
from models import PriceHistory, Product, AIScrapperResult
from constants import currency_map, ai_scrapper_task


def parse_price(price_str: str) -> float:
    replace_str = ["Price", " ", ","]
    for _, symbols in currency_map.items():
        replace_str.extend(symbols)
    for replace_str in replace_str:
        price_str = price_str.replace(replace_str, "")
    return float(price_str)


def parse_currency(price_str: str) -> str:
    for currency, symbols in currency_map.items():
        if any(symbol in price_str for symbol in symbols):
            return currency
    return "INR"


def parse_additional_data(additional_data: dict) -> dict:
    if additional_data is None:
        return {}
    return {k: v for k, v in additional_data.items() if v is not None}


class BaseScraper(ABC):
    @abstractmethod
    def extract_title(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extract_price(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extract_availability(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extract_image_url(self, soup: BeautifulSoup) -> str:
        pass


class NikeScrapper(BaseScraper):
    def extract_title(self, soup: BeautifulSoup) -> str:
        title = soup.find("h1", {"data-testid": "product_title"})
        if title is not None:
            return title.text.strip()
        else:
            raise Exception("Title not found")

    def extract_price(self, soup: BeautifulSoup) -> float:
        price = soup.find("span", {"data-testid": "currentPrice-container"})
        if price is not None:
            price_text = price.text.strip()
            return parse_price(price_text)
        else:
            raise Exception("Price not found")

    def extract_availability(self, soup: BeautifulSoup) -> bool:
        return soup.find("span", {"data-testid": "sold-out-container"}) is None

    def extract_currency(self, soup: BeautifulSoup) -> str:
        price = soup.find("span", {"data-testid": "currentPrice-container"})
        if price is None:
            return "INR"
        price_text = price.text.strip()
        return parse_currency(price_text)

    def extract_image_url(self, soup: BeautifulSoup) -> str:
        image = soup.find("img", {"data-testid": "HeroImg"})
        if image is not None:
            return image.get("src")
        else:
            raise Exception("Image not found")

    def additional_data(self, soup: BeautifulSoup) -> dict:
        additional_data = {}
        offer = soup.find("span", {"data-testid": "OfferPercentage"})
        sold_out_text = soup.find("div", {"data-testid": "sold-out-container"})
        additional_data["offer"] = offer.text.strip() if offer is not None else ""
        additional_data["sold_out_text"] = (
            sold_out_text.text.strip() if sold_out_text is not None else ""
        )

        return additional_data


class AdidasScrapper(BaseScraper):
    def extract_title(self, soup: BeautifulSoup) -> str:
        title = soup.find("h1", {"data-testid": "product-title"})
        if title is not None:
            return title.text.strip()
        else:
            raise Exception("Title not found")

    def extract_price(self, soup: BeautifulSoup) -> float:
        price = soup.find("div", {"data-testid": "main-price"})
        if price is not None:
            price_text = price.text.strip()
            return parse_price(price_text)
        else:
            raise Exception("Price not found")

    def extract_availability(self, soup: BeautifulSoup) -> bool:
        return soup.find("section", {"data-testid": "sold-out-signup"}) is None

    def extract_currency(self, soup: BeautifulSoup) -> str:
        price = soup.find("div", {"data-testid": "main-price"})
        if price is not None:
            price_text = price.text.strip()
            for currency, symbols in currency_map.items():
                if any(symbol in price_text for symbol in symbols):
                    return currency
        return "INR"

    def extract_image_url(self, soup: BeautifulSoup) -> str:
        image_galary = soup.find("div", {"id": "navigation-target-gallery"})
        if image_galary is not None:
            return image_galary.find("img").get("src")
        else:
            raise Exception("Image not found")

    def additional_data(self, soup: BeautifulSoup) -> dict:
        additional_data = {}

        return additional_data


class AiScrapper:
    def __init__(self, url: str, output_model: AIScrapperResult):
        self.url = url
        # controller = Controller(output_model=output_model)
        self.agent = Agent(
            task=ai_scrapper_task.format(url=url),
            llm=ChatGoogle(model="gemini-2.5-flash"),
            output_model=output_model,
            llm_timeout=15,
        )

    async def run(self):
        try:
            result = await self.agent.run()
            await self.agent.close()
            return result
        except Exception as e:
            print(f"Error in AI scraper: {str(e)}")
            await self.agent.close()
            return None


async def scrape_product(url: str) -> PriceHistory:

    scrapper_map = {
        "nike": NikeScrapper(),
        "adidas": AdidasScrapper(),
    }

    website_key = url.split("/")[2].split(".")[1]

    if website_key.lower() in scrapper_map:
        try:
            response = requests.get(
                url,
                timeout=5000,
                impersonate="chrome",
            )

            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error details: {str(e)}")
            raise

        scrapper = scrapper_map[website_key.lower()]
        title = scrapper.extract_title(soup)
        price = scrapper.extract_price(soup)
        availability = scrapper.extract_availability(soup)
        image_url = scrapper.extract_image_url(soup)
        currency = scrapper.extract_currency(soup)
        additional_data = scrapper.additional_data(soup)
    else:
        print(
            f"\nScrapper not found for {website_key.lower()} defaulting to AI scraper\n"
        )
        ai_scrapper = AiScrapper(url, AIScrapperResult)
        result = (await ai_scrapper.run()).final_result()

        if result is None:
            raise Exception("Failed to scrape product using AI scraper")

        try:
            parsed_result = AIScrapperResult.model_validate_json(result)
        except Exception as e:
            print(f"JSON validation error. Raw result: {result}")
            raise

        # Initialize variables from AI scraper result
        title = parsed_result.title
        price = parse_price(parsed_result.price)
        currency = parse_currency(parsed_result.price)
        image_url = parsed_result.image_url
        availability = parsed_result.availability
        additional_data = parse_additional_data(parsed_result.additional_data) or {}

    return PriceHistory(
        name=title,
        price=price,
        currency=currency,
        main_image_url=image_url,
        timestamp=datetime.now(timezone.utc),
        product_url=url,
        availability=availability,
        product=Product(url=url),
        additional_data=additional_data,
    )


async def scrape_products(products: list[dict], db: db.Database):
    print(f"Scraping {len(products)} products")
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_results = {
            product["url"]: executor.submit(asyncio.run, scrape_product(product["url"]))
            for product in products
        }

        for url, future in future_results.items():
            try:
                result = future.result()
                if result is not None:
                    try:
                        db.store_price_history(result)
                        print(f"Successfully scraped {url}")
                    except Exception as db_error:
                        print(f"Error storing price history for {url}: {db_error}")
                else:
                    print(f"No results returned for {url}")
            except Exception as e:
                print(f"Error scraping {url}: {e}")
