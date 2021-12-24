import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import logging
from pandas.testing import assert_frame_equal

logging.basicConfig(
    filename='log/events.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)


def check_new_companies(data):
    """
    checks if websites contains new companies
    :param data: list of touple
    :return: Boolean: True if new companies available
    """
    old_companies = pd.read_csv("companies.csv")
    df = touples_to_dataframe(data).drop('Current Price', axis=1)
    df.to_csv("companies.csv", index=False)
    logging.info(f"old companies: \n{old_companies}")
    logging.info(f"new companies: \n{df}")
    if not df.equals(old_companies):
        logging.info(f"found new companies")
        return True
    else:
        logging.info(f"no companies")
        return False


def send_mail(data):
    """
    :param data: must be a list of touple
    :return:
    """
    sender_email = "btmercati@gmail.com"
    receiver_email = get_receivers_address()
    password = 'DE_$%5#*Ee'
    logging.info(f"sender_email: {sender_email} - receiver_email: {receiver_email} ")
    message = create_message(sender_email, receiver_email, data)
    send_mail_ssl(message, password)


def create_message(sender_email, receiver_email, data):
    """
    :param sender_email: string
    :param receiver_email: list of strings
    :param data: list of touple
    :return: message suitable for email: email.mime.multipart.MIMEMultipart
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = "INVESTITORI IPO"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    html = '<html>' + '\n' + '<head>' + get_table_style()
    html = html + touples_to_dataframe(data).to_html().replace('\n', '')
    html = html.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" id="customers">')
    html = '<!DOCTYPE html>' + html + '</html>'
    body = MIMEText(html, "html")
    message.attach(body)
    return message


def send_mail_ssl(message, password):
    """
    :param message: message suitable for email (contains sender and receivers): email.mime.multipart.MIMEMultipart
    :param password: string
    :return:
    """
    port = 465  # For SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            logging.info(f"login into mail account")
            server.login(message["From"], password)
            logging.info(f"login OK")
        except Exception as e:
            logging.error(e, exc_info=True)
        try:
            logging.info(f"sending mail")
            server.sendmail(message["From"], message["To"].split(","), message.as_string())
            logging.info(f"mail sent with the following message: {message.as_string()}")
        except Exception as e:
            logging.error(e, exc_info=True)


def touples_to_dataframe(tuple):
    """
    :param tuple: list of touple, first touple must contains the columns name
    :return: dataframe
    """
    return pd.DataFrame(tuple[1:], columns=tuple[0])


def get_receivers_address():
    """
    return a list of receivers stored in receivers.txt file.
    receivers mails must be separated with ',' without spaces
    :return: list of strings
    """
    try:
        receivers = open("receivers.txt", "r").read().split(",")
    except Exception as e:
        logging.info(f"Error reading receivers addresses: {e}")
        receivers = ["luca.benzi.92@gmail.com","david.taraschi@gmail.com"]
    logging.info(f"receivers: {receivers}")
    return receivers


def get_table_style():
    """
    get table style from css file
    :return: string for table style
    """
    with open('static/table_style.css', 'r') as file:
        css = file.read()
    return '<style>\n' + css + '</style>'
