import mail
import scraper
import logging, logging.config

# logging.basicConfig(
#     filename='log/events.log',
#     level=logging.INFO,
#     format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
#     datefmt='%d-%m-%Y %H:%M:%S',
# )


def IPO_Fillant():
    """Check if there are some new available companies in the list of big investors.
    If so notifies customers by email"""
    try:
        logger.info('Getting data from web...')
        data = scraper.get_data()
        logger.info('checking new companies...')
        if mail.check_new_companies(data):
            logger.info('sending mail...')
            mail.send_mail(data)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e

if __name__ == '__main__':
    logging.config.fileConfig('log/log_config.ini', defaults={'logfilename': 'log/events.log'})
    logger = logging.getLogger('sampleLogger')
    logger.info(f"-----------------PGM-STARTED---------------------")
    IPO_Fillant()
    logger.info(f"-----------------PGM-ENDED---------------------\n\n")
