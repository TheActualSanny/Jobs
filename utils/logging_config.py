'''Initializing the logger which is used in the job searching process.'''
import logging

logger = logging.Logger('Job_Searcher')
formatter = logging.Formatter('%(asctime)s - %(message)s')
stream = logging.StreamHandler()
stream.setFormatter(formatter)
logger.addHandler(stream)

