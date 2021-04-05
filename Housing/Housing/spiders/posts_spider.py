import scrapy
import re
start_url1 = []
for i in range(5200001,52000010):
        start_url1.append('https://ihome.ir/details-page/%i'%(i))

class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = start_url1
    

    def parse(self,response):
        
        for post, option in zip(response.xpath('//*[@id="__layout"]/div/div[1]/div/div[1]/div[2]/div'),response.xpath('//*[@id="__layout"]/div/div[1]/div/div[3]/div/div[2]')):
            is_for_sale = post.xpath('div[2]/h1/text()').extract()
            if 'فروش' in is_for_sale[0]:
                Zone = post.xpath('div[2]/h1/text()').extract()
                Zone = cleanTitle(Zone[0])
                
                price = post.xpath('div[3]/div/div[2]/strong/text()').extract()
                
                
                if post.xpath('div[4]/div[1]/div/div/span[1]/span/text()').extract() :
                    Years = post.xpath('div[4]/div[1]/div/div/span[1]/span/text()').extract()
                else:
                    Years = 0
            
                Rooms = post.xpath('div[4]/div[2]/div/div/span[1]/span/text()').extract()
                Rooms = int(Rooms[0])

                Area = post.xpath('div[4]/div[3]/div/div/span[1]/span/text()').extract()
                Area = int(Area[0])
                
            ## '//*[@id="__layout"]/div/div[1]/div/div[3]/div/div[2]/div[1]/span[2]'
            # further options
                NumberOfElevators = option.xpath('div[1]/span/text()').extract()
                # if NumberOfElevators is None:
                #     NumberOfElevators[0] = ['0']
                # NumberOfElevators = int(Rooms[0])
                
                floor = option.xpath('div[4]/span[1]/text()').extract()

                if floor[0] == '——' or floor[0] =='—':
                    floor = None
                    
                
                direction = option.xpath('div[5]/span[1]/text()').extract()

                direction = str(direction[0])
                if direction == '—':
                    direction = None
                yield{
                    'Zone':Zone,
                    'Price': price,
                    'Years' : Years,
                    'Rooms': Rooms,
                    'Area' : Area,
                    'NumberOfElevators': NumberOfElevators,
                    'floor': floor,
                    'direction':direction


                }
        

def cleanTitle(zone):
    title = zone   
    if 'متری' in str(title):
        title = title.split('متری')
        
    title[-1].replace('r\n            ','')
    new_title = ''
    if '-' in title[-1] :
        index = title[-1].index('-')
        for i in range(0,index):
            new_title = new_title+title[-1][i]
        title[-1] = new_title
    
    title = str(title[-1])
    return title


