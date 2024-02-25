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


def pre_processing(msgs):
    model = KeyedVectors.load("model_vec.d2v")
    tv = TfidfVectorizer()
    X = tv.fit_transform(msgs)
    names = tv.get_feature_names_out()
    vectors = np.zeros((len(msgs), len(names)))
    i = 0
    for email in msgs:
        j = 0
        weights = {word: X[i, idx] for word, idx in zip(names, range(len(names)))}
        for word in weights:
            if word in model:
                vectors[i,j] = np.mean(model[word] * weights[word])
            j += 1
        i += 1    
    return vectors
    