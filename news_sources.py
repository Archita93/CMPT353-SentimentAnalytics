import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_url_allsides(session, url_news):
    try:
        async with session.get(url_news) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            read_more_div = soup.find('div', class_='read-more-story')
            if read_more_div:
                full_story_url = read_more_div.find('a')['href']
                return full_story_url
            else:
                return None
    except (aiohttp.ClientError, AttributeError):
        return None

async def scrape_page(session, url):
    try:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
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

                news_channel_url = await scrape_url_allsides(session, url) if url != 'NaN' else 'NaN'
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

    except (aiohttp.ClientError, AttributeError):
        return []

async def return_all_pages(session, args):
    n, url = args
    data = await scrape_page(session, url)
    for i in range(1, n):
        url_new = url + f"&page={i}"
        data += await scrape_page(session, url_new)

    return data

# 40 for immigration, sustainability and public-health
# 45 for healhcare
# 50 for abortion

async def main(topic):
    url_skeleton = f"https://www.allsides.com/search?search={topic}&item_bundle=1&sort_by=node_created"
    total_pages = 38
    
    async with aiohttp.ClientSession() as session:
        initial_url = url_skeleton
        urls = [(total_pages, initial_url)] + [(total_pages, initial_url + f"&page={i}") for i in range(1, total_pages)]
        tasks = [return_all_pages(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    data = [item for sublist in results for item in sublist]
    df = pd.DataFrame(data)
    df['topic'] = topic
    
    # Save dataframe to CSV file
    df.to_csv(f"{topic}.csv", index=False)
    
    return df


async def main_wrapper(topic):
    df = await main(topic)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <topic>")
        sys.exit(1)

    topic = sys.argv[1]
    asyncio.run(main_wrapper(topic))

# async def main_wrapper():
#     # df = await main("abortion")
#     df = await main("healthcare")
#     # df = await main("public-health")
#     # df = await main("housing-and-homelessness")
#     # df = await main("immigration")
#     # df = await main("economy-and-jobs")

# asyncio.run(main_wrapper())

