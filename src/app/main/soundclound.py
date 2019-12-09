import requests
from app import app
from bs4 import BeautifulSoup


class SoundCloudHelper(object):
    def __init__(self):
        return

    def search(search):

        results = []
        query = f"{app.config['SC_SEARCH_URL']}{search.replace(' ', '%20')}"
        page = requests.get(query)
        soup = BeautifulSoup(page.content, "html.parser")

        for link in soup.find_all("a", href=True):
            results.append("https://soundcloud.com" + link["href"])

        app.logger.warning("BEFORE CHOP: {results}")
        results = results[6:9]
        app.logger.warning("AFTER CHOP: {results}")

        return results
