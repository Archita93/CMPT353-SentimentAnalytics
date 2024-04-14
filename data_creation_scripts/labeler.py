import sys
import nltk.sentiment
import pandas as pd
import nltk

data = pd.read_csv(sys.argv[1], keep_default_na=False)


print(data)


def pre_process(text):

    #First tokenize the text to continue
    tokens = nltk.tokenize.word_tokenize(text.lower())

    #remove stop words:
    stopword_list = nltk.corpus.stopwords.words('english')

    filtered_tokens = [token for token in tokens if token not in stopword_list]

    lemmatizer = nltk.stem.WordNetLemmatizer()

    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    processed_text = ' '.join(lemmatized_tokens)

    return processed_text


def sentiment_analysis(processed_text):


    analyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()

    score = analyzer.polarity_scores(processed_text)

    return score['compound']

data['Processed text'] = data['Content'].apply(pre_process)
data['Sentiment'] = data['Processed text'].apply(sentiment_analysis)

print(data)

data.to_csv('test.csv')

