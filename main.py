import requests
from bs4 import BeautifulSoup
import os
import csv

class FileDownloader:
    def __init__(self, link, download_dir, csv_file):
        self.link = link
        self.download_dir = download_dir
        self.csv_file = csv_file
        self.response = requests.get(self.link).text
        self.soup = BeautifulSoup(self.response, 'lxml')
        self.all_block = self.soup.find('div', id='ik83r5m00_0')

    def create_download_dir(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_files(self):
        self.create_download_dir()
        with open(self.csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Filename", "FilePath", "Description"])
            for block in self.all_block.find_all('a'):
                url = block.get('href')
                filename = url.split('/')[-1]
                filepath = os.path.join(self.download_dir, filename)
                response2 = requests.get(f'https://kotelnich-omv.ru/{url}')
                with open(filepath, 'wb') as f:
                    f.write(response2.content)
            # Get the text of the parent element (should be a <li> or similar)
                parent_element = block.parent
                description = parent_element.get_text(strip=True)  # Extract text from parent element
                writer.writerow([filename, filepath, description])
                print(f"Файл {filename} сохранен в {self.download_dir}")

if __name__ == "__main__":
    downloader = FileDownloader("https://kotelnich-omv.ru/post-adm-2023", "downloads", "files.csv")
    downloader.download_files()