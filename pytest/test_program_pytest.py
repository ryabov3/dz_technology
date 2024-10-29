import pytest
import requests
from program import Products


class TestProgram:
    def test_raises(self):
        url = "https://parsinger.ru/html/index3_page_1.html"
        schema = "https://parsinger.ru/html/"
        product = Products(url, schema)

        with pytest.raises(
            requests.exceptions.ConnectionError,
            match="Неправильно указан url сайта. Или проблемы с самим сайтом.",
        ):
            product.get_response(url)

    def test_program(self):
        url = "https://parsinger.ru/html/index3_page_1.html"
        schema = "https://parsinger.ru/html/"
        product = Products(url, schema)
        print(product.get_name_products())
