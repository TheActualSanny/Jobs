'''This module contains the Manage_Jobs class which not only writes the found jobs into the table, but it also fetches the selected ammount of jobs every
X minutes/hours to send back to the user VIA email.'''

import psycopg2
import os
import logging
from dotenv import load_dotenv
from utils.logging_config import logger
from db.db_connection import get_connection

load_dotenv()

class ManageJobs:
    def __init__(self):
        self.last_index = 0

    def select_query(self, conn, cur):
        '''Selects all of the columns'''
        with conn:
            cur.execute(f'SELECT * FROM {os.getenv('JOBS_TABLE')}')
            data = cur.fetchall()
        return data
    
    def create_jobs_table(self, conn, cur):
        '''Method that creates a table where the found jobs are stored.'''
        with conn:
            cur.execute(f'CREATE TABLE IF NOT EXISTS {os.getenv('JOBS_TABLE')}' + '''(
                        id SERIAL PRIMARY KEY,
                        position VARCHAR(50) NOT NULL,
                        company VARCHAR(50) NOT NULL,
                        published_date VARCHAR(30) NOT NULL,
                        deadline VARCHAR(30) NOT NULL,
                        details TEXT
                        )''')

        
    def insert_found_jobs(self, new_jobs):
        '''Inserts the recently received job offers into the '''
        conn = get_connection()
        cur = conn.cursor()
        self.create_jobs_table(conn, cur)

        for job in new_jobs:
            with conn:
                cur.execute(f'INSERT INTO {os.getenv('JOBS_TABLE')}(position, company, published_date, deadline, details)' + 
                            'VALUES(%s, %s, %s, %s, %s)', (job['position'], job['company'], job['published_date'], job['deadline'], 
                                                           job['details_link']))
        cur.close()
        conn.close()

    def fetch_jobs(self, job_ammount):
        '''Method which selects a certain ammount of job offers from the table.
           the data that this fetches will be sent to the email'''
        conn = get_connection()
        cur = conn.cursor() 
        finalized_jobs = []

        data = self.select_query(conn, cur)

        length = len(data)

        for elem in range(self.last_index, self.last_index + job_ammount):
            if elem == length:
                break
            finalized_jobs.append(data[elem])

        cur.close()
        conn.close()
        if self.last_index + job_ammount > length - 1:
            self.last_index = length - 1
        else:
            self.last_index += job_ammount
        return finalized_jobs

    def delete_jobs(self):
        '''Deletes the inserted jobs. This method will be called every time the user stops notifications'''
        conn = get_connection()
        cur = conn.cursor()

        with conn:
            cur.execute(f'DELETE FROM {os.getenv('JOBS_TABLE')}')
        cur.close()
        conn.close()

