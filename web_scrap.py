from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import time



class Scrapping():
    def __init__(self):
        self.urls = {'even3': 'https://www.even3.com.br/eventos',
                     'sympla': 'https://www.sympla.com.br/eventos/aprender'}
        self.webdriver = webdriver
        self.firefox_options = webdriver.FirefoxOptions()

    def initBrowser(self, host_ip):
        GECKODRIVER_PATH = '/usr/local/bin/geckodriver'
        FIREFOX_BIN = '/usr/bin/firefox'
        FIREFOX_BIN = '/app/vendor/firefox/firefox'
        GECKODRIVER_PATH = '/app/vendor/geckodriver/geckodriver'
        LD_LIBRARY_PATH = '/usr/local/lib:/usr/lib:/lib:/app/vendor'
        PATH = '/usr/local/bin:/usr/bin:/bin:/app/vendor/'        
    
        self.firefox_options.binary_location = FIREFOX_BIN
        self.firefox_options.add_argument('--desable-gpu')
        self.firefox_options.add_argument('--no-sandbox')
        self.firefox_options.add_argument('--headless')
        self.browser = self.webdriver.Firefox(executable_path=GECKODRIVER_PATH, firefox_options=self.firefox_options)
        print(f"Host :{self.browser.command_executor._url} \nSession_id: {self.webdriver.session_id}")
        return self.browser

    def webScrap(self, site):
        initial = time.clock_gettime(1)
        i = 0
        while (i <= 30):
            try:
                self.browser.get(self.urls[site])
            except WebDriverException as exception:
                print(f"WebDriverException: {exception}.")
            if site == 'even3':              
                # Using BeatifulSoup
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                event_collection = soup.select('div[ng-controller=EventosCtrl] > div.container > div > div.row')[1] \
                    .select('div.col-md-4')  # Scrapping of card events from site
                events = []  # List of events

                for item in event_collection:
                    heading = item.find('div', attrs={'class': 'panel-heading'})
                    body = item.find('div', attrs={'class': 'panel-body'})

                    a = heading.find('a', attrs={'itemprop': 'url'}).find(
                        'img', attrs={'class': 'evento-image'})
                    description = body.find('p', attrs={'class': None}).find(
                        'hm-read').get('hmtext')
                    info_event = body.find('p', attrs={'class': 'evento-local'})
                    date_event = info_event.find(
                        attrs={'itemprop': 'startDate'}).get('content')
                    local_event2 = info_event.find(attrs={'itemprop': 'location'}).find(
                        attrs={'itemprop': 'address'})

                    title_event = a.get('alt')
                    image_event = a.get('ng-src')
                    # local_event = info_event.find(attrs={'itemprop':'location'}).find(attrs={'itemprop':'name'}).get_text() # To get more accurate data, use the code below;
                    address = {}
                    # {'street': local_event2.find('span', attrs={'itemprop':'streetAddress'}).get_text(),
                    #             'city':local_event2.find('span', attrs={'itemprop':'streetLocality'}).get_text(),
                    #             'state': local_event2.find('span', attrs={'itemprop':'streetRegion'}).get_text(),
                    #             'coutry': local_event2.find('span', attrs={'itemprop':'streetCountry'}).get_text()
                    #             }

                    event = {'even3': {'title': title_event,
                                    'img': image_event,
                                    'description': description,
                                    'date': date_event,
                                    'address': address
                                    }}
                    events.append(event)
                    break

                final = time.clock_gettime(1) - initial
                print('Tempo decorrido: ' + str(final))
                return events

            if site == 'sympla':
                self.browser.get(self.urls[site])
                soup = BeautifulSoup(self.browser.page_source, 'lxml')

                events = soup.select('title')
                for item in events:
                    title_page = item.get_text()
                    print(title_page)
                    break
                    return title_page
            i+=1
            print(i)

    def quit_browser(self):
        self.browser.close()
        self.browser.quit()




