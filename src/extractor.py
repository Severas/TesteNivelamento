import pdfplumber
import pandas as pd

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.data = []
    
    def extract_tables(self):
        """Extrai as tabelas do PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if any(row):  # Verifica se a linha não está vazia
                            self.data.append(row)
    
    def get_dataframe(self):
        """Retorna os dados"""
        return pd.DataFrame(self.data)
