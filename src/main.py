import os
from scraper import Scraper, HTMLParser
from downloader import FileDownloader
from file_manager import FileManager
from zip_manager import ZipManager
from extractor import PDFExtractor
from processor import DataProcessor

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
        
        #Fiquei na duvida em salvar os nomes de forma original, ou como Anexo 1 ou Anexo 2 por isso deixei as duas opções, basta alternar o comentario entre as linhas abaixo.
        #filenames = [os.path.join(data_dir, os.path.basename(link)) for link in links]
        filenames = [os.path.join(data_dir, f"Anexo_{i+1}.pdf") for i in range(len(links))]

        # Baixa os arquivos
        for link, filename in zip(links, filenames):
            FileDownloader.download_file(link, filename)

        # Processa apenas o primeiro anexo
        pdf_path = filenames[0]
        csv_filename = os.path.join(data_dir, "Rol_de_Procedimentos.csv")
        zip_filename = os.path.join(data_dir, "Teste_David_Marcelo_Gois.zip")
        
        # Extrai os dados do Anexo I
        extractor = PDFExtractor(pdf_path)
        extractor.extract_tables()
        df = extractor.get_dataframe()
        
        # Faz as modificações pedidas
        processor = DataProcessor(df)
        processor.clean_data()
        processor.save_to_csv(csv_filename)
        
        # Comprime o CSV
        ZipManager.compress_and_cleanup(zip_filename, csv_filename)

        # Compacta todos os arquivos baixados
        zip_path = os.path.join(data_dir, "Anexos_Compactados.zip")
        ZipManager.create_zip(zip_path, filenames)
        for file in filenames:
            os.remove(file)

        print("Download e processamento concluídos com sucesso! Verifique a pasta 'data'.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
