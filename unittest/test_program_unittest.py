import unittest
import requests
from program import Products


class TestProducts(unittest.TestCase):
    def setUp(self):
        url = "https://parsinger.ru/html/index3_page_1.html"
        schema = "https://parsinger.ru/html/"
        self.product = Products(url, schema)

    def test_response(self):
        url = "https://parsinger.ru/html/index3_page_1.html"
        with self.assertRaises(requests.exceptions.ConnectionError) as context:
            self.product.get_response(url)
            self.assertEqual(
                str(context.exception),
                "Неправильно указан url сайта. Или проблемы с самим сайтом.",
            )

    def test_soup(self):
        url = "https://parsinger.ru/html/index3_page_1.html"
        response = self.product.get_response(url)
        soup = self.product.get_soup(response)

        self.assertNotEqual(soup, "")

    def test_pagen_list(self):
        pagens = self.product.get_pagens("https://parsinger.ru/html/index3_page_1.html")

        self.assertNotEqual(pagens, [])

if __name__ == "__main__":
    unittest.main()