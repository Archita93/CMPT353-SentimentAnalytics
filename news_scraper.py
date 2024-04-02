import newspaper as ns
from bs4 import BeautifulSoup
import requests
import pandas as pd

url_skeleton = 'https://www.allsides.com/topics/{}'


df = pd.DataFrame({'Title': pd.Series(dtype='str'),
                   'URL': pd.Series(dtype='str'),
                   'Keywords': pd.Series(dtype='str'),
                    'Category': pd.Series(dtype='str')})

topics = ['abortion', 'defense-and-security', 'economy-and-jobs', 'energy', 'environment', 'foreign-policy', 'sustainability', 'gun-control-and-gun-rights', 'violence-america', 'healthcare', 'public-health', 'housing-and-homelessness', 'race', 'civil-rights']

successes = 0
failures = 0

for topic in topics:
    reqs = requests.get(url_skeleton.format(topic))
    soup = BeautifulSoup(reqs.text, 'html.parser')
 
    urls_topic = []
    print("hello")
    for link in soup.find_all('a'):
        potential_link = link.get('href')
        if potential_link is None:
            potential_link = ['placeholder']
            empty = True
        else:
            empty = False

        if 'https://www.allsides.com/news/' in potential_link and not empty:
            urls_topic.append(link.get('href'))
    print("hello")


    for url in urls_topic:
        article = ns.Article(url )
        print("hello")
        article.download()
        try:
            article.parse()
            article.nlp()
            new_row = {'Title': article.title, 'URL': article.url, 'Keywords': article.keywords, 'Category': topic}

        # Append the dictionary to the DataFrame
            df.loc[len(df)] = new_row
            successes += 1
        except:
            print("An exception occurred")
            failures += 1

print(df)
print("Successes: " + str(successes))
print("Failures: " + str(failures))
df.to_csv('out.csv', index=False)

    
#print(paper.size())


'''
url = 'https://www.cbc.ca/news/canada/british-columbia/kelowna-cloned-cats-1.7146050'
article = ns.Article(url)

print(article.title)
'''