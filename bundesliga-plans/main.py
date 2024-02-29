import requests
import selectorlib
import sqlite3

URL = "https://www.bundesliga.com/de/bundesliga/spieltag"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36',
    'Content-Type': 'application/json'
}


class MatchPlans:
    def scrape(self, url):
        """ Scrape the page source from the URL """
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file('match-plans.yaml')
        match_info = extractor.extract(source)["match-info"]
        match_teams = extractor.extract(source)["match-teams"]
        return {"match-info": match_info,
                "teams": match_teams}

    def process(self, extracted_content):
        match_number = extracted_content["match-info"].partition("Saison 2023-2024")[0].strip()
        match_info = tuple([match_number])
        match_teams = extracted_content["teams"]
        match_teams_vs = list(zip(match_teams[::2], match_teams[1::2]))
        values_sql = [match_info + team for team in match_teams_vs]
        return values_sql


class TextFile:
    def save(self, data):
        text = "\n".join(str(el) for el in data)
        with open('match.txt', 'w') as file:
            file.write(text)


class SQLDB:
    def __init__(self):
        self.connection = sqlite3.connect("../databases/match-data.db")

    def store(self, data):
        cursor = self.connection.cursor()
        cursor.executemany("INSERT INTO MatchInfos VALUES(?, ?, ?)", data)
        self.connection.commit()

    def read(self, data):
        match_number = data["match-info"].partition("Saison 2023-2024")[0].strip()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM MatchInfos WHERE match_number=?", (match_number,))
        records_from_sql = cursor.fetchall()
        return records_from_sql


if __name__ == "__main__":
    matches = MatchPlans()         # Create a instance 'matches' by calling the class MatchPlans()
    content = matches.scrape(URL)
    extracted = matches.extract(content)

    sql_db = SQLDB()
    records = sql_db.read(extracted)
    if len(records) == 0:
        processed = matches.process(extracted)
        txt_file = TextFile()
        txt_file.save(processed)
        sql_db.store(processed)
        print("New info about the Bundesliga matches is inserted into the database.")
    else:
        print("There is no update.")
