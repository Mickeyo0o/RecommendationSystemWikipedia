import os, sys

_i = os.path.abspath("")
if _i not in sys.path:
    sys.path.insert(0, _i)
del _i  # clean up global name space

import scrapy
import re
import argparse
import pickle
from scrapy.crawler import CrawlerProcess
from itemadapter import ItemAdapter
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize


class Pipeline(object):
    def open_spider(self, spider):
        self.df = pd.DataFrame(columns=["URL", "title", "content"]).set_index("URL")

    def process_item(self, item, spider):
        item = ItemAdapter(item)
        url = item.get("URL")
        if url is None:
            return
        title = item.get("title")
        title = title.replace("\n", "")
        content = item.get("content")
        content = content.replace("\n", "")
        self.df.loc[url] = [title, content]

    def close_spider(self, spider):
        def _transform(data):
            lemmatizer = WordNetLemmatizer()
            return [
                lemmatizer.lemmatize(token)
                for token in word_tokenize(data)
                if token not in stopwords.words("english") and token.isalpha()
            ]

        title_vec = TfidfVectorizer(use_idf=True, min_df=2, ngram_range=(1, 2))
        content_vec = TfidfVectorizer(use_idf=True, min_df=15)
        self.df.apply(
            lambda x: [_transform(x["title"]), _transform(x["content"])], axis=1
        )
        title_res = title_vec.fit_transform(self.df.title)
        content_res = content_vec.fit_transform(self.df.content)
        title_df = pd.DataFrame(
            title_res.toarray(),
            columns=title_vec.get_feature_names_out(),
            index=self.df.index,
        )
        content_df = pd.DataFrame(
            content_res.toarray(),
            columns=content_vec.get_feature_names_out(),
            index=self.df.index,
        )
        title_df.to_csv("titles_transformed.csv")
        content_df.to_csv("content_transformed.csv")
        with open("title_vec.bin", "wb") as handle:
            pickle.dump(title_vec, handle)
        with open("content_vec.bin", "wb") as handle:
            pickle.dump(content_vec, handle)


class _Spider(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {"__main__.Pipeline": 0},
    }

    def __init__(
        self,
        name: str = None,
        start_urls: list = [],
        max_sites_to_scrap: int = 1000,
    ):
        self.name = name
        self.start_urls = start_urls
        self.max_sites_to_scrap = max_sites_to_scrap
        self.scrapped_sites_urls = []
        self.scrapped_sites_total = 0

    def parse(self, response):
        self.scrapped_sites_urls.append(response.url)
        possible_title_css = [
             ".mw-body-header.vector-page-titlebar h1 .mw-page-title-main::text",
             ".mw-body-header.vector-page-titlebar #firstHeading i::text",
             ".mw-body-header.vector-page-titlebar #firstHeading::text"
        ]
        for css in possible_title_css:
            title = response.css(
                css
            ).get()
            if title is not None:
                break
        if title is None:
            yield {"URL": None}
        content = response.css("div#bodyContent p::text").getall()
        content = "".join(content)
        yield {"URL": response.url, "title": title, "content": content}
        next_pages = response.css("div#bodyContent a::attr(href)").getall()
        for page in next_pages:
            next_page = response.urljoin(page)
            if (
                re.fullmatch("\/wiki\/[^:]*", page)
                and next_page not in self.scrapped_sites_urls
            ):
                self.scrapped_sites_total += 1
                if self.scrapped_sites_total <= self.max_sites_to_scrap:
                    yield scrapy.Request(
                        next_page,
                        callback=self.parse
                    )


def create_database(starting_urls: list, sites_to_scrap: int):
    process = CrawlerProcess()
    process.crawl(
        _Spider,
        name="spider",
        start_urls=starting_urls,
        max_sites_to_scrap=sites_to_scrap,
    )
    process.start()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        usage="python scrap.py -l [list of initial links] (OPTIONAL) -n [sites to scrap (Default 1000)]"
    )
    argparser.add_argument(
        "-l", "--list", nargs="+", help="<Required> Set flag", required=True
    )
    argparser.add_argument("-n", "--sites-to-scrap", type=int, default=1000)
    args = argparser.parse_args()
    create_database(args.list, args.sites_to_scrap)
