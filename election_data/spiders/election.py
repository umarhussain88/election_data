import scrapy
import logging
from datetime import datetime
from pathlib import Path


class ElectionSpider(scrapy.Spider):
    name = 'election'
    allowed_domains = ['elezionistorico.interno.gov.it']
    start_urls = ['https://elezionistorico.interno.gov.it/index.php?tpel=R']
    parent_url = 'http://elezionistorico.interno.gov.it'

    log_dir = Path(__file__).parent.parent.joinpath('logs')
    if not log_dir.is_dir():
        log_dir.mkdir(parents=True) 


    logging.basicConfig(
        filename=log_dir.joinpath(f"{datetime.now().strftime('%d%m%y_%H%M%S')}_log.txt"),
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.WARNING
    )

    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    }

    @staticmethod
    def ignore_index_errors(data,n):
        try:
            return data[n]
        except IndexError:
            return None


    def parse(self,response): #dates.
        dates = response.xpath('//div[@class="sezione_ristretta"]/ul/li')

        for item in dates:

            yield scrapy.Request(
                self.parent_url + item.xpath('a/@href').extract()[0].replace('/?','?') + '&tpa=I&tpe=A&lev0=0&levsut0=0&es0=S&ms=N',
                callback=self.parse_region,headers=self.headers)                          # ^ date + regional level



    def parse_region(self,response):

        regions = response.xpath('//div[@id="collapseFour"]/div/div/ul/li')
        for region in regions:
            yield scrapy.Request(self.parent_url + region.xpath('a/@href').extract()[0],
            callback=self.parse_district, meta={'region' : region.xpath('a/text()').extract()[0]},headers=self.headers)


    def parse_district(self,response):
        districts = response.xpath('//div[@class="panel-collapse collapse in"]/div/div/ul/li')
        for district in districts:
            yield scrapy.Request(self.parent_url + district.xpath('a/@href').extract()[0],callback=self.parse_towns,
                                meta={'district' : district.xpath('a/text()').extract()[0],
                                    'region' : response.meta['region']
                                    })

    def parse_towns(self,response):

        town = response.xpath('//tbody/tr/th')
        for link in town:
            try:
                yield scrapy.Request(self.parent_url + '/' +  link.xpath('a/@href').extract()[0],
                callback=self.electoral_data, meta={'area' : link.xpath('a/text()').extract()[0],
                                                    'region' : response.meta['region'],
                                                    'district' : response.meta['district']
                                                     },headers=self.headers)
            except IndexError:
                pass
            

    def electoral_data(self,response):

        table = response.xpath('//tr')
        for items in table[1:]:
        

            yield { 

                'Candidati' : self.ignore_index_errors(items.xpath('th/text()').extract(),n=0),
                'Data di nascita' : self.ignore_index_errors(items.xpath('td/text()').extract(),n=0),
                'Luogo di nascita' : self.ignore_index_errors(items.xpath('td/text()').extract(),n=1),
                'Preferenze' : self.ignore_index_errors(items.xpath('td/text()').extract(),n=2),
                'Eletto' : self.ignore_index_errors(items.xpath('td/text()').extract(),n=3),
                'src_url' : response.url,
                'region' : response.meta['region'],
                'area' : response.meta['area'],
                'district' : response.meta['district'] 
            }