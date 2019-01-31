from flask import Flask
from github import Github
from views import views as views_blueprint

DEBUG = True

# setup github token
g = Github(login_or_token="github-token")

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)


if __name__ == '__main__':
    app.register_blueprint(views_blueprint, url_prefix='/')
    app.run(debug=True)
