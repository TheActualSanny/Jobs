import scrapy
import json
from jobsge.items import JobsgeItem

class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["jobs.ge"]
    start_urls = ['https://jobs.ge/en/?page=1&q=&cid=6&lid=&jid=']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 5,  
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    fetched_jobs_file = 'fetched_jobs.json'
    
    last_fetched_job_file = 'last_fetched_job.json'

    def load_last_fetched_job(self):
        try:
            with open(self.last_fetched_job_file, 'r') as file:
                self.log(f"Loading last fetched job from {self.last_fetched_job_file}")
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.log(f"No valid last fetched job file found, starting fresh.")
            return None

    def save_last_fetched_job(self, last_job_link):
        with open(self.last_fetched_job_file, 'w') as file:
            json.dump(last_job_link, file)
        self.log(f"Saved last fetched job: {last_job_link}")

    def parse(self, response):
        last_fetched_job = self.load_last_fetched_job()

        if response.status == 200:
            rows = response.xpath('//div[@class="regularEntries"]//table[@id="job_list_table"]/tr')[1:]

            new_last_fetched_job = None
            for row in rows:
                job_data = {
                    "position": row.xpath('td[2]/a/text()').get(default='').strip(),
                    "company": row.xpath('td[4]/a/text()').get(default='').strip(),
                    "published_date": row.xpath('td[5]/text()').get(default='').strip(),
                    "deadline": row.xpath('td[6]/text()').get(default='').strip(),
                    "details_link": response.urljoin(row.xpath('td[2]/a/@href').get())
                }

                if last_fetched_job and job_data == last_fetched_job:
                    self.log(f"Reached last fetched job: {job_data}. Stopping.")
                    break

                if not new_last_fetched_job:
                    new_last_fetched_job = job_data

                jobsge_item = JobsgeItem(
                    position=job_data['position'],
                    company=job_data['company'],
                    published_date=job_data['published_date'],
                    deadline=job_data['deadline'],
                    details_link=job_data['details_link']
                )

                yield jobsge_item
                self.log(f"Fetched job: {job_data['details_link']}")

            if new_last_fetched_job:
                self.save_last_fetched_job(new_last_fetched_job)
                self.log(f"New last fetched job: {new_last_fetched_job}")