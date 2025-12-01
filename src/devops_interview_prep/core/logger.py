import logging

def get_logger(verbose: bool = False):
    logger = logging.getLogger("devops_interview_prep")

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger