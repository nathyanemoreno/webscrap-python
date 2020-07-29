from flask import Flask, jsonify
import requests
import socket
from web_scrap import Scrapping

app = Flask(__name__)

try:
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name)
    print(host_ip)
except:
    print("Unable to get Hostname and IP")


@app.route('/')
def index():    
    scrapInstace = Scrapping()
    browser = scrapInstace.initBrowser(host_ip)
    print(browser.session_id)
    return 'OI'


@app.route('/scrap', methods=['GET', 'POST'])
def web_scrap():
    scrapInstace = Scrapping()
    scrapInstace.initBrowser(host_ip)
    data = jsonify(scrapInstace.webScrap('even3'))
    # json = jsonify(webScrap('sympla'))
    scrapInstace.quit_browser()
    return data


if __name__ == "__main__":
    app.run(debug=True)
    
