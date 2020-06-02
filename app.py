from flask import Flask, session, redirect, jsonify, request
from classes.users import Buyer
from classes import dbCommunicator

app = Flask(__name__)
app.secret_key = b'HeLl0ThisIsRand0m8ytesHemp_st0resoCOOOOll'
comm = dbCommunicator(db_name = "db_weed", user="postgres", password = "postgres", host = "localhost")

@app.route('/')
def title_page():
    # if there is a logged in user
    if 'user' not in session:
        session['user'] = Buyer(1, 'Denys Datsko', '', '').__dict__()

    return Buyer(**session['user']).render_buyers()


@app.route('/logout')
def log_out():
    session.clear()
    session['user'] = Buyer(1, 'hello@hello.com', '')
    return redirect('/')


@app.route('/buy')
def buy_hemp():
    # return session['user']
    return ''


# API part
@app.route('/get_goods', methods=['GET', 'POST'])
def get_goods():
    data = request.get_json()
    # TODO: make request to DB here
    # return jsonify(({"name": 'Best hemp', 'price': '128', 'pack': '15', 'min_age': 18, 'id': 1},
    #                 {"name": 'Best hemp 2', 'price': '100', 'pack': '5', 'min_age': 16, 'id': 2},
    #                 {"name": 'Cool hemp', 'price': '10145', 'pack': '1', 'min_age': 0, 'id': 3}))
    return jsonify(comm.get_user_items())


if __name__ == '__main__':
    session['user'] = Buyer(1, 'Buyer@gmail.com', '')
    app.run(debug=True, port=1200)
