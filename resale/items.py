# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field() # the brand of the motor vehicle 
    price = scrapy.Field() # the price of the motor vehicle
    model = scrapy.Field() # the model of the motor vehicle
    drivetrain = scrapy.Field() # the drivetrain of the model vehicle
    year = scrapy.Field() # the year of the model of the motor vehicle
    exterior_color = scrapy.Field() # the exterior color of the motor vehicle
    interior_color = scrapy.Field() # the interior color of the motor vehicle
    mileage = scrapy.Field() # the mileage travelled by the motor vehicle
    transmission = scrapy.Field() # the transmission of the motor vehicle
    config = scrapy.Field()
