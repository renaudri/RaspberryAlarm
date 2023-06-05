import logging
logger = logging.getLogger('app_logger')

class LoggingConfig():
    @staticmethod
    def configureLogging():
        print("configure logger")

        formatter = logging.Formatter('%(asctime)s %(message)s')

        logger.setLevel(logging.INFO)

        fh = logging.FileHandler('logs/applog.log', mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
