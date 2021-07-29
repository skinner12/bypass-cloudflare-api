from flask import Flask, jsonify, request
from logging.config import dictConfig
from flask_restx import abort
from scraper.cloudflare import BypassCloudflare
from pathlib import Path

import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
import re
from xvfbwrapper import Xvfb


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

from xvfbwrapper import Xvfb
vdisplay = Xvfb(width=800, height=1280)
vdisplay.start()

import undetected_chromedriver.v2 as uc

options = uc.ChromeOptions()
options.add_argument(f'--no-first-run --no-service-autorun --password-store=basic')
#options.user_data_dir = '{}/cloudflare-bypass/scraper'.format(Path.home())
options.user_data_dir = f'./tmp/test_undetected_chromedriver'
options.add_argument(f'--disable-gpu')
options.add_argument(f'--no-sandbox')
options.add_argument(f'--disable-dev-shm-usage')

# Proxy 
# print("Use proxy: {proxy}".format(proxy=proxy))
# if proxy:
#     options.add_argument('--proxy-server={proxy}'.format(proxy=proxy))

driver = uc.Chrome(
version_main=92,
options=options,
headless=False)

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


 
    with driver:
        driver.get(url)

    html = driver.page_source

    #vdisplay.stop()
    
    return jsonify({
        'url': url,
        'html': html
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)