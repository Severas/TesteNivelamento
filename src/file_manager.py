import os

class FileManager:
    @staticmethod
    def create_directory(path):
        os.makedirs(path, exist_ok = True)

    @staticmethod
    def delete_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def list_files(directory):
        if os.path.exists(directory) and os.path.isdir(directory):
            return os.listdir(directory)
        return []

    @staticmethod
    def file_exists(filepath):
        return os.path.exists(filepath)
