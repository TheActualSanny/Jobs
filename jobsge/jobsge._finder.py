import string
import logging
import json
from utils.logging_config import logger

class FindJobs():
    def load_jobs(self):
        '''Loads the jobs.json file.'''
        try:
            with open('jobs.json', 'r') as file:
                loaded_jobs = json.load(file)
                return loaded_jobs
        except FileNotFoundError:
            logger.exception('The file was not found, please check if the name is written correctly.')
            return None
        except json.JSONDecodeError:
            logger.exception('Could not load the JSON data.')
            return None            
        
    def search_jobs(self, user_input):
        lowercase_input = user_input.lower()
        initial_jobs = self.load_jobs()

        if initial_jobs:
            found_jobs = [job for job in initial_jobs if lowercase_input in job['position'].lower()]# The jobs that were 
            # found based on the user input will be stored here. It will be passed to a module in the db folder
            
        return found_jobs
                