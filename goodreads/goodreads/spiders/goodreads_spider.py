from scrapy import Spider, Request
from goodreads.items import GoodreadsItem

import re

class GoodreadsSpider(Spider):
	name = 'goodreads_spider'
	allowed_url = ['https://www.goodreads.com/']
	start_urls = ['https://www.goodreads.com/book/popular_by_date/{}/'.format(x) for x in range(1980,2018)]

	#These are tests
	#start_urls = ['https://www.goodreads.com/book/popular_by_date/2012/']
	#start_urls = [('https://www.goodreads.com/book/popular_by_date/' + 
	#i + '/' ) for i in range(1980,2018)]

	


	def parse(self, response):
		# this doesn't work title_links = response.xpath('//span[@itemprop="name"]')
		# this works 
		#title_links = ['/book/show/7869.The_Bourne_Identity']
		#linkslist = []
		title_links = response.xpath('//a[@class="bookTitle"]/@href').extract()
		title_links = ['https://www.goodreads.com' + title_link for title_link in title_links]
		#for i in range(0, len(title_links)-196):
		#	linkslist.append(title_links[i].get_attribute())
		# unecessary title_url = response.xpath(['http://www.goodreads.com' + x for x in title_links])
		for url in title_links:
			#links = ['https://www.goodreads.com/book/popular_by_date/{}/'.format(x) for x in range(1980,2018)]
			yield Request(url = url, callback = self.parse_book_info)


	def parse_book_info(self, response):

		title = response.xpath('//h1[@id="bookTitle"]/text()').extract_first()
		title = re.sub('[\n]', '', title)
		title = title.strip()
		
		author = response.xpath('//span[@itemprop="name"]/text()').extract_first()
		
		avgrating = response.xpath('//span[@class="average"]/text()').extract_first()
		
		count_per_stars = response.xpath('//script[@type="text/javascript+protovis"]/text()').extract_first()
		count_per_stars = count_per_stars.split('renderRatingGraph([')
		count_per_stars = count_per_stars[1].split(']);')
		count_per_stars = count_per_stars[0].split(', ')
		five_stars = count_per_stars[0]
		four_stars = count_per_stars[1]
		three_stars = count_per_stars[2]
		two_stars = count_per_stars[3]
		one_stars = count_per_stars[4]
		
		totalratings = response.xpath('//span[@class="votes value-title"]/text()').extract_first()
		totalratings = re.sub('[\n]', '', totalratings)
		totalratings = totalratings.strip()

		totalreviews = response.xpath('//span[@class="count value-title"]/text()').extract_first()
		totalreviews = re.sub('[\n]', '', totalreviews)
		totalreviews = totalreviews.strip()

		if (response.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()').extract_first() == 'Favorites'):
			genre = response.xpath('//html//div[@class="stacked"]//div[@class="bigBoxBody"]//div[2]/div[1]/a[1]/text()').extract_first()
		else:
			genre = response.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()').extract_first()

		numpages = response.xpath('//span[@itemprop="numberOfPages"]/text()').extract_first()
		numpages = numpages.split()
		numpages = numpages[0]
		
		publisher = response.xpath('//html//div[@id="details"]/div[2]/text()').extract_first()
		publisher = publisher.split('by ')
		publisher = publisher[1].strip()
		# publisher = re.sub('[\n]', '', publisher)
		# publisher = publisher.strip()
		
		try:
			origpubdate = response.xpath('//nobr[@class="greyText"]/text()').extract_first()
			bad_chars = '(){}<>'
			origpubdate = re.sub('[\n]', '', origpubdate)
			origpubdate = origpubdate.strip()
			rgx = re.compile('[%s]' % bad_chars)
			origpubdate = rgx.sub('', origpubdate)
			origpubdate = origpubdate.split('published ')
			origpubdate = origpubdate[1]
			print(origpubdate)
		except:
			origpubdate = ''

		pubdate = response.xpath('//html//div[@id="details"]/div[2]/text()').extract_first()
		pubdate = pubdate.strip()
		pubdate = pubdate.strip(' ')
		pubdate = pubdate.split('by')
		pubdate = pubdate[0].split('Published')
		pubdate = pubdate[1].strip()

		try:
			awards = response.xpath('//html//div[@class="leftContainer"]//div[7]/div[2]/a[@class="award"]/text()').extract()
		except:
			awards = ''

		item = GoodreadsItem()
		item['title'] = title
		item['author'] = author
		item['avgrating'] = avgrating
		item['five_stars'] = five_stars
		item['four_stars'] = four_stars
		item['three_stars'] = three_stars
		item['two_stars'] = two_stars
		item['one_stars'] = one_stars
		item['totalratings'] = totalratings
		item['totalreviews'] = totalreviews
		item['genre'] = genre
		item['numpages'] = numpages
		item['publisher'] = publisher
		item['pubdate'] = pubdate
		item['origpubdate'] = origpubdate
		item['awards'] = awards



		yield item