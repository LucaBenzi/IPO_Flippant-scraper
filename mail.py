import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import logging

logger = logging.getLogger('sampleLogger')

def check_new_companies(data):
    """
    checks if websites contains new companies
    :param data: list of touple
    :return: Boolean: True if new companies available
    """
    old_companies = pd.read_csv("companies.csv")
    df = touples_to_dataframe(data).drop('Current Price', axis=1)
    df.to_csv("companies.csv", index=False)
    logger.info(f"old companies: \n{old_companies}")
    logger.info(f"new companies: \n{df}")
    if len(df) != 0:    # Se non ci sono aziende nella lista ritorna zero, altrimenti guarda la prima riga
        if not df.iloc[0].equals(old_companies.iloc[0]):
            logger.info(f"found new companies")
            return True
        else:
            logger.info(f"no companies")
            return False
    else:
        return False


def send_mail(data):
    """
    :param data: must be a list of touple
    :return:
    """
    sender_email = "btmercati@gmail.com"
    receiver_email = get_receivers_address()
    password = 'DE_$%5#*Ee'
    logger.info(f"sender_email: {sender_email} - receiver_email: {receiver_email} ")
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
    #todo: gestire l'ìnsieme dei caratteri in modo che si possano usare le lettere accentate nella mail.

    html = get_mail_html()
    css = get_table_style()
    table = get_table(data)
    html = html.replace('Style Here',css)
    html = html.replace('Table Here', table)
    # html = '<html>\n' + '<head>' + '\n<meta http-equiv="Content-Type" content="text/html charset=UTF-8" />\n' + get_table_style() + '</head>'
    # html = html + '<body>' + touples_to_dataframe(data).to_html().replace('\n', '') + '</body>'
    # html = html.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" id="customers">')
    # html = '<!DOCTYPE html>\n' + html + '\n</html>'
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
            logger.info(f"login into mail account")
            server.login(message["From"], password)
            logger.info(f"login OK")
        except Exception as e:
            logger.error(e, exc_info=True)
        try:
            logger.info(f"sending mail")
            server.sendmail(message["From"], message["To"].split(","), message.as_string())
            logger.info(f"mail sent with the following message: \n{message.as_string()}")
        except Exception as e:
            logger.error(e, exc_info=True)


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
        logger.info(f"Error reading receivers addresses: {e}")
        receivers = ["luca.benzi.92@gmail.com","david.taraschi@gmail.com"]
    logger.info(f"receivers: {receivers}")
    return receivers


def get_mail_html():
    """
    get mail structure from html file
    :return: string for html structure
    """
    with open('static/mail.html', 'r') as file:
        mail_html = file.read()
    return mail_html


def get_table_style():
    """
    get table style from css file
    :return: string for table style
    """
    with open('static/table_style.css', 'r') as file:
        css = file.read()
    return css

def get_table(data):
    table = touples_to_dataframe(data).to_html()
    table = table.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" id="customers">')
    return table
