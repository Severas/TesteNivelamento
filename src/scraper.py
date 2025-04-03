import requests
from bs4 import BeautifulSoup

class Scraper:
    """Classe para buscar dados"""
    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        """Faz o get"""
        response = requests.get(self.url, timeout = 10)
        # Lança um erro se a req falhar
        response.raise_for_status()
        return response.content

class HTMLParser:
    """Classe para extrair os dados"""
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_links(self):
        """Extrai os links dos anexos"""
        paragrafo = self.soup.find('div', class_ = 'cover-richtext-tile tile-content')
        if not paragrafo:
            raise ValueError("Não foi possivel encontrar a seção de links.")
        
        lista = paragrafo.find('ol')
        if not lista:
            raise ValueError("Não foi possivel encontrar a lista ordenada.")
        
        itens = lista.find_all('li')
        if len(itens) < 2:
            raise ValueError("Menos de dois itens encontrados na lista.")
        
        return [itens[i].find('a')['href'] for i in range(2) if itens[i].find('a')]
