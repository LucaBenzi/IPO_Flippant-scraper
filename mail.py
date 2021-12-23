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
    old_companies = pd.read_csv("companies.csv")
    df = data_to_html(data)
    df.to_csv("companies.csv", index=False)
    logging.info(f"old companies: \n{old_companies}")
    logging.info(f"new companies: \n{df}")
    if not df.equals(old_companies):
        logging.info(f"found new companies")
        return True
    else:
        logging.info(f"no companies")
        return False

def send_mail(data):    # data must be a list of touple
    sender_email = "btmercati@gmail.com"
    receiver_email = get_receivers_address()
    password = 'DE_$%5#*Ee'
    logging.info(f"sender_email: {sender_email} - receiver_email: {receiver_email} ")

    message = MIMEMultipart("alternative")
    message["Subject"] = "INVESTITORI IPO"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)

    html = '<html>' + css
    html = html + data_to_html(data).to_html().replace('\n', '')
    html = html.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" id="customers">')
    html = '<!DOCTYPE html>' + html + '</html>'
    print(html)
    body = MIMEText(html, "html")
    message.attach(body)

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            logging.info(f"login into mail account")
            server.login(sender_email, password)
            logging.info(f"login OK")
        except Exception as e:
            logging.error(e, exc_info=True)
        # TODO: Send email here
        try:
            logging.info(f"sending mail")
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info(f"mail sent with the following message: {message.as_string()}")
        except Exception as e:
            logging.error(e, exc_info=True)


def data_to_html(tuple):
    return pd.DataFrame(tuple[1:], columns=tuple[0])


def get_receivers_address():
    try:
        receivers = open("receivers.txt", "r").read().split(",")
    except Exception as e:
        logging.info(f"Error reading receivers addresses: {e}")
        receivers = ["luca.benzi.92@gmail.com","david.taraschi@gmail.com"]
    logging.info(f"receivers: {receivers}")
    return receivers

css = '''
<head>
<style>
#customers {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #ddd;}

#customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}
</style>
'''