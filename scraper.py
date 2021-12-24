import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    filename='log/events.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)


def get_data():
    """
    :return: list of touple of IPO bought from big investors
    """
    URL = 'https://cheaperthanguru.com/transactions'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table_row = soup.find_all("div",
                              class_="share__top-box-link js-hover-parent js-accordion js-line-chart-click-container")
    companies = []
    companies.append(('Company Name', 'Investor Price', 'Current Price', 'Investor','Action'))
    for t in table_row:
        picture_url = get_picture_url(t)
        if isIPO(picture_url) and get_action(t) == 'New holding':
            company = (get_company_name(t), get_guru_price(t), get_current_price(t), get_guru_name(t), get_action(t))
            logging.info(f"Found new company {company}")
            companies.append(company)
    return companies


def get_company_name(table_row):
    """returns the name of the company"""
    company_name = table_row.find_all("h4", class_="share__company-name")
    return company_name[0].text


def get_guru_price(table_row):
    """returns the price that investor paid for this company"""
    guru_price = table_row.find_all("div", class_="share share--avg-price")
    return guru_price[0].text.replace("Guru Buy Price","").replace("\n","").replace(" ","")


def get_current_price(table_row):
    """returns the actual price"""
    current_price = table_row.find_all("div", class_="share share--current-price")
    return current_price[0].text.replace("Current Price","").replace("\n","").replace(" ","")


def get_guru_name(table_row):
    """who performed the trade"""
    guru_name = table_row.find_all("a", class_="share__guru-link js-hover")
    return guru_name[0].text.replace("\n","").replace("  ","")


def get_action(table_row):
    """what investor did"""
    action = table_row.find_all("p",class_="share__muted-text share__muted-text-big")
    return action[0].text.replace("\n","").replace("  ","")


def get_picture_url(table_row):
    """get the url of the picture so we can discover if the company has a logo or not"""
    picture = table_row.find_all("img", class_="share__company-logo")
    return picture[0].get('src')


def isIPO(picture_url): # questa funzione sta tirando loggate assurde.
    """check if the company is a IPO by looking at the logo.
    If a company doesn't have a logo, classify it as IPO"""
    return not requests.get(picture_url).ok
