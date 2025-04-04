import os
from zipfile import ZipFile, ZIP_DEFLATED

class ZipManager:
    @staticmethod
    def create_zip(zip_filename, files):
        """Compacta arquivo"""
        with ZipFile(zip_filename, 'w', compression=ZIP_DEFLATED) as zip_file:
            for file in files:
                if os.path.exists(file):
                    zip_file.write(file, os.path.basename(file))
    
    @staticmethod
    def compress_and_cleanup(zip_filename, file_to_compress):
        """Compacta um unico arquivo e o apaga depois da compactação."""
        ZipManager.create_zip(zip_filename, [file_to_compress])
        os.remove(file_to_compress)