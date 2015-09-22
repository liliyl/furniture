from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import string
import collections
 
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer



def wayfair_product_links(link, num_pages = 1):

    linklist = []

    for num in range(1,num_pages+1):

        print num

        html  = urlopen(link+str(num))
        soup = BeautifulSoup(html, 'html.parser')
        productbox = soup.findAll('a', {'class':'productbox'})
        linklist.extend([s['href'] for s in productbox])

    return linklist



def wayfair_scraper(link):

    if link[:12] == '/daily-sales':
        link = 'http://www.wayfair.com' + link
        print 'SPECIAL!'

    html  = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.findAll('div', {'class':'product_sub_section'})
    features = [''.join(s.findAll(text=True)).replace('\n',',') for s in product]
    try:
        price = soup.find('div', {'class':'dynamic_sku_price'}).text.strip()
        title = soup.find('span', {'class':'title_name'}).text.strip()

    except:
        price = soup.find('div', {'class':'dynamic_sku_price'})
        title = soup.find('span', {'class':'title_name'})
    
    try:
        manufacturer = ''.join(soup.find('span', {'class':'manu_name'}).text.replace('\n', '').replace('              by              ', '')).strip()
        print manufacturer
    except:
        manufacturer = soup.find('span', {'class':'manu_name'})
    
    try:
        image = soup.find('div', {'class': 'js-slider-container car_slider'}).find('img')['src']
    except:
        image = None

    #features[0] = features[0].split('Features')[1:]
    #features[1] = features[1].split('Product Details')[1:]
    sleep(1)
    return price, title, manufacturer, features, link
    #return ([s for s in ' '.join(features[0]).split(',') if s], [s for s in ' '.join(features[1]).split(',') if s])

print wayfair_scraper("http://www.wayfair.com/Vita-Mix-Professional-Series-750-Blender-1944-VTM1020.html")





furniturelinks = wayfair_product_links('http://www.wayfair.com/Dressers-C46091.html?&curpage=')
furniture_info = []
for each in furniturelinks:
    info = wayfair_scraper(each)
    print info
    furniture_info.append(info)

    

furniture_join = []
for each in furniture_info:
    if each:   
        furniture_join.append(''.join(each))




vectorizer = TfidfVectorizer(max_df=(.6), min_df=(3./float(len(furniture_join))), stop_words='english',use_idf=True, strip_accents='ascii', ngram_range = (1,3))
X = vectorizer.fit_transform(furniture_join)
features = vectorizer.get_feature_names()

print features

km_model = KMeans(n_clusters=10)
km_model.fit(X)
clustering = collections.defaultdict(list)

for idx, label in enumerate(km_model.labels_):
    clustering[label].append(idx)

print clustering