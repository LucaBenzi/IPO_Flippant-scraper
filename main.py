import schedule
import time
import mail
import scraper
import logging, logging.config

logging.config.fileConfig('log/log_config.ini', defaults={'logfilename': 'log/events.log'})
logger = logging.getLogger('sampleLogger')

def IPO_Fillant():
    try:
        logger.info(f"-----------------PGM-STARTED---------------------")
        data = scraper.get_data()
        if mail.check_new_companies(data):
            mail.send_mail(data)
        print('Pgm end')
        logger.info(f"-----------------PGM-ENDED---------------------\n\n")
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e


if __name__ == '__main__':
    schedule.every().day.at("11:00").do(IPO_Fillant)
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute

