import argparse

from flask import Flask
from dbco import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ask')
def getRecentArticles():
    return 'Miaw'

def isProdEnvironment():
   '''
   Read the mode from command line flags.
   
   Returns True if flag prod is set, False otherwise.
   '''
   parser = argparse.ArgumentParser(description='Flags for API server.')
   parser.add_argument('prod', type=bool, nargs=1, default=False)
   args = parser.parse_args()
   return args.prod

def main():
    if isProdEnvironment():
        app.run(host='0.0.0.0', port=80)
    else:
        app.run()
   
if __name__ == '__main__':
    main()
