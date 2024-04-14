# CMPT353-SentimentAnalytics

### Project Title

News agencies often use various tactics to influence viewers toward their political stance. These methods include appealing to emotions, omitting important context, and sometimes disseminating false information. As global polarisation increases, it is increasingly crucial to understand how news outlets manipulate readers' emotions and perceptions. Hence, this project aims to explore potential media bias by questioning whether news outlets from different political standings (Left, Right and Centre) use sentimental language, namely positive or negative, to report on topics with suspected polarisation such as Abortion, Immigration, etc, which could influence an emotional reaction amongst readers.

## Getting Started 

Here is a structure of our directory

CMPT353-SentimentAnalytics/
│
├── data_creation_scripts/         # Scripts for data preparation and scraping
│   
│   ├── labeler.py                # Script to add the sentiment scores 
│   ├── news_scraping.py          # Script to extract actual content from news sources
│   └── news_sources.py           # Script to scrape news articles
|   └── summary.py                # Script to summarise news article
|
├── data_creation_scripts/         # Scripts for data preparation and scraping
│   
│   ├── abortion_news.csv          # Script produced after running news_scraping.py                                                       
│   ├── healthcare_news.csv        # Script produced after running news_scraping.py  
│   └── environment_news.csv       # Script produced after running news_scraping.py  
|   └── immigration_news.csv       # Script produced after running news_scraping.py  
|   └── public-health_news.csv     # Script produced after running news_scraping.py  
|   └── sustainability_news.csv    # Script produced after running news_scraping.py  
|   └── labeled.csv                 # Non-duplicated data produced after running labeler.py
|   └── test.csv                    # Duplicated data produced after running labeler.py
|   └── final_summ.csv              # Data produced after running summary.py
|
├── scripts_old/         # Not relevant scripts - initialised in the beginning of the project
│   
│   ├── news_scraper.py               
│   ├── news_sources.ipynb          
│   └── news_sources_old.py           
|
├── data_cleaning.ipynb                    
├── model.ipynb        
├── requirements.txt  # contains all the required packages
├── requirements.txt


Instructions:

Step 1: Create a Virtual Environment using pip and install all the packages using requirements.txt (these commands are applicable to Unix/Mac)

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

Step 2: Create the Dataset

 2a: Retrieve all the articles pertaining to a topic using news_sources.py 

     python script.py <topic> (topic can be "abortion", "immigration" etc)
      
     Output: <topic>.csv
 
 2b: Populate the actual article content based on the URL using news_scraping.py 
      
     python news_sources.py <topic>.csv <topic>_news.csv
     
     Output: <topic>_news.csv
  
 2c: Combine all the datasets in data_cleaning.ipynb and output a csv file called - news_data_all.csv
  
Step 3: Run summary.py to attain all the three distinct summaries of the news articles 
      
     python summary.py
     
     Output: final_summ.py 
     
Step 4: Run labeler.py to attain the two sentiment scores for all the news articles and their corresponding summaries 
     
     python labeler.py final_summ.py
     
     Output: labeled.csv

model.ipynb and results.ipynb use labeled.csv to produce the model results and perform exploratory data analysis 

* Limitations identified in our project: When we merged all the data to produce a combined dataset in data_cleaning.ipynb, we discovered a significant number of duplicates that significantly affected the outcomes of our model and subsequent analyses. So, initially, we had created test.csv, which contained duplicated data resulting from executing labeler.py. However, after recognizing the issue with duplicates, we later generated a new dataset named labeled.csv, which comprised non-duplicated data processed after running labeler.py.
