import requests

URL = "https://www.bundesliga.com/de/bundesliga/spieltag"


def scrape(url):
    """ Scrape the page source from the URL """
    response = requests.get(url)
    source = response.text
    return source


if __name__ == "__main__":
    print(scrape(URL))
