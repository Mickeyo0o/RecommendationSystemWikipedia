# Wikipedia Article Recommendation System - Information Retrieval

Welcome to our Wikipedia Article Recommendation System project repository! This system aims to recommend Wikipedia articles based on previous user queries, optimizing for generating high traffic on Wikipedia websites.

## Features

* <b>Data Scraping and Crawling:</b> Our scrapy folder contains a program to crawl through Wikipedia and scrape random articles for data generation.
* <b>Data Split:</b> We split the contents of each article into separate databases for titles and contents.
* <b>Data Preprocessing:</b> After scraping around 1000 articles, we performed basic preprocessing and vectorized each text.
* <b>Data Visualizations:</b> We conducted exploratory data analysis and visualizations to understand the gathered data better.
* <b>KMeans Algorithm:</b> Using provided previous searches, we apply the KMeans algorithm to select the larger group containing similar searches.
* <b>Cosine Similarity:</b> We compare the similarity of query links to the links in the database and calculate cosine similarity of their contents and titles separately.
* <b>Link Calculation:</b> We identify the websites from the database with the largest amount of external links, increasing the likelihood of users further exploring Wikipedia articles.
* <b>Final Recommendation Acquisition:</b> Based on the described formula, we present the best matches to the user.
* <b>Examples:</b> We provide examples of our recommendation system's performance.

## Usage

* <b>Scraping:</b> To perform scraping, install the required libraries provided in the .py files inside the scrapy folder. Use the following command in the command line:

    python scrap.py -l [list of initial links] (OPTIONAL) -n [sites to scrap (Default 1000)]

* <b>Results Viewing:</b> Download or view the Report.ipynb on GitHub. Note that interactive graphs representing similarities had to be removed to reduce notebook size.
* <b>Notebook Running:</b> To run the notebook, download the scraped *.csv files containing the data and place them in the same folder as the Report.ipynb. Also, download the scrapy folder for scraping functionalities. Ensure to download all mentioned libraries in the report and .py files from the scrapy folder.

## Note

This project was completed as a part of the Information Retrieval Course.

## Creators

* Kajetan Sulwiński (ekohachi22)
* Mikołaj Marmurowicz (Mickeyo0o)
