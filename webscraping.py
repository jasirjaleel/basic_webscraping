from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={"id": "priceblock_ourprice"}).string.strip()
    except AttributeError:
        price = ""
    return price

def get_rating(soup):
    try:
        rating = soup.find("span", attrs={"id": "acrPopover"}).string.strip()
    except AttributeError:
        rating = ""
    return rating

def get_reviews(soup):
    try:
        reviews = soup.find("span", attrs={"id": "acrCustomerReviewText"}).string.strip()
    except AttributeError:
        reviews = ""
    return reviews

def get_availability(soup):
    try:
        availability = soup.find("div", attrs={"id": "availability"}).find("span").text.strip()
    except AttributeError:
        availability = ""
    return availability 

if __name__ == "__main__":
    URL = 'https://www.amazon.in/s?k=macbook+air'
    HEADERS = ({ 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",'Accept-Language': 'en-US,en;q=0.9',
})

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", {"class": "a-link-normal s-underline-text s-underline-link-text-xs"})
    links_list = []
    for link in links:
        links_list.append(link.get('href'))
    
    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        d["title"].append(get_title(new_soup))
        d["price"].append(get_price(new_soup))
        d["rating"].append(get_rating(new_soup))
        d["reviews"].append(get_reviews(new_soup))
        d["availability"].append(get_availability(new_soup))
    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df = amazon_df[amazon_df['title'] != '']  # Filter out rows with empty titles
    amazon_df.to_csv("amazon_products.csv", index=False)

