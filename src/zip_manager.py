import os
from zipfile import ZipFile, ZIP_DEFLATED

class ZipManager:
    @staticmethod
    def create_zip(zip_filename, files):
        """Cria um arquivo ZIP contendo os anexos."""
        with ZipFile(zip_filename, 'w', compression=ZIP_DEFLATED) as zip_file:
            for file in files:
                # Garante que exista aquivo antes de adicionar
                if os.path.exists(file):
                    zip_file.write(file, os.path.basename(file))
