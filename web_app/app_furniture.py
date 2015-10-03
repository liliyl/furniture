import pandas as pd
import cPickle as pickle
import skimage
from skimage.io import imread
from recommender import recommender
from flask import Flask, render_template, request
app = Flask(__name__)


# Home page:
@app.route('/')
def index():
    return render_template('index.html')


# Input pages for 8 categories:
@app.route('/sofa_input')
def sofa_input():
    return render_template('input.html', cat='sofa', msg='', form_action="/sofa_seeker#portfolio")

@app.route('/coffee_table_input')
def coffee_table_input():
    return render_template('input.html', cat='coffee table', msg='', form_action="/coffee_table_seeker#portfolio")

@app.route('/dining_input')
def dining_input():
    return render_template('input.html', cat='dining table/chair', msg='', form_action="/dining_seeker#portfolio")

@app.route('/office_input')
def office_input():
    return render_template('input.html', cat='office desk/chair', msg='', form_action="/office_seeker#portfolio")

@app.route('/bookcase_input')
def bookcase_input():
    return render_template('input.html', cat='bookcase', msg='', form_action="/bookcase_seeker#portfolio")

@app.route('/nightstand_input')
def nightstand_input():
    return render_template('input.html', cat='nightstand', msg='', form_action="/nightstand_seeker#portfolio")

@app.route('/bed_input')
def bed_input():
    return render_template('input.html', cat='bed', msg='', form_action="/bed_seeker#portfolio")

@app.route('/dresser_input')
def dresser_input():
    return render_template('input.html', cat='dresser', msg='', form_action="/dresser_seeker#portfolio")


# Recommended items page - sofa:
@app.route('/sofa_seeker', methods=['POST'])
def sofa_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'sofa'
    cat = 'sofa'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - coffee table:
@app.route('/coffee_table_seeker', methods=['POST'])
def coffee_table_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'coffee_table'
    cat = 'coffee table'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - dining table/chair:
@app.route('/dining_seeker', methods=['POST'])
def dining_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'dining'
    cat = 'dining table/chair'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - bookcase:
@app.route('/bookcase_seeker', methods=['POST'])
def bookcase_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'bookcase'
    cat = 'bookcase'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - office desk/chair:
@app.route('/office_seeker', methods=['POST'])
def office_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'office'
    cat = 'office desk/chair'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - nightstand:
@app.route('/nightstand_seeker', methods=['POST'])
def nightstand_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'nightstand'
    cat = 'nightstand'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - bed:
@app.route('/bed_seeker', methods=['POST'])
def bed_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'bed'
    cat = 'bed'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


# Recommended items page - dresser:
@app.route('/dresser_seeker', methods=['POST'])
def dresser_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    category = 'dresser'
    cat = 'dresser'
    form_action = "/" + category + "_seeker#portfolio"

    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat=cat, msg='Oops! That was not a image url. ', form_action=form_action)
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat=cat, msg='Oops! Please enter a number in the price limit box. ', form_action=form_action)
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category=category, color=False, price_limit=price_limit)
    if final_df is None:
        return render_template('input.html', cat=cat, msg='Oops! No items found! Please increase the price limit. ', form_action=form_action)
    
    base_path = '../static/img/wayfair/' + category + '/'
    return render_template('seeker.html', cat=cat, df=final_df, base_path=base_path, form_action=form_action)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
