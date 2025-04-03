import requests

class FileDownloader:
    @staticmethod
    def download_file(url, filename):
        with requests.get(url, stream = True, timeout = 10) as response:
            response.raise_for_status()
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size = 8192):
                    file.write(chunk)
