class DataProcessor:
    def __init__(self, df):
        self.df = df
    
    def clean_data(self):
        """Faz a troca  de abreviação."""
        # Remove colunas vazias
        self.df.dropna(axis=1, how='all', inplace=True)  
        
        substitutions = {
            "OD": "Procedimentos Odontológicos",
            "AMB": "Procedimentos Ambulatoriais"
        }
        self.df.replace(substitutions, inplace=True)
    
    def save_to_csv(self, filename):
        """Salva os dados no CSV."""
        self.df.to_csv(filename, index=False, sep=";")
        return filename