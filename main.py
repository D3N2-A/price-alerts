from bs4 import BeautifulSoup
import requests


def main():
    url = "https://www.nike.com/in/t/air-jordan-1-low-shoes-lFCSjp/553558-169"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.find("div", {"id": "price-container"}))


if __name__ == "__main__":
    main()
