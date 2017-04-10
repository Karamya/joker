# @Author: ramya <ramya>
# @Date:   2017-03-22T10:02:46+01:00
# @Last modified by:   ramya
# @Last modified time: 2017-03-24T16:44:41+01:00

import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrap_jokes.items import ScrapJokesItem # ScrapJokesItem is the class we created in items.py
from scrapy.http import Request ## Request class enables us to recursively crawl a webpage
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector


class UnijokesSpider(Spider):
    name = "jokes" ### name of my spider
    allowed_domains = ["unijokes.com"] ## Optional. A list of domains for crawling. Anything not in this list will not be available for crawling
    start_urls = ["https://unijokes.com/%d/" %d for d in range(1, 1238)] ## list of urls, which will be the roots of later crawls

    def parse(self, response):
        jokes = response.xpath('//div[@class="joke"]')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.xpath("./text()").extract_first()
            item["ratingValue"] = joke.xpath(".//div[@class='panel']//b/span/text()").extract_first()
            if float(item["ratingValue"]) > 50:
                with open("urljokes.txt", "a") as f:
                    f.write(((item["joke"].replace("\r\n", " ")).replace("\n", " ")).replace("\'", "''") + "\r\t")
            yield item

class LaughFactory(Spider):
    name = "laughfactory"
    allowed_domains = ["www.laughfactory.com"]
    start_urls = ["http://www.laughfactory.com/jokes/popular-jokes/all-time/%d" %d for d in range(1, 300)]

    def parse(self, response):
        jokes = response.css('div.jokes')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.css("div.joke-text p").extract()
            item["likes"] = joke.css("a.like span::text").extract()
            item["dislikes"] = joke.css("a.dislike span::text").extract()
            score = int(item["likes"][0]) - int(item["dislikes"][0])
            if score > 50:
                print(joke)#, likes)
                joke = item["joke"][0][30: -5]
                with open("laughfactory.txt", "a") as f:
                    f.write((((joke.lstrip().rstrip()).replace("\n", " ")).replace("\r\t", "")).replace("\r", "").replace("<br>", ". ") + "\n")
            yield item

class OneLineFun(Spider):
    name = "onelinefun"
    allowed_domains = ["www.onelinefun.com"]
    start_urls = ["http://onelinefun.com/%d/" %d for d in range(1, 310)]

    def parse(self, response):
        jokes = response.css('div.oneliner')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.css("p::text").extract()
            item["ratingValue"] = joke.css("div.panel b::text").extract()
            rating = float(item["ratingValue"][0])
            if rating > 52:
                joke = item["joke"][0]
                with open("onelinefun.txt", 'a') as f:
                    f.write(joke.replace("\r\n", " ") + "\n")
            yield item


class JokeaDay(Spider):
    name = "ajokeaday"
    allowed_domains = ["www.ajokeaday.com"]  ### difficult to extract good jokes as ratings are not a reliable measure here
    start_urls = ["https://www.ajokeaday.com/jokes/best?pagenumber=%d" %d for d in range(1, 2206)]

    def parse(self, response):
        jokes = response.css('div.jd-body')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.css("p").extract()
            joke = item["joke"][0][3:-4]
            with open("ajokeaday.txt", 'a') as f:
                f.write(joke.replace("<br>", " ").replace("&amp;", "&").replace("\r", "") + "\n")
            yield item

class KickAssHumor(Spider):
    name = "kickasshumor"
    allowed_domains = ["www.kickasshumor.com"]  ### difficult to extract good jokes as ratings are not a reliable measure here
    start_urls = ["http://kickasshumor.com/all-time-best/4/funny-one-liner-jokes"]

    def parse(self, response):
        jokes = response.css('div.jokes')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.css("a::text").extract()
            joke = item["joke"][0]
            with open("kickasshumor.txt", 'a') as f:
                f.write(joke.replace("<br>", " ").replace("&amp;", "&").replace("\r", "") + "\n")
            yield item

class Funny2(CrawlSpider):
    name = "funny2"
    allowed_domains = ["http://funny2.com"]  ### difficult to extract good jokes as ratings are not a reliable measure here
    #start_urls = ['http://funny2.com/jokes.htm']
    start_urls = ['http://funny2.com/jokes%s.htm' % chr(s) for s in range(ord('a'), ord('o'))]

    def parse(self, response):
        jokes = response.xpath('.//*[@id="divMain"]/div[1]/text()[normalize-space()]')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.extract().strip().replace("\\", "")
            joke = item["joke"]
            with open("funny2.txt", 'a') as f:
                f.write(joke + "\n")
            yield item

class JokesoftheDay(Spider):  ### have some bugs in this. Work on it during your free time. 
    name = "jokesoftheday"
    allowed_domains = ["www.jokesoftheday.net"]  ### difficult to extract good jokes as ratings are not a reliable measure here
    start_urls = ["http://www.jokesoftheday.net/tag/short-jokes/%d" %d for d in range(1, 2)] #920

    def parse(self, response):
        jokes = response.xpath('//*/div[@class="jokeContent"]')
        for joke in jokes:
            item = ScrapJokesItem()
            item["joke"] = joke.xpath(".//h2/../text()[normalize-space()] | .//h2/../p").extract()
            joke = item["joke"][0]
            with open("jokesoftheday.txt", 'a') as f:
                f.write(joke)
            yield item
