import requests
import selectorlib
import sqlite3

URL = "https://www.bundesliga.com/de/bundesliga/spieltag"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36',
    'Content-Type': 'application/json'
}

connection = sqlite3.connect("../databases/match-data.db")

def scrape(url):
    """ Scrape the page source from the URL """
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('match-plans.yaml')
    match_info = extractor.extract(source)["match-info"]
    match_teams = extractor.extract(source)["match-teams"]
    return {"match-info": match_info,
            "teams": match_teams}


def process(extracted):
    match_number = extracted["match-info"].partition("Saison 2023-2024")[0]
    match_info = tuple([match_number])

    match_teams = extracted["teams"]
    match_teams_vs = list(zip(match_teams[::2], match_teams[1::2]))
    values_sql = [match_info + team for team in match_teams_vs]

    return values_sql


def save_as_text(data):
    text = "\n".join(str(el) for el in data)
    with open('match.txt', 'w') as file:
        file.write(text)


def store_to_sql(data):
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO MatchInfos VALUES(?, ?, ?)", data)
    connection.commit()


if __name__ == "__main__":
    content = scrape(URL)
    extracted = extract(content)
    processed = process(extracted)
    save_as_text(processed)
    store_to_sql(processed)
