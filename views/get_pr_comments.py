import pandas as pd
from flask import request, render_template

from app import g
from views import views

# Excel parameter for output
writer = pd.ExcelWriter('data/pr_comments_data.xlsx', engine='openpyxl')

columns = [
    'S.No',
    'Pull request',
    'Owner',
    'PR comments',
    'Review comments',
    'Issue Comments'
]


def create_excel_from_data(data, max_pr_per_sheet=20, max_pr_count=200):
    count = 0
    sheet_count = 1
    current_row = 0
    pr_count = 1

    for item in data:
        print "Loading PR - {}/{}".format(pr_count, max_pr_count)

        df = pd.DataFrame(columns=columns)
        pr = item.as_pull_request()

        pr_comments = [comments.body for comments in pr.get_comments() if comments.body != '']
        reviews = [comments.body for comments in pr.get_reviews() if comments.body != '']
        issues = [comments.body for comments in pr.get_issue_comments() if comments.body != '']

        max_comments = max(len(pr_comments), len(reviews), len(issues))

        for i in range(max_comments):
            df.loc[i] = [
                pr_count if i == 0 else '',
                pr.html_url if i == 0 else '',
                pr.user.login if i == 0 else '',
                pr_comments[i] if i < len(pr_comments) else '',
                reviews[i] if i < len(reviews) else '',
                issues[i] if i < len(issues) else '',
            ]

        if max_comments == 0:
            df.loc[0] = [
                pr_count,
                pr.html_url,
                pr.user.login,
                '',
                '',
                '',
            ]

        if count == 0:
            df.to_excel(writer, startrow=current_row, sheet_name='Sheet {}'.format(sheet_count), index=False)
        else:
            df.to_excel(writer, startrow=current_row + 2, sheet_name='Sheet {}'.format(sheet_count), header=False,
                        index=False)
            current_row += 2

        current_row += max_comments
        count += 1
        pr_count += 1

        if count == max_pr_per_sheet:
            sheet_count += 1
            count = 0
            current_row = 0
            if sheet_count > max_pr_count/max_pr_per_sheet:
                break

    writer.save()


@views.route('/comments', methods=['POST'])
def get_comments():
    if request.method == 'POST':
        query = "repo:{} author:{} type:pr"
        data = g.search_issues(
            query=query,
            sort='created',
            order='desc'
        )
        return render_template('tag.html', data=data)

