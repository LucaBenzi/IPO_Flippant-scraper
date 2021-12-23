import pandas as pd
import requests
import selenium
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    filename='log/events.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)


def get_data():
    URL = 'https://cheaperthanguru.com/transactions'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    pictures_list = soup.find_all("img", class_="share__company-logo")
    companies = soup.find_all("div", class_="js-line-chart-click-container")
    hidden_comp = soup.find_all("div", class_="share-details")
    values = soup.find_all("p", class_="share__detail-element")
    guru = soup.find_all("a", class_="share__guru-link js-hover")
    days = soup.find_all("p", class_="share__muted-text share__muted-text--sell")
    new_holdings = soup.find_all("p", class_="share__muted-text-big")
    data = []

    logging.info(f"pictures_list {len(pictures_list)} elements")
    logging.info(f"companies {len(companies)} elements")
    logging.info(f"new_holdings {len(new_holdings)} elements: {new_holdings}")

    for c in pictures_list:
        logging.info(f"analyzing {c.get('src')} ")
        try:
            if requests.get(c.get('src')).text.count('Error'):
                company = companies.pop(0).find('img').get('alt')
                shares = values.pop(0).text
                holding = values.pop(0).text
                g = guru.pop(0).text.replace('\n','').replace(' ','')
                # d = days.pop(0).text.replace('\n','').replace(' ','')
                d = new_holdings.pop(0).text.replace('\n','').replace(' ','') # data evento
                b = new_holdings.pop(0).text.replace('\n','').replace(' ','') # cosa è successo
                logging.info(f"company {company}, shares {shares}, holding {holding}, guru {g}, date {d}, new holding {b} ")
                if b == 'Newholding':
                    data.append((company,shares,holding,g,d,b))
            else:
                try:
                    buttare = ""
                    buttare += companies.pop(0)
                    buttare += values.pop(0)
                    buttare += values.pop(0)
                    buttare += guru.pop(0)
                    buttare += new_holdings.pop(0)
                    buttare += new_holdings.pop(0)
                    buttare += days.pop(0)
                    buttare += '\n'
                    logging.info(f"aziende da buttare: {buttare}")
                except:
                    print("empty")
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e
    return data
