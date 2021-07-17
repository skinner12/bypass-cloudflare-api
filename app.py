from flask import Flask, jsonify, request
from logging.config import dictConfig
from flask_restx import abort
from scraper.cloudflare import BypassCloudflare
import re


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/html')
def html():
    url = request.args.get('url')
    proxy = request.args.get('proxy')

    # Check if param URL is present
    if not url:
        app.logger.error("Missing Parameter URL")
        abort(jsonify(message="Missing Parameter", error=400, status="error"), 400)

    # Check if param is a real url
    regex = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    if not re.search(regex, url):
        app.logger.error("Not real URL")
        abort(jsonify(message="Not a valid URL", error=400, status="error"), 400)
    cl = BypassCloudflare(url, proxy=proxy)
    html = cl.read_webpage()
    return jsonify({
        'url': url,
        'html': html
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)