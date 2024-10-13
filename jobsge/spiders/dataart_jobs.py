import scrapy
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod

class DataArtJobSpider(scrapy.Spider):
    name = "dataart_jobs"
    allowed_domains = ["dataart.team"]
    start_urls = ["https://www.dataart.team/vacancies?countries=5742"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler"
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,  
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".VacancyCard-Link") 
                ],
            },
            callback=self.parse
        )

    async def parse(self, response):
        page = response.meta.get("playwright_page") 
        if not page:
            self.logger.error("No Playwright page found in response meta.")
            return

        content = await page.content() 
        await page.close()  

        sel = Selector(text=content)
        job_links = sel.css(".VacancyCard-Link::attr(href)").getall()

        for job_link in job_links:
            yield {
                "job_link": response.urljoin(job_link)
            }

        # Handle pagination for additional jobs if "Show 10 more" button exists
        next_button = sel.css("button:contains('Show 10 more')")
        if next_button:
            yield scrapy.Request(
                url=response.url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("click", "button:contains('Show 10 more')"),
                        PageMethod("wait_for_selector", ".VacancyCard-Link")
                    ],
                },
                callback=self.parse
            )
