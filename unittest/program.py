import requests
from bs4 import BeautifulSoup


class Products:
    def __init__(self, start_page, schema):
        self.start_page = start_page
        self.schema = schema
        self.session = requests.Session()

    def get_response(self, url):
        response = self.session.get(url)
        response.encoding = "utf-8"

        if response.status_code != 200:
            raise requests.exceptions.ConnectionError(
                "Неправильно указан url сайта. Или проблемы с самим сайтом."
            )

        return response

    def get_soup(self, resp):
        soup = BeautifulSoup(resp.text, "html.parser")

        return soup

    def get_pagens(self, url):
        response = self.get_response(url)
        soup = self.get_soup(response)

        tags_pagen = soup.select_one("div.pagen").select("a")
        links_pagen = [f"{self.schema}{a_tag['href']}" for a_tag in tags_pagen]

        return links_pagen

    def get_name_products(self):
        names = []
        for link in self.get_pagens(self.start_page):
            response = self.get_response(link)
            soup = self.get_soup(response)

            all_titles_on_page = [
                a_tag.text.strip() for a_tag in soup.select("a.name_item")
            ]
            names.append(all_titles_on_page)

        return names


url = "https://parsinger.ru/html/index3_page_1.html"
schema = "https://parsinger.ru/html/"
product = Products(url, schema)
print(product.get_name_products())
