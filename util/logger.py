import logging

INFO: int = logging.INFO
ERROR: int = logging.ERROR


def log(message: str, notifier_type: int, is_silent: bool = False) -> None:
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=INFO, filename='log.txt')

    if notifier_type == INFO:
        logging.info(message)
    elif notifier_type == ERROR:
        logging.error(message)

    if not is_silent:
        print(message)
