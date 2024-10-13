import scrapy

class QuantoriJobSpider(scrapy.Spider):
    name = "quantori_jobs"
    allowed_domains = ["career.quantori.com"]
    start_urls = ["https://career.quantori.com/positions"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"playwright": True}  
            )

    def parse(self, response):
        job_cards = response.xpath("//div[contains(@class, 'VacancyCardWide_card__qASWF card')]")
        
        for job in job_cards:
            yield {
                "title": job.xpath(".//div[contains(@class, 'VacancyCardWide_title__MmNNm')]/text()").get(),
                "location": job.xpath(".//div[contains(@class, 'VacancyCardWide_location__7ETnZ')]/small[1]/text()").get(),
                "link": response.urljoin(job.xpath(".//ancestor::a[1]/@href").get())
            }

        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={"playwright": True})
