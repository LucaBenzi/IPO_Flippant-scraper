import schedule
import time
import mail
import scraper
import logging

logging.basicConfig(
    filename='log/events.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)


def IPO_Fillant():
    try:
        print('Pgm started')
        data = scraper.get_data()
        if mail.check_new_companies(data):
            mail.send_mail(data)
        print('Pgm end')
    except Exception as e:
        logging.error(e, exc_info=True)
        raise e

if __name__ == '__main__':
    logging.info(f"-----------------PGM-STARTED---------------------")
    IPO_Fillant()
    logging.info(f"-----------------PGM-ENDED---------------------\n\n\n\n\n\n\n\n\n\n\n\n")

