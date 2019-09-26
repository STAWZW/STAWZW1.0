import requests
from scrapy.selector import Selector
 
 
 
def crawl_ips():
    #爬取西刺的免费高匿IP代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
    re = requests.get("http://www.xicidaili.com/nn", headers = headers)
 
    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")
 
    for tr in all_trs[1:]:
        speed_str = tr.xpath('./td[2]/text()').extract()[0]
        print(speed_str)

crawl_ips()