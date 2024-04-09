import pandas as pd
import numpy as np
from newspaper import Article, ArticleException
import os
import sys
from multiprocessing import Pool


def scrape_page(url):
    print(url)
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        print("An exception occurred")
        return None
    

def main(input_directory, output_directory):

    # Read data from input file
    data = pd.read_csv(input_directory)
    
    urls = data["News Channel URL"].tolist()
    
    # Use multiprocessing to scrape news article content
    with Pool() as pool:
        article_contents = pool.map(scrape_page, urls)
    
    # Add scraped content to DataFrame
    data["News Article Content"] = article_contents
    
    # Save cleaned data to output file
    data.to_csv(output_directory, index=False)

if __name__=='__main__':
    # Input and output directories provided as command-line arguments
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    
    # Call main function with input and output directories
    main(input_directory, output_directory)

