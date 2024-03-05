import requests
import pickle
from bs4 import BeautifulSoup

class OnePageScrapper:
    def __init__(self):
        with open('title_vec.bin', 'rb') as handle:
            self.title_vec = pickle.load(handle)
        with open('content_vec.bin', 'rb') as handle:
            self.content_vec = pickle.load(handle)
    
    def scrap_site(self, url: str) -> dict:
        req = requests.get(url)
        if req.status_code != 200:
            raise Exception(f"Server returned status code {req.status_code}")
        soup = BeautifulSoup(req.content, 'html.parser')
        possible_title_css = [
            ".mw-body-header.vector-page-titlebar h1 .mw-page-title-main",
            ".mw-body-header.vector-page-titlebar #firstHeading i",
            ".mw-body-header.vector-page-titlebar #firstHeading"

        ]
        for css in possible_title_css:
            title_el = soup.select_one(css)
            if title_el is not None:
                break
        if title_el is None:
            raise Exception("No title found!")
        title_str = title_el.text.strip()
        content_els = soup.select("div#bodyContent p")
        content_str = ' '.join([i.text.strip() for i in content_els])
        transformed_title = self.title_vec.transform([title_str]).toarray()
        transformed_content = self.content_vec.transform([content_str]).toarray()
        return {
            'title': transformed_title[0],
            'content': transformed_content[0]
        }



    