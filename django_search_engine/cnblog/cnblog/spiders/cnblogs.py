import scrapy

from ..items import CnblogItem


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/legacy']

    def parse(self, response):
        divLst = response.xpath('//div[@id="post_list"]/div')
        item = CnblogItem()
        for div in divLst:
            item["post_date"] = div.xpath(".//div[@class='post_item_foot']/text()").extract()[1].strip().replace('发布于 ',
                                                                                                                 '')
            item["title"] = div.xpath(".//h3/a/text()").extract_first()
            item["title_link"] = div.xpath(".//h3/a/@href").extract_first()
            summary_lst = div.xpath(".//p[@class='post_item_summary']/text()").extract()
            if len(summary_lst) > 1:
                item["item_summary"] = summary_lst[1].strip()
            else:
                item["item_summary"] = summary_lst[0].strip()
            yield item
        nexturl = response.xpath('.//a[text()="Next >"]/@href').extract_first()

        if nexturl is not None:
            nexturl = 'https://www.cnblogs.com' + nexturl
            yield scrapy.Request(nexturl, callback=self.parse)

