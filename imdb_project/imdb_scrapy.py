import scrapy
import os
from selenium import webdriver



class MovieSpider(scrapy.Spider):
    name = 'imdb_movies'
    #selenium stuff
    chromedriver = "/Applications/chromedriver" # location of chrome driver
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    #custom
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.imdb.com/search/title?sort=boxoffice_gross_us&title_type=feature&year=2007,2017',
    ]

    def parse(self, response):

        for href in (response.xpath('//h3[@class="lister-item-header"]/a/@href')
            .extract()):


            yield scrapy.Request(# parse individual movie
                url=response.urljoin(href),
                callback=self.parse_movie,
                meta={'url': href})



        next_url = (response.xpath('//a[@class="lister-page-next next-page"]/@href').extract()[0])

        yield scrapy.Request(
            url=response.urljoin(next_url),
            callback=self.parse,
        )


    def parse_movie(self, response):

        self.driver.get(response.url)

        url = response.request.meta['url']

        title = (response.xpath('//h1[@itemprop="name"]/text()').extract()[0]
            .replace('\xa0',''))

        releaseDate = (' '.join(response.xpath(
            '//div[@id="titleDetails"]/div[4]/text()[2]')
            .extract()[0].split()[0:3]))

        contentRating = (response.xpath('//div[@class="subtext"]/text()[2]')
            .extract()[0].strip())

        runTime = (response.xpath('//div[@class="txt-block"]/time/text()')
            .extract()[0].split()[0])

        genres = ([genre.strip() for genre in list(filter(lambda x : x!=' ',
            response.xpath('//div[@class="see-more inline canwrap"]/a/text()'
            ).extract()))])

        rating = (response.xpath('//div[@class="ratingValue"]/strong/span/text()')
            .extract()[0])

        numReviews = (response.xpath('//span[@class="small"]/text()')
            .extract()[0].replace(",", ""))

        # website has non consistent layout
        if len(response.xpath('//div[@id="titleDetails"]/div/h4').extract()) > 13:

            prodBudget = (response.xpath('//div[@id="titleDetails"]/div[7]/text()')
                .extract()[1].strip().replace('$','').replace(',',''))

            openingWeekend = (response.xpath('//div[@id="titleDetails"]/div[8]/text()')
                .extract()[1].strip().replace('$','').replace(',','').split()[0])

            gross = (response.xpath('//div[@id="titleDetails"]/div[9]/text()')
                .extract()[1].strip().replace('$','').replace(',','').split()[0])

        else:

            prodBudget = (response.xpath('//div[@id="titleDetails"]/div[6]/text()')
                .extract()[1].strip().replace('$','').replace(',',''))

            openingWeekend = (response.xpath('//div[@id="titleDetails"]/div[7]/text()')
                .extract()[1].strip().replace('$','').replace(',','').split()[0])

            gross = (response.xpath('//div[@id="titleDetails"]/div[8]/text()')
                .extract()[1].strip().replace('$','').replace(',','').split()[0])

        self.driver.switch_to.frame("iframe_like")
        fbLikes = (self.driver.find_element_by_xpath('//span[@id="u_0_2"]').text.split()[0]
            .replace('K','000').replace('.',''))


        yield {
            'url': url,
            'title': title,
            'releaseDate': releaseDate,
            'contentRating': contentRating,
            'runTime': runTime,
            'rating': rating,
            'genres': genres,
            'numReviews': numReviews,
            'prodBudget': prodBudget,
            'openingWeekend': openingWeekend,
            'gross': gross,
            'fbLikes': fbLikes,
            }
