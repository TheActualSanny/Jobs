import scrapy

class HrGeSpider(scrapy.Spider):
    name = "hr_ge"
    allowed_domains = ["hr.ge"]
    start_urls = [
        "https://www.hr.ge/search-posting?l=%5B%222%22,%2211%22%5D&c=%5B%22215%22,%22228%22,%22216%22,%22233%22,%22217%22,%22232%22,%22218%22,%22230%22,%22219%22,%22236%22,%22220%22,%22226%22,%22642%22,%22221%22,%22235%22,%22231%22,%22222%22,%22223%22,%22646%22,%22238%22,%22237%22,%22234%22,%22224%22,%22225%22,%22227%22,%22239%22,%22229%22%5D"
    ]
    
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={'User-Agent': self.custom_user_agent}
            )

    def parse(self, response):
        seen_jobs = set()  
        for job in response.css('div.ann div.ng-star-inserted'):
            
            title = job.css('div.title__text::text').get()
            link = job.css('a.title::attr(href)').get()
            location = job.css('div.location::text').get()
            work_from_home = bool(job.css('svg-icon[title="Work from home"]'))
            
            if title and link:
                title = title.strip()
                link = response.urljoin(link)
                
                if link not in seen_jobs:
                    seen_jobs.add(link)
                    yield {
                        'title': title,
                        'location': location.strip() if location else "Not specified",
                        'work_from_home': work_from_home,
                        'link': link,
                    }

        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse, headers={'User-Agent': self.custom_user_agent})
