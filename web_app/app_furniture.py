from flask import Flask, render_template, request
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html', title='Hello!')

@app.route('/sofa_input')
def sofa_input():
    return render_template('sofa_input.html')

@app.route('/sofa_seeker', methods=['POST'])
def sofa_seeker():
    text = str(request.form['user_input'])
    return render_template('sofa_seeker.html', text=text)


# coffee_table_input
# dining_input
# desk_chair_input
# bookcase_input
# nightstand_input
# bed_input
# dresser_input

# My maps
@app.route('/map', methods=['POST'] )
def map():
    text = str(request.form['user_input'])


              #   <form action="/sofa_seeker" method='POST' >
              #     <input type="text" name="user_input" />
              #   <input type="submit" />
              # </form>

    # return render_template('locked_out.html', map_name = 'Rescue Lock In/Out', maplink = maplink)


    # return render_template('map.html', map_name = map_name, maplink = maplink)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
