import requests
import doctest
from bs4 import BeautifulSoup


class Products:
    """
    Класс для извлечения информации о продуктах с веб-страниц.

    >>> products = Products("https://parsinger.ru/html/index3_page_1.html", "https://parsinger.ru/html/")
    >>> products.start_page
    'https://parsinger.ru/html/index3_page_1.html'
    >>> products.schema
    'https://parsinger.ru/html/'
    """

    def __init__(self, start_page, schema):
        """
        Инициализация класса Products.

        :param start_page: URL начальной страницы
        :param schema: Схема URL
        """
        self.start_page = start_page
        self.schema = schema
        self.session = requests.Session()

    def get_response(self, url):
        """
        Получение HTTP-ответа по заданному URL.

        :param url: URL для запроса
        :return: Response объект
        :raises ConnectionError: Если ответ не 200
        >>> products = Products('https://parsinger.ru/html/index3_page_1.html', 'https://parsinger.ru/html/')
        >>> response = products.get_response("https://parsinger.ru/html/index3_page_1.html")
        >>> response.status_code
        200
        """
        response = self.session.get(url)
        response.encoding = "utf-8"

        if response.status_code != 200:
            raise requests.exceptions.ConnectionError(
                "Неправильно указан url сайта. Или проблемы с самим сайтом."
            )

        return response

    def get_soup(self, resp):
        """
        Получение объекта BeautifulSoup из ответа.

        :param resp: HTTP-ответ
        :return: BeautifulSoup объект
        >>> products = Products('https://parsinger.ru/html/index3_page_1.html', 'https://parsinger.ru/html/')
        >>> response = products.get_response('https://parsinger.ru/html/index3_page_1.html')
        >>> soup = products.get_soup(response)
        >>> soup != ''
        True
        """
        soup = BeautifulSoup(resp.text, "html.parser")
        assert soup, "Проблемы с парсингом кода страницы."

        return soup

    def get_pagens(self, url):
        """
        Получение всех страниц с товарами.

        :param url: URL для запроса
        :return: Список ссылок на страницы с товарами
        >>> products = Products('https://parsinger.ru/html/index3_page_1.html', 'https://parsinger.ru/html/')
        >>> products.get_pagens("https://parsinger.ru/html/index3_page_1.html")
        ['https://parsinger.ru/html/index3_page_1.html', 'https://parsinger.ru/html/index3_page_2.html','https://parsinger.ru/html/index3_page_3.html', 'https://parsinger.ru/html/index3_page_4.html']
        """
        response = self.get_response(url)
        soup = self.get_soup(response)

        tags_pagen = soup.select_one("div.pagen").select("a")
        assert len(tags_pagen) > 1, "Вероятные проблемы с .select()"
        links_pagen = [f"{self.schema}{a_tag['href']}" for a_tag in tags_pagen]

        return links_pagen

    def get_name_products(self):
        """
        Получение имен всех продуктов.

        :return: Список имен продуктов
        >>> products = Products('https://parsinger.ru/html/index3_page_1.html', 'https://parsinger.ru/html/')
        >>> products.get_name_products()
        [['Vampire RGB,9 кнопок', 'Defender Halo Z GM-430L', 'Defender Shark 2', 'Defender sTarx GM-390L', 'Defender Skull GM-180L', 'Defender Killer GM-170L', 'Defender Ghost GM-190L', 'Defender Witcher GM-990'], ['Logitech G305 LIGHTSPEED Wireless', 'Logitech G102 LIGHTSYNC Gaming', 'Logitech G PRO HERO Black', 'Logitech G402 Hyperion Fury', 'STM 109CW', 'Defender MB-986', 'Gembird MG-520', 'CBR CM 846'], ['Гарнизон GM-720G', 'Гарнизон GM-700G', 'Гарнизон GM-760G', 'Гарнизон GM-730G', 'Гарнизон GM-620G', 'A4TECH Bloody Q51', 'MGK-03U Dialog Gan-Kata', 'Defender Flash MB-600L'], ['Gembird MG-550', 'Lenovo Legion M200', 'Sven RX-G750', 'Wired Gaming Mouse', 'MSI Clutch GM08', 'Gembird MG-760', 'MGK-11U Dialog Gan-Kata', 'Logitech G102']]
        """
        names = []
        for link in self.get_pagens(self.start_page):
            response = self.get_response(link)
            soup = self.get_soup(response)

            all_titles_on_page = [
                a_tag.text.strip() for a_tag in soup.select("a.name_item")
            ]
            names.append(all_titles_on_page)

        return names

if __name__ == "__main__":
    doctest.testmod()