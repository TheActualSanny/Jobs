import scrapy
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

    def parse(self, response):
        if response.status == 200:
            rows = response.xpath('//div[@class="regularEntries"]//table[@id="job_list_table"]/tr')[1:]

            for row in rows:
                jobsge_item = JobsgeItem() 
                jobsge_item['position'] = row.xpath('td[2]/a/text()').get(default='').strip()
                jobsge_item['company'] = row.xpath('td[4]/a/text()').get(default='').strip()
                jobsge_item['published_date'] = row.xpath('td[5]/text()').get(default='').strip()
                jobsge_item['deadline'] = row.xpath('td[6]/text()').get(default='').strip()
                jobsge_item['details_link'] = response.urljoin(row.xpath('td[2]/a/@href').get())
                
                yield jobsge_item  
