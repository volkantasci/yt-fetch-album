import multiprocessing
import os
import subprocess
from shutil import which
from sys import argv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

HOME = "/home/ubuntu/services/navidrome.volkantasci.com"
MUSIC_FOLDER_PATH = os.path.join(HOME, "downloaded-music")
TEMP_FOLDER_PATH = os.path.join(HOME,  "temp")

music_file_extensions = ['.opus', '.oog,', '.webm', '.mp3', '.wav', '.flac', '.m4a', '.aac', '.wma', '.ogg']


def cover_file(file, current_album, current_artist):
    os.chdir(TEMP_FOLDER_PATH)
    dot_index = file.rindex('.')
    extension = file[dot_index:]
    title = file

    if '[' in file:
        bracket_index = file.index('[')
        title = file[:bracket_index]

    if extension in music_file_extensions:
        print("Process started for:", title)
        merged_name = os.sep.join([MUSIC_FOLDER_PATH, current_artist, current_album, title]).strip() + extension
        temp_name = os.sep.join([TEMP_FOLDER_PATH, file])
        cover_path = os.sep.join([TEMP_FOLDER_PATH, 'cover.jpg'])
        add_art_command = f'opusdec --force-wav "{temp_name}" - | opusenc --artist "{current_artist}" --album "{current_album}" --title "{title}" --picture {cover_path} - "{merged_name}"'
        print("Command: ", add_art_command)
        os.system(add_art_command)
        print("Process finished for: ", title)


def add_covers(current_album, current_artist):
    os.chdir(TEMP_FOLDER_PATH)
    os.makedirs('covering')
    os.system('rm -rf covering/*')
    music_files = [i for i in os.listdir('.') if '.' in i]

    processes = []
    for f in music_files:
        p = multiprocessing.Process(target=cover_file, args=(f, current_album, current_artist))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()


class Cloner:
    def __init__(self, url_list: list, driver: webdriver.Firefox):
        self.driver = driver
        self.url_list = url_list
        self.current_url = ""
        self.current_album = ""
        self.current_artist = ""

    def get_parser_from_url(self, url):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source.encode('utf-8'), features="html.parser")
        self.current_album = soup.find('yt-formatted-string', class_='title').text
        print("Current album: ", self.current_album)
        all_a_tags = soup.find_all('a')
        for a in all_a_tags:
            try:
                if 'channel' in a['href']:
                    self.current_artist = a.text
                    print("Current artist: ", self.current_artist)
            except KeyError:
                pass

        return soup

    def create_folders(self):
        if os.path.isdir(MUSIC_FOLDER_PATH):
            structure = os.sep.join([MUSIC_FOLDER_PATH, self.current_artist, self.current_album])
            os.makedirs(structure, exist_ok=True)
            os.makedirs(TEMP_FOLDER_PATH, exist_ok=True)
            os.system(f'rm -rf "{TEMP_FOLDER_PATH}/*"')

            return 0, "Successfully created"
        else:
            return 1, "Music folder is not valid"

    def fetch_all_songs(self):
        os.chdir(TEMP_FOLDER_PATH)
        os.system("rm -rf *")
        print("Songs are fetching from this url:")
        print(f"Adres: {self.current_url}")
        subprocess.run(['yt-dlp', '-x', self.current_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Songs are fetched successfully!")

    def fetch_cover(self):
        os.chdir(TEMP_FOLDER_PATH)
        soup = BeautifulSoup(self.driver.page_source.encode('utf-8'))
        img = soup.find('img', id='img')
        command = f'wget {img["src"]} -O cover.jpg'
        os.system(command)

    def run_url_list(self):
        for url in self.url_list:
            if not url:
                continue
            self.current_url = url
            self.get_parser_from_url(self.current_url)
            self.create_folders()
            self.fetch_all_songs()
            self.fetch_cover()
            add_covers(self.current_album, self.current_artist)

        self.driver.close()


def valid_args():
    return [line if '\n' not in line else line[:-1] for line in open(argv[1]).readlines()] if len(argv) == 2 else print(
        "Missing URL File") or exit(1)


def check_requirements():
    return True not in [which(i) is None for i in ['yt-dlp', 'opusenc', 'opusdec']]


def main():
    print("Welcome to Youtube Music Cloner!")
    if not check_requirements():
        print("Install all requirements programs in Readme.md file!")
        return 9  # Error Code

    options = Options()
    options.headless = True
    options.binary_location = 'geckodriver'
    driver = webdriver.Firefox(options=options)

    my_list = valid_args()

    cloner = Cloner(my_list, driver)
    cloner.run_url_list()


if __name__ == "__main__":
    main()