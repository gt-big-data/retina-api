from flask import Flask
from dbco import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ask')
def getRecentArticles():
	return 'Miaw'

if __name__ == '__main__':
    app.run()
