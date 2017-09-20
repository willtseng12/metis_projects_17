import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from six.moves.urllib.parse import urljoin
from scrapy.utils.python import to_native_str

url_list = []

class NYTSpider(scrapy.Spider):
    name = 'NYTspider'
    
    handle_httpstatus_list = [301, 302]
    #custom
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True,
    }

    # retreiving the url list (both the original and additional)
    with open("nyt_urls.txt", "r") as urls:
        for url in urls:
            url_list.append(url)
    with open("nyt_urls_add.txt", "r") as urls:
        for url in urls:
            url_list.append(url)


    start_urls = url_list

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_article,
                                    errback=self.errback_httpbin,
                                    meta={'dont_redirect':False},
                                    dont_filter=True)

    # parsing

    def parse_article(self, response):

        self.logger.info("got response %d for %r" % (response.status, response.url))

        # handle redirection
        # this is copied/adapted from RedirectMiddleware
        if response.status >= 300 and response.status < 400:

            # HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
            location = to_native_str(response.headers['location'].decode('latin1'))

            # get the original request
            request = response.request

            # and the URL we got redirected to
            redirected_url = urljoin(request.url, location)

            if response.status == 301 or request.method == 'HEAD':
                redirected = request.replace(url=redirected_url, callback=self.parse_article,
                                             errback=self.errback_httpbin,)
                yield redirected
            

        p_tags = response.xpath('//p[@class="story-body-text story-content"]/text()')

        content = ' '

        # new version of NYT
        if p_tags != []:
            for i, p_tag in enumerate(p_tags):
                
                p_text = p_tag.extract().strip()
                
                try:
                    a_text = (response.xpath('//p[@class="story-body-text story-content"]/a/text()')
                        .extract()[i]
                        .strip())
                except IndexError:
                    a_text = ''
                
                if a_text != '':
                    content += p_text + ' ' + a_text + ' '
                else:
                    content += p_text + ' '

        # unhandled IndexError denote old version of NYT
        else:

            p_tags = response.xpath('//p[@itemprop="articleBody"]/text()')

            for i, p_tag in enumerate(p_tags):
                
                p_text = p_tag.extract().strip()
                
                try:
                    a_text = (response.xpath('//p[@itemprop="articleBody"]/a/text()')
                        .extract()[i]
                        .strip())
                except IndexError:
                    a_text = ''
                
                if a_text != '':
                    content += p_text + ' ' + a_text + ' '
                else:
                    content += p_text + ' '
            

        yield {'url' : response.request.url,
               'content' : content,
               }


    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response

            # just yield blank string
            yield {'content' : ' ',
                   'url' : response.request.url}
            self.logger.error('HttpError on %s', response.url)

