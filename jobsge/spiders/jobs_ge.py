import scrapy
import json
from jobsge.items import JobsgeItem

# scrapy crawl jobs -o jobs.json

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
        """Load the last fetched job link from the JSON file."""
        try:
            with open(self.last_fetched_job_file, 'r') as file:
                self.log(f"Loading last fetched job from {self.last_fetched_job_file}")
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.log(f"No valid last fetched job file found, starting fresh.")
            return None

    def save_last_fetched_job(self, last_job_link):
        """Save the last fetched job link to the JSON file."""
        with open(self.last_fetched_job_file, 'w') as file:
            json.dump(last_job_link, file)
        self.log(f"Saved last fetched job: {last_job_link}")

    def parse(self, response):
        last_fetched_job = self.load_last_fetched_job()

        if response.status == 200:
            rows = response.xpath('//div[@class="regularEntries"]//table[@id="job_list_table"]/tr')[1:]

            new_last_fetched_job = None
            for row in rows:
                job_link = response.urljoin(row.xpath('td[2]/a/@href').get())

                # Stop parsing once we hit the last fetched job
                if job_link == last_fetched_job:
                    self.log(f"Reached last fetched job: {job_link}. Stopping.")
                    break

                # Set the first job as the new "last fetched job"
                if not new_last_fetched_job:
                    new_last_fetched_job = job_link

                # Collect job data
                jobsge_item = JobsgeItem(
                    position=row.xpath('td[2]/a/text()').get(default='').strip(),
                    company=row.xpath('td[4]/a/text()').get(default='').strip(),
                    published_date=row.xpath('td[5]/text()').get(default='').strip(),
                    deadline=row.xpath('td[6]/text()').get(default='').strip(),
                    details_link=job_link
                )

                yield jobsge_item  # Yield the job item for output
                self.log(f"Fetched job: {job_link}")

            # Save the new last fetched job link (if new jobs were fetched)
            if new_last_fetched_job:
                self.save_last_fetched_job(new_last_fetched_job)