import os
from scraper import Scraper, HTMLParser
from downloader import FileDownloader
from file_manager import FileManager
from zip_manager import ZipManager

def main():
    # Diretorios
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    FileManager.create_directory(data_dir)

    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    
    try:
        # Faz o get
        scraper = Scraper(url)
        html_content = scraper.fetch_html()

        # Busca os links dos anexos
        parser = HTMLParser(html_content)
        links = parser.extract_links()
        
        filenames = [os.path.join(data_dir, f"Anexo_{i+1}.pdf") for i in range(len(links))]

        # Baixa os arquivos
        for link, filename in zip(links, filenames):
            FileDownloader.download_file(link, filename)

        # Compacta os arquivos baixados
        zip_path = os.path.join(data_dir, "Anexos_Compactados.zip")
        ZipManager.create_zip(zip_path, filenames)

        print("Download e compactação concluidos com sucesso!\nVerifique na pasta \"data\".")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
