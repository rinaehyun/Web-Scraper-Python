import requests
import selectorlib

URL = "https://www.bundesliga.com/de/bundesliga/spieltag"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36',
    'Content-Type': 'application/json'
}

def scrape(url):
    """ Scrape the page source from the URL """
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('match-plans.yaml')
    match_info = extractor.extract(source)["match-info"]
    match_time_details = extractor.extract(source)["match-time-details"]
    match_teams = extractor.extract(source)["match-teams"]
    return match_info, match_time_details, match_teams


def process(extracted):
    match_info = extracted[0]["match-number"]
    match_teams = extracted[len(extracted)-1]
    match_teams_vs = list(zip(match_teams[::2], match_teams[1::2]))
    home_teams = match_teams[0::2]
    away_teams = match_teams[1::2]
    return match_info, match_teams_vs, home_teams, away_teams


if __name__ == "__main__":
    content = scrape(URL)
    extracted = extract(content)
    print(process(extracted))
