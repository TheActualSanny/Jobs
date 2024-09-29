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
    
    def load_fetched_jobs(self):
        try:
            with open(self.fetched_jobs_file, 'r') as file:
                self.log(f"Loading fetched jobs from {self.fetched_jobs_file}")
                return set(json.load(file))
        except FileNotFoundError:
            self.log(f"No fetched jobs file found: {self.fetched_jobs_file}")
            return set()
        
    def save_fetched_jobs(self, fetched_jobs):
        with open(self.fetched_jobs_file, 'w') as file:
            json.dump(list(fetched_jobs), file)
        self.log(f"Saved fetched jobs to {self.fetched_jobs_file}")
    
    def parse(self, response):
        fetched_jobs = self.load_fetched_jobs()
        new_fetched_jobs = set()
        
        if response.status == 200:
            rows = response.xpath('//div[@class="regularEntries"]//table[@id="job_list_table"]/tr')[1:]

            for row in rows:
                jobsge_item = JobsgeItem() 
                job_link = response.urljoin(row.xpath('td[2]/a/@href').get())
                
                # Skip jobs already fetched
                if job_link in fetched_jobs:
                    self.log(f"Job already fetched: {job_link}")
                    continue
                
    
                jobsge_item = JobsgeItem(
                    position=row.xpath('td[2]/a/text()').get(default='').strip(),
                    company=row.xpath('td[4]/a/text()').get(default='').strip(),
                    published_date=row.xpath('td[5]/text()').get(default='').strip(),
                    deadline=row.xpath('td[6]/text()').get(default='').strip(),
                    details_link=job_link
                )

                yield jobsge_item  
                self.log(f"Fetched job: {job_link}")
                new_fetched_jobs.add(job_link)
            self.update_fetched_jobs(fetched_jobs, new_fetched_jobs)

    # Save new fetched jobs
    def update_fetched_jobs(self, fetched_jobs, new_fetched_jobs):
        if new_fetched_jobs:
            fetched_jobs.update(new_fetched_jobs)
            self.save_fetched_jobs(fetched_jobs)
            self.log(f"New jobs added: {len(new_fetched_jobs)}, Total fetched jobs: {len(fetched_jobs)}")
             
   