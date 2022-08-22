# webscrapping movies from https://m.arabseed.sbs
# github: @sherif-abdallah
# email: sherif.abdulla@outlook.com
# repositry: https://github.com/sherif-abdallah/arabseed-movies-scraper
# date: 2022-8-20
# version: 1.0
# license: GPLv3
# python: 3.8.0

import requests
from bs4 import BeautifulSoup
import pandas as pd
import webbrowser

domain = "https://m.arabseed.sbs"


inp = input("Enter movie name or url: ")
if inp.startswith("http://") or inp.startswith("https://"):
    url = inp

else:
    # Show Search Results
    results_linl = domain + "/find/?find=" + inp
    results_page = requests.get(results_linl)
    results_soup = BeautifulSoup(results_page.content, "html.parser")
    results_list = results_soup.find_all("div", class_="MovieBlock")
    if len(results_list) == 0:
        print("No results found")
        exit()
    else:
        result_list = []
        print("Found {} results".format(len(results_list)))
        for i in range(len(results_list)):
            movie_link = results_list[i].find("a")["href"]
            movie_title = str(results_list[i].find("h4").text).replace("فيلم", "").replace("مسلسل", "").replace("مترجم", "").strip()
            print("{}. {}".format(i + 1, movie_title))
            result_list.append(movie_link)
        

        # Select Movie
        inp = input("Enter number: ")
        if inp.isdigit():
            inp = int(inp)
            if inp > len(result_list) or inp < 1:
                print("Invalid number")
                exit()
            else:
                url = result_list[inp - 1]
        else:
            print("Invalid number")
            exit()

# Get Movie Details
movie_page = requests.get(url)
movie_soup = BeautifulSoup(movie_page.content, "html.parser")
movie_title = str(movie_soup.find("h1", class_="Title").text).replace("فيلم", "").replace("مسلسل", "").replace("مترجم", "").strip()

# MetaTermsInfo
meta_terms_info = movie_soup.find("div", class_="MetaTermsInfo")
year = None
type = None
lang = None

try:
    if meta_terms_info is not None:
        meta_terms_info = meta_terms_info.find_all("li")
        for i in range(len(meta_terms_info)):
            meta_terms_info_span = meta_terms_info[i].find("span").text
            meta_terms_info_a = meta_terms_info[i].find("a").text
            if "السنه" in meta_terms_info_span:
                year = meta_terms_info_a
            elif "النوع" in meta_terms_info_span:
                type = meta_terms_info_a
            elif "اللغة" in meta_terms_info_span:
                lang = meta_terms_info_a
except:
    pass

# Get Movie Img
movie_img = movie_soup.find("div", class_="hold").find("img")["data-src"]

# Get Movie Description
movie_description = movie_soup.find_all("p", class_="descrip")[1].text

try:
    rating = movie_soup.find("div", class_="RatingImdb").find("em").text    
except:
    rating = None

# Get Movie Wathc Page
movie_watch_page_link = movie_soup.find("a", class_="watchBTn")["href"]

movie_watch_page = requests.get(movie_watch_page_link)
movie_watch_soup = BeautifulSoup(movie_watch_page.content, "html.parser")

movie_watch_iframe = movie_watch_soup.find("iframe")["src"]

# Request Movie Iframe Page
movie_iframe_page = requests.get(movie_watch_iframe)
movie_iframe_soup = BeautifulSoup(movie_iframe_page.content, "html.parser")

# Get Movie Download Link
movie_download_link = movie_iframe_soup.find("source")["src"]

print("1. Movie Player")
print("2. Download Movie")
print("3. Excel Sheet")
print("4. Exit")

ask = input("Enter number: ")
if ask == "1":
    webbrowser.open(movie_watch_iframe)
elif ask == "2":
    webbrowser.open(movie_download_link)
elif ask == "3":
    # Export data to CSV file pandas
    df = pd.DataFrame({"titles": ["Title", "Year","Type" , "Language", "Image Link", "Description", "Rating", "Download Link", "Watch Link"], "Data": [movie_title, year, type, lang, movie_img, movie_description, rating, movie_download_link, movie_watch_iframe]})
    df.to_html("data.html".format(movie_title), index=False, header=False)
    webbrowser.open("data.html".format(movie_title))

  
input("Enter any key to exit: ")
