import os

class FileManager:
    @staticmethod
    def create_directory(path):
        """Cria diretorio"""
        os.makedirs(path, exist_ok = True)

    @staticmethod
    def delete_file(filepath):
        """Deleta arquivo"""
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def list_files(directory):
        """Lista os arquivos do diretorio"""
        if os.path.exists(directory) and os.path.isdir(directory):
            return os.listdir(directory)
        return []

    @staticmethod
    def file_exists(filepath):
        """ Verifica se existe arquivo"""
        return os.path.exists(filepath)
