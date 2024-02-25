from sklearn.decomposition import PCA
import gensim.downloader as api
from tensorflow.keras import layers
import tensorflow as tf
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

pre_labels2 = [
    "Personal",
    "Work",
    "Finance",
    "Receipts",
    "Travel",
    "Events",
    "Promotions",
    "Newsletters",
    "Social",
    "Updates",
    "Notifications",
    "Education",
    "Health",
    "Shopping",
    "Bills",
    "Subscriptions",
    "Legal",
    "Projects",
    "Meetings",
    "Invitations",
    "Feedback",
    "Surveys",
    "Offers",
    "Coupons",
    "Announcements",
    "Shipping",
    "Orders",
    "Support",
    "Security",
    "Confirmations",
    "Reminders",
    "Appointments",
    "Entertainment",
    "Sports",
    "Technology",
    "Science",
    "Human Resources",
    "Marketing",
    "Sales",
    "Operations",
    "Customer Service",
    "Management",
    "IT Support",
    "Development",
    "Research",
    "Collaboration",
    "Networking",
    "Fundraising",
    "Volunteering",
    "Miscellaneous"
]

pre_labels = ['personal',
 'work',
 'finance',
 'receipt',
 'travel',
 'event',
 'promotion',
 'newsletter',
 'social',
 'update',
 'notification',
 'education',
 'health',
 'shopping',
 'bill',
 'subscription',
 'legal',
 'project',
 'meeting',
 'invitation',
 'feedback',
 'survey',
 'offer',
 'coupon',
 'announcement',
 'shipping',
 'order',
 'support',
 'security',
 'confirmation',
 'reminder',
 'appointment',
 'entertainment',
 'sport',
 'technology',
 'science',
 'human resource',
 'marketing',
 'sale',
 'operation',
 'customer service',
 'management',
 'it support',
 'development',
 'research',
 'collaboration',
 'network',
 'fundraise',
 'volunteer',
 'miscellaneous']

def remove_stopwords(lines, sw = stopwords.words('english')):
    res = []
    for line in lines:
        original = line
        line = [w for w in line if w not in sw]
        if len(line) < 1:
            line = original
        res.append(line)
    return res

def cleanup(msgs):
    nlp = spacy.load('en_core_web_sm')
    new_msgs = []
    for msg in msgs:
        new_msg = re.sub(r"\W", " ", msg).lower() 
        # tokenize
        new_msg = word_tokenize(new_msg)
        new_msgs.append(new_msg)    
        
    new_3_msgs = []
    new_new_msgs = [" ".join(item) for item in remove_stopwords(new_msgs)]
    for new_msg in new_new_msgs:
        doc = nlp(new_msg)
        new_3_msg = [token.lemma_ for token in doc]
        new_3_msgs.append(" ".join(new_3_msg))

    return new_3_msgs 

def pre_processing(msgs):
    model = KeyedVectors.load("model_vec.d2v")
    vectors = np.zeros((len(msgs), 25))
    for idx, email in enumerate(msgs):
        tv = TfidfVectorizer()
        try:
            X = tv.fit_transform([email])
        except:
            continue
        names = tv.get_feature_names_out()
        weights = {word: X[0, idx] for word, idx in zip(names, range(len(names)))}
        l = []
        for word in weights:
            if word in model:
                l.append(model[word] * weights[word])
        vectors[idx] = (np.array(l).mean(axis=0))    
    return vectors


def cluster(vectors):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(vectors)
    Z = linkage(scaled, method='complete')
    fig = plt.figure(figsize=(10, 7))
    dendrogram(Z)
    fig.tight_layout
    return Z, plt

def label_maker(clusters):
    
    vectorizer = TfidfVectorizer()

    vectorizer.fit(pre_labels)  
    label_vectors = vectorizer.transform(pre_labels)
    
    dictionary = {}

    for i, cluster in enumerate(clusters):
        aggregate_scores = np.zeros(len(pre_labels))
        word_counts = {}
        for word in cluster:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1


        top_words = sorted(word_counts, key=word_counts.get)

        for word in top_words:
            word_vector = vectorizer.transform([word])
            similarities = cosine_similarity(word_vector, label_vectors).flatten()
            aggregate_scores += similarities


        # Find the label with the highest similarity
        max_sim_index = np.argmax(aggregate_scores)
        assigned_label = pre_labels2[max_sim_index]
        
        dictionary[i] = assigned_label
        
    return dictionary

        
        
        
        
        
        
        
        