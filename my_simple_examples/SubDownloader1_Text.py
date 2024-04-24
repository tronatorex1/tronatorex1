# -*- coding: utf-8 -*- 
import re
import os
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

# Variables
url_base = "https://www.podnapisi.net/"
#movie_name = "Inception"  # Provide the movie name for which you want to download subtitles
#movie_path = "c:\\tmp\\"

# Input
movie_path = input(" · Enter the whole movie path: ").replace('"','')
#movie_name = input(" · Enter movie name: ")
#movie_year = input(" · Enter movie year: ")

# Housekeeping o variables
try:
    movie_name = (movie_path.split("\\")[-1]).split('(')[0].strip()
    movie_year = (movie_path.split("\\")[-1]).split('(')[1].replace(')','')
except Exception as e:
    print(f"[X] Exception: {e} : @ # Housekeeping o variables")
    movie_name = (movie_path.split("\\")[-1]) # no parenthesis found for movie's year
    movie_year = "" # no year found

# Possible title correction
q = input(" + Do you need to simplify the title's name and year? [y/n]")
if q == 'y':
    movie_name = input(" · Enter movie name: ")
    movie_year = input(" · Enter movie year: ")

# Collected variables
print(f"SubDownloader v1 [ using: {url_base} ]")
print("\n  Collected variables: " + f"{movie_path}\{movie_name} | Year={movie_year} | Lang=EN (default)" + "\n")

def download_podnapisi_subtitle(movie_name):
    url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en&year={movie_year}&movie_type=movie&sort=ratings.combined&order=asc" # selects subtitle based on ratings (best first)
    #url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en" # intentar filtrar más, por rating o downloads
    #url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en&stat.downloads&order=desc"
    #url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en&year=2021&movie_type=movie"
    print(f"  - Searching : {url}", end=" ")
    response = requests.get(url)

    if response.status_code == 200:
        print("= something found!")
        soup = BeautifulSoup(response.text, 'html.parser')
        #open("c:\\tmp\\xxx.html","w").write(str(soup.contents)) # aquí el contenido de la página que lista los subs posibles
        #subtitle_link = soup.select_one('subtitle-entry') # parece que no sirve porque no consigue el sub-entry
        #soup.find_all('subtitle-entry') # parece que no sirve porque no consigue el sub-entry
        download_link = soup.contents[2]
        #download_link.find_next(r'a alt="Download subtitles." data-toggle="tooltip" href=') # este debe ser el primer link que aparece en los res
        idx1 = re.search(r'a alt="Download subtitles." data-toggle="tooltip" href=', str(download_link)).end() # index del primer link que aparece en los res
        download_link = url_base + str(download_link)[idx1 + 2:str(download_link).index(r'" rel="nofollow"',1)] # buscar y picar el string de descarga
        """
        aquí concat url base + res3 y test aquello de download file
        """
        print("  - Downloading the first pseudo-matching source... (highest download rated link)")
        subtitle_response = requests.get(download_link)
        with open(movie_path + "\\" + movie_name + ".zip", "wb") as subtitle_file: # originally all subtitles must be downloaded as zip files
            subtitle_file.write(subtitle_response.content)
        
        with ZipFile(movie_path + "\\" + movie_name + ".zip", "r") as subtitle_file_to_unzip: # here use the actual zip's whole path
            subtitle_file_to_unzip.extractall(movie_path) # here use the path in which to unzip the srt file
        
        srt1 = [i for i in os.listdir(path = movie_path) if '.srt' in i][0]
        ren2 = [i for i in os.listdir(path = movie_path) if '.m' in i][0] # list and pick only the file ending with ".m" (eg.: .mp4, .mpeg, etc.)
        ren3 = ren2.split(".m")[0] + ".srt"
        os.rename(movie_path + "\\" + srt1, movie_path + "\\" + ren3)
        print("  - Download finished...")

download_podnapisi_subtitle(movie_name)