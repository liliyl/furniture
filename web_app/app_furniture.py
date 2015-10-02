import pandas as pd
import cPickle as pickle
import skimage
from skimage.io import imread
from recommender import recommender
from flask import Flask, render_template, request
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')


# input pages
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


# recommended item pages - sofa:
@app.route('/sofa_seeker', methods=['POST'])
def sofa_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    price_limit = str(request.form['price_limit'])
    
    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat='sofa', msg='Oops! That was not a image url. ', form_action="/sofa_seeker#portfolio")
    else:
        image = None

    if len(price_limit) > 0:
        try:
            price_limit = int(price_limit)
        except ValueError:
            return render_template('input.html', cat='sofa', msg='Oops! Please enter a number in the price limit box. ', form_action="/sofa_seeker#portfolio")
    else:
        price_limit = None

    final_df = recommender(image=image, text=description, category='sofa', color=False, price_limit=price_limit)
    base_path = '../static/img/wayfair/sofa/'

    if final_df is None:
        return render_template('input.html', cat='sofa', msg='Oops! No items found! Please increase the price limit. ', form_action="/sofa_seeker#portfolio")

    return render_template('seeker.html', cat='sofa', df=final_df, base_path=base_path, form_action="/sofa_seeker#portfolio")






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
