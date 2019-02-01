import pickle
import re

import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


def clean(x):
    try:
        x = re.sub(r'http\S+', '', x)
        x = re.sub(r'`(.*?)`', '', str(x))
        x = str(x).lower()
        x = re.sub('[^\w\s]', '', x)
        stop = stopwords.words('english')
        x = [word for word in x.split() if word not in stop]
        return " ".join(x)
    except:
        if x == 'nan':
            return str(x)
        return x


def pre_process(pr_data):
    pr_data['pr_comments'] = pr_data.apply(lambda x: clean(x.pr_comments), axis=1)
    pr_data = pr_data.replace(np.nan, 'no comments', regex=True)

    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    count_vect.fit(pr_data['pr_comments'])

    loaded_count_vec = pickle.load(open("models/count_vect.sav", 'rb'))
    xvalid_tfidf_ngram_chars = loaded_count_vec.transform(pr_data['pr_comments'])

    return xvalid_tfidf_ngram_chars

