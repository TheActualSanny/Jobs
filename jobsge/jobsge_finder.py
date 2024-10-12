import string
import logging
import json
from utils.logging_config import logger

class FindJobs:
    def __init__(self, file_path='jobs.json'):
        self.file_path = file_path
        
    def load_jobs(self):
        '''Loads the jobs.json file.'''
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error("File not found: Ensure '%s' exists.", self.file_path)
        except json.JSONDecodeError:
            logger.error("JSON decoding error: Check the file format of '%s'.", self.file_path)
        return None           
        
    def search_jobs(self, user_input):
        """Searches for jobs matching the user input within the job's position field."""
        initial_jobs = self.load_jobs()

        if initial_jobs:
            lowercase_input = user_input.lower()
            found_jobs = [job for job in initial_jobs if lowercase_input in job['position'].lower()]
            
        return found_jobs
    