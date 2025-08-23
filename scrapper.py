from abc import ABC, abstractmethod
from datetime import datetime, timezone
from curl_cffi import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

from models import PriceHistory, Product
from constants import currency_map


def parse_price(price_str: str) -> float:
    cleaned = price_str.replace("Price", "").replace("₹", "").replace(" ", "")
    return float(cleaned)


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
        if price is not None:
            price_text = price.text.strip()
            for currency, symbols in currency_map.items():
                if any(symbol in price_text for symbol in symbols):
                    return currency
        else:
            return "INR"

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


def scrape_product(url: str) -> PriceHistory:
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

    scrapper_map = {
        "nike": NikeScrapper(),
        "adidas": AdidasScrapper(),
    }

    website_key = url.split("/")[2].split(".")[1]

    if website_key.lower() not in scrapper_map:
        print(f"Scrapper not found for {website_key} for url {url}")
        return None

    scrapper = scrapper_map[website_key.lower()]
    title = scrapper.extract_title(soup)
    price = scrapper.extract_price(soup)
    availability = scrapper.extract_availability(soup)
    image_url = scrapper.extract_image_url(soup)
    currency = scrapper.extract_currency(soup)
    additional_data = scrapper.additional_data(soup)

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


async def scrape_products(products: list[dict]):
    print(f"Scraping {len(products)} products")
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_results = {
            product["url"]: executor.submit(scrape_product, product["url"])
            for product in products
        }

        for url, future in future_results.items():
            try:
                result = future.result()
                print(f"Scraped {url}")
                if result is not None:
                    print(result.__dict__)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
