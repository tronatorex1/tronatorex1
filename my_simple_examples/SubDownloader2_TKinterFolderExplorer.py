# -*- coding: utf-8 -*- 
import re
import os
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import *

# Variables
url_base = "https://www.podnapisi.net/"
movie_name = movie_path = movie_year = folder_selected = url = ""

# Visual Input
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
movie_path = folder_selected

# Manual Input = uses only the movie_path variable via keyboard
#movie_path = input(" · Enter the whole movie path: ").replace('"','')

# Housekeeping o variables
movie_name = movie_path.split('/')[-1].split('(')[0].strip()
movie_year = movie_path[movie_path.index('('):].replace('(','').replace(')','')

# Collected variables
print(f"SubDownloader v1 [ using: {url_base} ]")
print("  Collected variables: " + f"{movie_path} | Year={movie_year} | Lang=EN (default)")

def download_podnapisi_subtitle(movie_name):
    url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en&year={movie_year}&movie_type=movie&sort=ratings.combined&order=asc" # selects subtitle based on ratings (best first)
    #url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en" # intentar filtrar más, por rating o downloads
    #url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en&stat.downloads&order=desc"
    #url = f"{url_base}subtitles/search/?keywords={movie_name}&language=en&year=2021&movie_type=movie"
    print(f"  - Searching : {url}", end=" ")
    response = requests.get(url)

    if response.status_code == 200:
        print("= something found!")

        # Parsing the weird HTML file into something readeable
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the portion of the HTML that might contain the links to subtitles
        download_link = soup.contents[2]
        
        # Detects where the First subtitle link appears in the HTML 
        idx1 = re.search(r'a alt="Download subtitles." data-toggle="tooltip" href=', str(download_link)).end() # index del primer link que aparece en los res
        download_link = url_base + str(download_link)[idx1 + 2:str(download_link).index(r'" rel="nofollow"',1)] # buscar y picar el string de descarga
        
        # Having the hard URL of the subtitle (above), downloads its contents (zip file)
        print("  - Downloading the first pseudo-matching source... (highest download rated link)")
        subtitle_response = requests.get(download_link)
        
        # Creates in the path a zip file (bin) with the subtitles within
        with open(movie_path + "/" + movie_name + ".zip", "wb") as subtitle_file: # originally all subtitles must be downloaded as zip files
            subtitle_file.write(subtitle_response.content)
        
        # Extracts the subtitle file from the zip file 
        with ZipFile(movie_path + "/" + movie_name + ".zip", "r") as subtitle_file_to_unzip: # here use the actual zip's whole path
            subtitle_file_to_unzip.extractall(movie_path) # here use the path in which to unzip the srt file
        
        # Renames the recently downloaded subtitle with the local movie's name
        srt1 = [i for i in os.listdir(path = movie_path) if '.srt' in i][0] # list and pick only the file ending with '.srt'
        ren2 = [i for i in os.listdir(path = movie_path) if '.m' in i][0] # list and pick only the file ending with ".m" (eg.: .mp4, .mpeg, etc.)
        ren3 = ren2.split(".m")[0] + ".srt"
        os.rename(movie_path + "/" + srt1, movie_path + "/" + ren3)

        print("  - Download finished...")

download_podnapisi_subtitle(movie_name)