import pandas as pd
import random
import urllib
import threading
from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep


def get_wayfair_product_links(base_link, num_pages=1):
    '''
    INPUT: 
        base_link: string
            product index page URL link 
        num_pages: integer
            number of pages that product links will be scraped from 
            (each page have 48 products)
    OUTPUT:
        product_links: list of strings
            URL links to product pages with product details
    '''

    product_links = []

    for num in range(1,num_pages+1):
        html  = urlopen(base_link+str(num))
        soup = BeautifulSoup(html, 'html.parser')
        productbox = soup.findAll('a', {'class':'productbox'})
        product_links.extend([s['href'] for s in productbox])
        
    sleep(random.random())
    return product_links


def wayfair_product_info_scraper(link, category):
    '''
    INPUT: 
        link: string
            one product URL link 
        category: string
    OUTPUT:
        product_info_dict: dictionary
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

    html  = urlopen(link, timeout=100)
    soup = BeautifulSoup(html, 'html.parser')
    
    product_id = soup.find('span', {'class': 'product_breadcrumb'}).text.split(':')[1]
    website = 'wayfair'
    url = link
    title = soup.find('span', {'class':'title_name'}).text.strip()
    price = soup.find('div', {'class':'dynamic_sku_price'}).text.strip()
    color_info = soup.findAll('a', {'class': 'js-visual-option'})
    colors = [x['data-name'] for x in color_info]
    
    features_info = soup.findAll('div', {'class':'product_sub_section'})
    features = [x.text for x in features_info]
       
    manufacturer = soup.find('span', {'class':'manu_name'}).text.strip().lstrip('by').strip() 
        
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

    if soup.find('p', {'class':'product_section_description'}) != None:
        description = soup.find('p', {'class':'product_section_description'}).text
    else:
        description = None

    # Add code to scrape missing features data (when the webpage has a different structure):
    if len(features) == 0:
        description_info = soup.find('div', {'class':'no_json_description'})
        if description_info.text != None:
            description = description_info.text
        else:
            description = '\n'.join([x.text for x in description_info.findAll('p')])
        if description_info.ul != None:
            features = description_info.ul.text
        else:
            features = '\n'.join([x.text for x in soup.findAll('ul') if 'Free Shipping' not in x.text])
    # Added code ends

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


def wayfair_image_scraper(indices, category):
    '''
    Save images from the image URLs.

    INPUT: 
        indices: list of integers
        category: string
    OUTPUT:
        None
    '''

    image = urllib.URLopener()
    for i in indices:
        i = int(i)
        product_id = str(df.ix[i,'product_id'].strip())
        img_links = df.ix[i,'image_links_all']

        for j, link in enumerate(img_links):
            image.retrieve(link, 'wayfair/images/%s/%s_%s_%s.jpg' % (category, category, product_id, str(j)))


def multithreading_image_scraper(df, category):
    '''
    INPUT: 
        df: pandas dataframe 
        category: string
    OUTPUT:
        None
    '''

    index = df.index.values
    threads = []
    for i in xrange(0, 11):
        start = i*100
        if (i+1)*100 > 1008:       
            end = 1008       
        else:
            end = (i+1)*100
        indices = tuple(index[start:end])
        t = threading.Thread(target=wayfair_image_scraper, args=(indices, category))
        threads.append(t)

    for thread in threads: thread.start()
    for thread in threads: thread.join()


if __name__ == '__main__':

    # Base link for each category:
    base_link_dict = {}
    base_link_dict['sofa'] = 'http://www.wayfair.com/Sofas-C413892.html?&curpage='
    base_link_dict['sofa_bed'] = 'http://www.wayfair.com/Sofa-Beds-C413895.html?&curpage='
    base_link_dict['futon'] = 'http://www.wayfair.com/Futons-C1780368.html?&curpage='
    base_link_dict['loveseat'] = 'http://www.wayfair.com/Loveseats-C413896.html?&curpage='
    base_link_dict['coffee_table'] = 'http://www.wayfair.com/Coffee-Tables-C414602.html?&curpage='
    base_link_dict['desk'] = 'http://www.wayfair.com/All-Desks-C1780384.html?&curpage='
    base_link_dict['office_chair'] = 'http://www.wayfair.com/All-Office-Chairs-C478390.html?&curpage='
    base_link_dict['bookcase'] = 'http://www.wayfair.com/All-Bookcases-C1780385.html?&curpage='
    base_link_dict['dining_table'] = 'http://www.wayfair.com/Kitchen-and-Dining-Tables-C46129.html?&curpage='
    base_link_dict['dining_chair'] = 'http://www.wayfair.com/Kitchen-and-Dining-Chairs-C46130.html?&curpage='
    base_link_dict['bed'] = 'http://www.wayfair.com/Beds-C46122.html?&curpage='
    base_link_dict['nightstand'] = 'http://www.wayfair.com/Nightstands-C46062.html?&curpage='
    base_link_dict['dresser'] = 'http://www.wayfair.com/Dressers-C46091.html?&curpage='

    categories = ['sofa', 'sofa_bed', 'futon', 'loveseat', 'coffee_table', 'desk', 'office_chair', 
                    'dining_table', 'dining_chair', 'bookcase', 'nightstand', 'bed', 'dresser']

    # Product info scraping:
    for category in categories:
        product_links = get_wayfair_product_links(base_link_dict[category], num_pages=20)
        link_0 = product_links[0]
        dict_0 = wayfair_product_info_scraper(link_0, category_input= category)
        df = pd.DataFrame([dict_0], index=[0])
        i = 1
        for link in sofa_bed_links[1:]:
            product_dict = wayfair_product_info_scraper(link, category_input=category)
            df_product = pd.DataFrame([product_dict], index=[i])
            df = pd.concat([df, df_product], axis=0)
            i += 1
        df.to_json('wayfair/%s.json' % category)

    # Image scraping: 
    for category in categories:
        df = pd.read_json('wayfair/%s.json' % category)
        multithreading_image_scraper(df, category)
   