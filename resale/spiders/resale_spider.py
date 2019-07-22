from scrapy import Spider, Request
from resale.items import ResaleItem
import numpy as np
import re

class ResaleSpider(Spider):
	name = 'resale_spider'
	allowed_urls = ['https://www.cars.com/']

	# start_urls for Jeep Wrangler
	# start_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22306&mkId=20021&page=1&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001']

	# start_urls for Toyota Tacoma
	# start_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22250&mkId=20088&page=1&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001']

	# start_urls for Toyota Tundra
	# start_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22213&mkId=20088&page=1&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001']

	# start_urls for GMC Sierra
	# start_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22044&mkId=20061&page=1&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001']

	# start_urls for Toyota 4Runner
	# start_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=20482&mkId=20088&page=1&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001']

	# start_urls for Lincoln MKS
	start_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=21403&mkId=20025&page=1&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001']

	def parse(self, response):
		# the number of pages available for scraping is 50
		number_pages = 50

		# number of cars per page is 100
		cars_per_page = 100

		# List comprehension to construct all the urls
		# urls for Jeep Wrangler
		# result_urls = ['https://www.cars.com/for-sale/searchresults.action/?dealerType=all&mdId=22306&mkId=20021&page={}&perPage=100&prMn=2000&rd=99999&searchSource=GN_REFINEMENT&sort=relevance&stkTypId=28881&zc=10001'.format(x) for x in range(1,number_pages+1)]

		# urls for Toyota Tacoma
		# result_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22250&mkId=20088&page={}&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001'.format(x) for x in range(1,number_pages+1)]

		# urls for Toyota Tundra
		# result_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22213&mkId=20088&page={}&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001'.format(x) for x in range(1,number_pages+1)]

		# urls for GMC Sierra
		# result_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=22044&mkId=20061&page={}&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001'.format(x) for x in range(1,number_pages+1)]

		# urls for Toyota 4Runner
		# result_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=20482&mkId=20088&page={}&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001'.format(x) for x in range(1,number_pages+1)]

		# urls for Lincoln MKS
		result_urls = ['https://www.cars.com/for-sale/searchresults.action/?mdId=21403&mkId=20025&page={}&perPage=100&rd=99999&searchSource=NEW_SEARCH&sort=relevance&stkTypId=28881&zc=10001'.format(x) for x in range(1,number_pages+1)]


		# Yield the requests to different search result urls, 
		# using parse_result_page function to parse the response.
		for url in result_urls:
			#print(url)
			yield Request(url=url, callback=self.parse_result_page)
		#pass

	def parse_result_page(self, response):
		# This fucntion parses the search result page.
		
		# We are looking for url of the detail page.
		detail_urls = response.xpath('//div[@class="sku-title"]/h4/a/@href').extract()

		# car list block
		blocks = response.xpath('//*[@id="srp-listing-rows-container"]/div[@class="shop-srp-listings__listing-container"]')

		for block in blocks:

			# take care of the title
			title = block.xpath('.//h2[@class="listing-row__title"]/text()').extract_first().strip()

			# extract the year
			year = title[0:4]
			brand = 'Lincoln'
			model = 'MKS'

			# the configuration
			config = re.findall('(?<=MKS).*',title)

			#print(config)

			# extract the price
			try:
				price = block.xpath('.//div[@class="payment-section"]/span[@class="listing-row__price "]/text()').extract_first().strip().replace(',','')
			#price = block.xpath('.//div[@class="payment-section"]/span[1]/text()').extract_first().strip().replace(',','')
				price = int(price[1:])
				#print(price)
			except AttributeError:
				price = ''

			# extract the mileage
			mileage = block.xpath('.//div[@class="payment-section"]/span[@class="listing-row__mileage"]/text()').extract_first().strip().replace(',','').replace('mi.','')
			mileage = int(mileage)
			#print(mileage)

			# extract the drivetrain
			drivetrain = block.xpath('.//ul[@class="listing-row__meta"]/li[4]/text()').extract()[1].strip()
			# drivetrain = blocks[0].xpath('.//ul[1]/li[4]/text()').extract()

			# extract the transmission
			transmission = block.xpath('.//ul[@class="listing-row__meta"]/li[3]/text()').extract()[1].strip()

			# extract the exterior color
			exterior_color = block.xpath('.//ul[@class="listing-row__meta"]/li[1]/text()').extract()[1].strip()

			# extract the interior color
			interior_color = block.xpath('.//ul[@class="listing-row__meta"]/li[2]/text()').extract()[1].strip()

			item = ResaleItem()
			item['brand'] = brand
			item['price'] = price
			item['model'] = model
			item['drivetrain'] = drivetrain
			item['year'] = year
			item['exterior_color'] = exterior_color
			item['interior_color'] = interior_color
			item['mileage'] = mileage
			item['transmission'] = transmission
			item['config'] = config

			yield item
