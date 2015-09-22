import pandas as pd
import random
from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep


def get_wayfair_product_links(link, num_pages=1):
	'''
    INPUT: 
    * product index page URL link 
    * number of pages that product links will be scrapped from 
      (each page have 48 products)
    
    OUTPUT:
    * URL links to product pages with product details
    '''

    product_links = []

    for num in range(1,num_pages+1):
        html  = urlopen(link+str(num))
        soup = BeautifulSoup(html, 'html.parser')
        productbox = soup.findAll('a', {'class':'productbox'})
        product_links.extend([s['href'] for s in productbox])
        
    sleep(random.random())
    return product_links



def wayfair_product_info_scrapper(link, category_input):
    '''
    INPUT: 
    * one product URL link 
    * category name
    
    OUTPUT:
    A product info dictionary with the following keys:
	    * product_id
	    * website
	    * category
	    * url
	    * title
	    * price
	    * colors

	    * description
	    * features
	    * specs
	    
	    * manufacturer
	    * rating_avg
	    * rating_count

	    * image_links_all
	    * image_links_by_color
    
    '''

#     import requests
#     html = requests.get(link, timeout=100)

    html  = urlopen(link, timeout=100)
    soup = BeautifulSoup(html, 'html.parser')
    
    product_id = soup.find('span', {'class': 'product_breadcrumb'}).text.split(':')[1]
    website = 'wayfair'
    category = category_input
    url = link
    title = soup.find('span', {'class':'title_name'}).text.strip()
    price = soup.find('div', {'class':'dynamic_sku_price'}).text.strip()
    color_info = soup.findAll('a', {'class': 'js-visual-option'})
    colors = [x['data-name'] for x in color_info]
    
    features_info = soup.findAll('div', {'class':'product_sub_section'})
    features = [x.text for x in features_info]
       
    manufacturer = soup.find('span', {'class':'manu_name'}).text.strip().lstrip('by').strip() 
    
    if soup.find('p', {'class':'product_section_description'}) != None:
        description = soup.find('p', {'class':'product_section_description'}).text
    else:
        description = None
        
    if soup.find('span', {'class': 'rating_value'}) != None:
        rating_avg = soup.find('span', {'class': 'rating_value'}).text
    else:
        rating_avg = None
    
    if soup.find('span', {'itemprop':"reviewCount"}) != None:
        rating_count = soup.find('span', {'itemprop':"reviewCount"}).text
    else:
        rating_count = None
    
    if soup.find('div', {'class':'spec_dimensions'}) != None:
        specs = soup.find('div', {'class':'spec_dimensions'}).text
    else:
        specs = None
     
    image_links_all = []
    image_links_by_color = {}
    
    image_info = soup.findAll('a', {'class': 'photoswipe_link'})
    image_links = [x['data-original-src'] for x in image_info]
    
    if len(colors) == 0:
        image_links_all = image_links
    else:
        color_links = [x['href'] for x in color_info]
        for i, color_link in enumerate(color_links):
            color_key = colors[i]
            link_color = link + color_link
            html_color  = urlopen(link_color, timeout=100)
            soup_color = BeautifulSoup(html_color, 'html.parser')
            image_info_color = soup_color.findAll('a', {'class': 'photoswipe_link'})
            image_links_color = [x['data-original-src'] for x in image_info_color]
            image_links_by_color[color_key] = image_links_color
            image_links_all.extend(image_links_color)
            sleep(random.random())
    image_links_all = list(set(image_links_all))
    
    product_info_dict = {}
    product_info_dict['product_id'] = product_id
    product_info_dict['website'] = website
    product_info_dict['category'] = category
    product_info_dict['url'] = url
    product_info_dict['title'] = title
    product_info_dict['price'] = price
    product_info_dict['colors'] = colors
    
    product_info_dict['description'] = description
    product_info_dict['features'] = features
    product_info_dict['specs'] = specs
    product_info_dict['manufacturer'] = manufacturer
    product_info_dict['rating_avg'] = rating_avg
    product_info_dict['rating_count'] = rating_count
    

    product_info_dict['image_links_all'] = image_links_all
    product_info_dict['image_links_by_color'] = image_links_by_color
    
    sleep(random.random())
    return product_info_dict
