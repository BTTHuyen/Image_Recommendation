import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

subscription_key = "9b521c515a0b4467ac3bb2739ca40939"
search_url = "https://api.bing.microsoft.com/v7.0/images/search"

mkt = "en-US" #the market where the results come from

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}


def image_search(search_term,mkt,Num_of_images=5):
    params  = {"q": search_term, "license": "public", "imageType": "photo", "mkt": mkt}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:Num_of_images]]
    return thumbnail_urls
