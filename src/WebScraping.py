import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile, ZIP_DEFLATED
import os

class Scraper:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.site = None

    def fetch_page(self):
        response = self.session.get(self.url, timeout = 10)
        response.raise_for_status()
        self.site = BeautifulSoup(response.content, 'html.parser')

    def extract_links(self):
        if not self.site:
            raise ValueError("A pagina ainda não foi carregada. Execute fetch_page() primeiro.")
        
        paragrafo = self.site.find('div', class_ = 'cover-richtext-tile tile-content')
        if not paragrafo:
            raise ValueError("Não foi possivel encontrar a seção de links.")
        
        lista = paragrafo.find('ol')
        if not lista:
            raise ValueError("Não foi possivel encontrar a lista ordenada.")
        
        itens = lista.find_all('li')
        if len(itens) < 2:
            raise ValueError("Menos de dois itens encontrados na lista.")
        
        return [itens[i].find('a')['href'] for i in range(2) if itens[i].find('a')]

class FileDownloader:
    @staticmethod
    def download_file(url, filename):
        with requests.get(url, stream = True, timeout = 10) as response:
            response.raise_for_status()
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size = 8192):
                    file.write(chunk)

class ZipManager:
    def __init__(self, zip_filename):
        self.zip_filename = zip_filename

    def create_zip(self, files):
        with ZipFile(self.zip_filename, 'w', compression = ZIP_DEFLATED) as zip_file:
            for file in files:
                zip_file.write(file, os.path.basename(file))

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok = True)

    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    scraper = Scraper(url)

    try:
        scraper.fetch_page()
        links = scraper.extract_links()
        
        filenames = [os.path.join(data_dir, f"Anexo_{i+1}.pdf") for i in range(len(links))]

        # Baixa arquivos
        for link, filename in zip(links, filenames):
            FileDownloader.download_file(link, filename)

        # Compacta arquivos
        zip_manager = ZipManager(os.path.join(data_dir, "Anexos_Compactados.zip"))
        zip_manager.create_zip(filenames)

        print("Download e compactação concluidos com sucesso!\nVerifique na pasta \".\data\".")
    except Exception as e:
        print(f"Erro: {e}")
