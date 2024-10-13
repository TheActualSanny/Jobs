import logging

logger = logging.Logger('Job_Searcher')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream = logging.StreamHandler()

stream.setFormatter(formatter)
logger.addHandler(stream)

