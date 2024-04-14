import sys
import nltk.sentiment
import pandas as pd
import nltk

from transformers import pipeline

#python labeler.py ./final_summ.csv


#nltk.download('all')

data = pd.read_csv(sys.argv[1], keep_default_na=False)

data.drop_duplicates(subset=['URL'], inplace=True)



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



def sentiment_analysis_nltk(processed_text):

    analyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()

    score = analyzer.polarity_scores(processed_text)

    return score['compound']


sentiment_pipeline_model_finiteautomata = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis", max_length=256, truncation=True)

def sentiment_analysis_finiteautomata(text):

    text = text[:256]

    dictionary = sentiment_pipeline_model_finiteautomata(text)[0]
    if dictionary['label'] == 'NEG':
        result = -dictionary['score']
    else:
        result = dictionary['score']
    return result

sentiment_pipeline_model_cardiffnlp = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")

def sentiment_analysis_huggingface_cardiffnlp(text):

    text = text[:256]
    dictionary = sentiment_pipeline_model_cardiffnlp(text)[0]
    if dictionary['label'] == 'LABEL_0':
        result = -dictionary['score']
    elif dictionary['label'] == 'LABEL_2':
        result = dictionary['score']
    else:
        result = 0
    return result


sentiment_pipeline_model_bhadresh = pipeline(model="bhadresh-savani/distilbert-base-uncased-emotion", max_length=256, truncation=True)

def sentiment_analysis_huggingface_bhadresh(text):


    result = sentiment_pipeline_model_bhadresh(text)


    return result



#News Article Content,Distil_Summary,Falcons_Summary,Bart_Summary

data['Processed text'] = data['News Article Content'].apply(pre_process)
data['Sentiment_Content_nltk'] = data['Processed text'].apply(sentiment_analysis_nltk)

data['Processed Distil'] = data['Distil_Summary'].apply(pre_process)
data['Sentiment_Distil_nltk'] = data['Processed Distil'].apply(sentiment_analysis_nltk)

data['Processed Falcons'] = data['Falcons_Summary'].apply(pre_process)
data['Sentiment_Falcons_nltk'] = data['Processed Falcons'].apply(sentiment_analysis_nltk)

data['Processed Bart'] = data['Bart_Summary'].apply(pre_process)
data['Sentiment_Bart_nltk'] = data['Processed Bart'].apply(sentiment_analysis_nltk)

data.drop(['Processed text', 'Processed Distil', 'Processed Falcons', 'Processed Bart'], axis=1)

data['Sentiment_Content_finiteautomata'] = data['News Article Content'].apply(sentiment_analysis_finiteautomata)
data['Sentiment_Distil_finiteautomata'] = data['Distil_Summary'].apply(sentiment_analysis_finiteautomata)
data['Sentiment_Falcons_finiteautomata'] = data['Falcons_Summary'].apply(sentiment_analysis_finiteautomata)
data['Sentiment_Bart_finiteautomata'] = data['Bart_Summary'].apply(sentiment_analysis_finiteautomata)

data['Sentiment_Content_cardiffnlp'] = data['News Article Content'].apply(sentiment_analysis_huggingface_cardiffnlp)
data['Sentiment_Distil_cardiffnlp'] = data['Distil_Summary'].apply(sentiment_analysis_huggingface_cardiffnlp)
data['Sentiment_Falcons_cardiffnlp'] = data['Falcons_Summary'].apply(sentiment_analysis_huggingface_cardiffnlp)
data['Sentiment_Bart_cardiffnlp'] = data['Bart_Summary'].apply(sentiment_analysis_huggingface_cardiffnlp)


data.to_csv('labeled_data.csv')

