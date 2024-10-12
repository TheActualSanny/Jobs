import string
import logging
import json
from services.logging_config import logger

class Find_Jobs():
    def load_jobs(self):
        '''Loads the jobs.json file.'''
        try:
            with open('jobs.json', 'r') as file:
                loaded_lobs = json.load(file)
                return loaded_lobs
        except (FileNotFoundError, json.JSONDecodeError):
            logger.exception('Exception caught, please check the data again.')
            return None
        
    def search_jobs(self, user_input):
        lowercase_input = user_input.lower()
        initial_jobs = self.load_jobs()
        found_jobs = [] # The jobs that were found based on the user input will be stored here. It will be passed to a module in the db folder

        if initial_jobs:
            for job in initial_jobs:
                lower_position = job['position'].lower()
                if lowercase_input in lower_position:
                    found_jobs.append(job)
        return found_jobs
                