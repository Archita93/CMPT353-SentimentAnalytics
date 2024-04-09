import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
import ssl
from newspaper import Article, ArticleException
import requests
from multiprocessing import Pool

from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import RequestException
import requests
from urllib3.exceptions import NewConnectionError, MaxRetryError
from bs4 import BeautifulSoup
import csv
import re 

ssl._create_default_https_context = ssl._create_unverified_context

def scrape_url_allsides(url_news):

    try:
        response = requests.get(url_news)
        soup = BeautifulSoup(response.content, 'html.parser')
        read_more_div = soup.find('div', class_='read-more-story')
        if read_more_div:
            full_story_url = read_more_div.find('a')['href']
            return full_story_url
        else:
            return None
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError, NewConnectionError, MaxRetryError):
        return None
    

def scrape_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='views-row')
        data = []

        for article in articles:
            published_date = article.find('p', class_='search-result-publish-date').text.strip() if article.find('p', class_='search-result-publish-date') else 'NaN'
            title = article.find('h3', class_='search-result-title').text.strip() if article.find('h3', class_='search-result-title') else 'NaN'
            content_allsides = article.find('a', class_='search-result-body').text.strip() if article.find('a', class_='search-result-body') else 'NaN'
            url = article.find('a', class_='search-result-body')['href'] if article.find('a', class_='search-result-body') else 'NaN'
            news_channel = article.find('a', class_='search-result-source').text.strip() if article.find('a', class_='search-result-source') else 'NaN'
            bias = article.find('img')['src'].split('-')[-1].strip().split('.')[0] if article.find('img') else 'NaN'
            tags_element = article.find('p', class_='search-result-tags') if article.find('p', class_='search-result-tags') else None

            if tags_element:
                tags_html = tags_element.find('span', class_='field-content').prettify()  # Get the HTML content of the tags
                soup = BeautifulSoup(tags_html, 'html.parser')  # Create a new BeautifulSoup object with the HTML content
                tags = soup.find_all('a')  # Find all <a> tags within the HTML
                tag_texts = [tag.text.strip()  for tag in tags]  # Extract tag text from <a> tags
            else:
                tag_texts = None

            news_channel_url = scrape_url_allsides(url) if url != 'NaN' else 'NaN'
            print(news_channel_url)

            data.append({
                'Published Date': published_date,
                'Title': title,
                'AllSides Content': content_allsides,
                'URL': url,
                'News Channel': news_channel,
                "News Channel URL": news_channel_url,
                'Bias': bias,
                'Tags':tag_texts,
            })

        return data

    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError, NewConnectionError, MaxRetryError, AttributeError):
        return []

def return_all_pages(args):
    n, url = args
    data = scrape_page(url)
    for i in range(1, n):
        url_new = url + "&page=" + str(i)
        data += scrape_page(url_new)

    return data

def get_data(topic,url_skeleton,n):
    final_url = url_skeleton.format(topic)
    with Pool(processes=8) as pool:  # Adjust the number of processes based on your system's capabilities
        urls = [(n, final_url)]
        urls.extend([(n, final_url + f"&page={i}") for i in range(1, n)])
        data = pool.map(return_all_pages, urls)

    data = [item for sublist in data for item in sublist]
    df = pd.DataFrame(data)
    df['topic'] = topic
    return df 

    # final_url = url_skeleton.format(topic)
    # data = return_all_pages(n, final_url)
    # df = pd.DataFrame(data)
    # df['topic'] = topic
    # return df 

 
def main():
    topic_1 = ["healthcare","public-health","abortion"]
    topic_2 = ["housing-and-homelessness","immigration","economy-and-jobs"]
    
    data_one = pd.DataFrame()

    url_skeleton = "https://www.allsides.com/search?search={}&item_bundle=1&sort_by=node_created"

    for topic in topic_1:
        data_one = pd.concat([data_one, get_data(topic, url_skeleton, 500)], ignore_index=True)

    # data_two = get_data(topic_2,url_skeleton,1)
    
    data_one.to_csv('trial_one.csv', index=False)
    # data_two.to_csv('trial_two.csv', index=False)

    print(data_one.head(10))
    # print(data_two.head(10))
    # df.to_csv('output.csv', index=False)


if __name__=='__main__':
    main()
