import json
from collections import Counter

import pandas as pd
from flask import request, make_response
from sklearn import preprocessing

from app import g
from app import loaded_model
from helper.pre_process_data import pre_process
from views import views

columns = [
    'pr_comments',
    'Category'
]


def create_dataframe(data, max_pr_count=200):
    pr_count = 1
    df = pd.DataFrame(columns=columns)

    for item in data:
        print "Loading PR - {}/{}".format(pr_count, max_pr_count)

        pr = item.as_pull_request()
        pr_comments = [comments.body for comments in pr.get_comments() if comments.body != '']
        if len(pr_comments) == 0:
            pr_comments = ["no comments"]
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    {
                        'pr_comments': pr_comments,
                        'Category': [None]*len(pr_comments)
                    })
            ],
            ignore_index=True,
            sort=False
        )

        pr_count += 1

    return df


@views.route('/comments', methods=['POST'])
def get_comments():
    if request.method == 'POST':
        data = json.loads(request.data)
        repo = data.get('repo')
        author = data.get('author')
        query = "repo:{} author:{} type:pr".format(repo, author)
        data = g.search_issues(
            query=query,
            sort='created',
            order='desc'
        )
        data_frame = create_dataframe(data=data)

        xvalid_tfidf_ngram_chars = pre_process(pr_data=data_frame)
        y_pred = loaded_model.predict(xvalid_tfidf_ngram_chars)

        encoder = preprocessing.LabelEncoder()
        encoder.fit_transform(['No review comments', 'Minor', 'Moderate', 'Critical'])
        result_data = encoder.inverse_transform(y_pred)

        result_data = Counter(result_data)

        resp = make_response(json.dumps(result_data))
        resp.content_type = "application/json"
        return resp

