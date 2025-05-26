#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PySimpleGUI as sg
import os
import pandas as pd
import gzip
import json
import numpy as np
from tensorflow.keras.models import load_model #to load a saved mode
from langdetect import detect
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
import tensorflow as tf
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import sklearn
from sklearn import preprocessing
from sklearn import model_selection
import keras
from tensorflow.keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import *
from keras.models import *

nltk.download ('stopwords')
nltk.download ('punkt')
nltk.download ('wordnet')



sg.theme('Dark Blue 2')

layout = [[sg.Text('Select File (.json, .csv, or .xlsx)')],
            [sg.Input(key='file'), sg.FileBrowse()],
            [sg.Text(' ')], 
            [sg.Text('Input Review Column Name EXACTLY AS IT APPEARS')],
            [sg.Input(key='col_name')],
            [sg.Checkbox('Reviews are in English', key='English')],
            [sg.OK(), sg.Cancel()] ]

window = sg.Window('Sentiment Labeler', layout, enable_close_attempted_event=True, finalize=True)
window.bring_to_front()
while True:
    event, values = window.read()
    text = values['file']
    colname = values['col_name']
    LangCheck=values['English']
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit' or event == 'Cancel') and sg.popup_yes_no('Are you sure you want to exit?') == 'Yes':
        break
    elif event == 'OK' and len(text)>0 and len(colname)>0:
        sg.popup(text, 'will be processed!')
        
        max_value = 100
        progress_bar = sg.ProgressBar(max_value, orientation='h', size=(20, 20))

        layout_progress = [[sg.Text('Processing...', size=(15, 1))], [progress_bar]]

        window_progress = sg.Window('Processing', layout_progress, finalize=True)

        progress_bar.update_bar(10)
        fileloc = os.path.splitext(text)
        file_extension = str(fileloc).split('.', 1)[1]
        
        
        
        if 'json' and '.gz' in file_extension:
            def parse(path):
                g = gzip.open(path, 'rb')
                for l in g:
                  yield json.loads(l)
          
            def getDF(path):
              i = 0
              df = {}
              for d in parse(path):
                df[i] = d
                i += 1
              return pd.DataFrame.from_dict(df, orient='index')
            
            DF = getDF(text)
        elif 'json' in file_extension and '.gz' not in file_extension: 
            DF = pd.read_json(text, lines=True)
        elif 'csv' in file_extension:
            DF = pandas.read_csv(text)
        elif 'xlsx' or 'xls' in file_extension:
            DF = pd.read_excel(text)
        progress_bar.update_bar(10)
        
        
        DF.dropna(subset = [colname], inplace = True)
        
        
        
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        table = str.maketrans("", "", letters)
        DF['Unusual']=DF[colname].str.translate(table)
        
        
        numbers = "0123456789"
        nums = str.maketrans("", "", numbers)
        DF['Unusual']=DF['Unusual'].str.translate(nums)
        
        
        
        Punc = str.maketrans("", "", string.punctuation)
        DF['Unusual']=DF['Unusual'].str.translate(Punc)
        
        
        Extras = "\n \t"
        Spaces= str.maketrans("", "", Extras)
        DF['Unusual']=DF['Unusual'].str.translate(Spaces)
        
        
        Unusual = DF['Unusual'][(DF['Unusual'].isnull() == False)].to_list()
        
        
        x = ''.join(Unusual)
        Unknown= str.maketrans("", "", x)
        
        
        DF['Review_Cleaned']=DF[colname].str.translate(Punc)
        DF['Review_Cleaned']=DF['Review_Cleaned'].str.translate(nums)
        ReturnChars = "\n\t"
        Returns= str.maketrans("", "", ReturnChars)
        DF['Review_Cleaned']=DF['Review_Cleaned'].str.translate(Returns)
        DF['Review_Cleaned']=DF['Review_Cleaned'].str.translate(Unknown)
        DF['ReviewsNoPunct']=DF['Review_Cleaned']
        
        progress_bar.update_bar(20)
        lemmatizer = nltk.stem.WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        negationwords = ['not','ain', 'aren','can', "aren't", 'don', "don't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
        'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 
        'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 
        'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 
        'wouldn', "wouldn't", 'no']
        stop_words = [x for x in stop_words if x not in negationwords]
        
        
        
        def clean_reviews(text):
            text = text.lower()
            tokens = word_tokenize(text)
            cleaned_text = []
            i = 0
            while i < len(tokens):
                if tokens[i] in stop_words:
                    i += 1
                else:
                    if tokens[i] in negationwords:
                        if i + 1 < len(tokens):
                            concatenated_word = tokens[i] + '_' + tokens[i + 1]
                            cleaned_text.append(lemmatizer.lemmatize(concatenated_word))
                            i += 2
                        else:
                            cleaned_text.append(lemmatizer.lemmatize(tokens[i]))
                            i += 1
                    else:
                        cleaned_text.append(lemmatizer.lemmatize(tokens[i]))
                        i += 1
            return cleaned_text
        
        DF['Review_Cleaned'] = DF['Review_Cleaned'].apply(clean_reviews)
        
        progress_bar.update_bar(30)
        
        DF['TokenLen'] = DF['Review_Cleaned'].apply(lambda x: len(x))
        
        progress_bar.update_bar(40)
        
        DF = DF[(DF['TokenLen'] != 0)]
        
        
        if LangCheck == False:
            DF['lang'] = DF['ReviewsNoPunct'].apply(lambda x: detect(x))
            DF=DF.loc[DF['lang'] != "es"]
        
        progress_bar.update_bar(50)
        
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(DF['Review_Cleaned'])
        reviews_to_list = DF['Review_Cleaned'].tolist()
        sequences=tokenizer.texts_to_sequences(reviews_to_list)
        
        progress_bar.update_bar(60)
        
        X = pad_sequences(sequences, padding="post", maxlen = 40)
        
        
        reconstructed_model_sentiment = keras.models.load_model('best_rnn_model_sentiment.keras')
        
        progress_bar.update_bar(70)
        
        predictions_sent = reconstructed_model_sentiment(X)
        #negative, positive
        
        
        
        
        DF['Predicted_Sentiment']= np.argmax(predictions_sent, axis=1)
        
        progress_bar.update_bar(80)
        
        
        DF['Predicted_Sentiment'] = DF['Predicted_Sentiment'].replace({0:'Negative', 1:'Positive'})
    
        progress_bar.update_bar(90)
    
    
        if LangCheck == False:
            DF=DF.drop(columns=['Unusual','Review_Cleaned', 'TokenLen', 'lang', 'ReviewsNoPunct'])
        else:
            DF=DF.drop(columns=['Unusual','Review_Cleaned', 'TokenLen', 'ReviewsNoPunct'])
            
        folder_name = "Labeled Reviews"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            
        file_path = os.path.join(folder_name, 'Predicted_Reviews_{}.xlsx'.format(datetime.now().strftime("%Y-%m-%d %H%M%S")))
        
        DF.to_excel(file_path, index=False)
        progress_bar.update_bar(100)
    
        window_progress.close()
    
        sg.theme('Dark Blue 2')
    
        layout_final = [[sg.Text('The file was processed successfully!',pad=((30, 0), 1))],
                        [sg.Button('OK', pad=((125, 0),5))]]
        
        window_final = sg.Window('Sentiment Labeler', layout_final, 
                                 size=(300, 70), enable_close_attempted_event=True, finalize=True)
        window_final.bring_to_front()
        while True:
            event,values = window_final.read()
            if event == sg.WINDOW_CLOSED or event == 'OK' or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                break
        window_final.close()
        
        break
    elif event == 'OK' and len(text)>0 and len(colname)==0:
        sg.popup('Please input the review column name!')
    elif event == 'OK' and len(text)== 0:
        sg.popup('Please select a file!')
window.close()    


