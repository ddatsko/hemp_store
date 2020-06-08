from flask import Flask, session, redirect, jsonify, request, render_template, url_for
from utils import get_user_from_session

from classes.users import Buyer, UserRole, Agronom
from helper_functions import check_registered, register_new


app = Flask(__name__)
app.secret_key = b'HeLl0ThisIsRand0m8ytesHemp_st0resoCOOOOll'

@app.route('/', methods=["GET", "POST"])
def render_welcome():
    return render_template("welcome/welcome.html")


@app.route('/log_in')
def render_login():
    # takes login data from user
    return render_template("log_in/log_in.html")

@app.route('/log_in', methods=["POST"])
def process_input():
    # processes user's input
    pas = request.form['password']
    mail = request.form['mail']

    if check_registered(pas, mail):
        return title_page(mail, pas)
    else:
        return render_template("log_in/failed_log.html")

@app.route('/agro_register')
def process_a_reg():
    #processes agro registration
    return render_template("register/agro_register.html")

@app.route('/agro_register', methods=["POST"])
def process_a_reg_response():
    #processes agro registration
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    b_a = request.form['bank_account']
    mail = request.form['mail']
    location = request.form['location']
    password = request.form['password']

    if register_new("agronom", name, surname, phone, b_a, mail, location, password):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")

@app.route('/buyer_register')
def process_b_reg():
    #processes buyer registration
    return render_template("register/buyer_register.html")

@app.route('/buyer_register', methods=["POST"])
def process_b_reg_response():
    #processes agro registration
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    b_a = request.form['bank_account']
    mail = request.form['mail']
    location = request.form['location']
    money = request.form['money']
    password = request.form['password']
    

    if register_new("agronom", name, surname, phone, b_a, mail, location, password):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")

@app.route('/seller_register')
def process_s_reg():
    #processes buyer registration
    return render_template("register/seller_register.html")

@app.route('/seller_register', methods=["POST"])
def process_s_reg_response():
    #processes agro registration
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    b_a = request.form['bank_account']
    mail = request.form['mail']
    location = request.form['location']
    productivity = request.form['productivity']
    password = request.form['password']
    
    if register_new("agronom", name, surname, phone, b_a, mail, location, password):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")

@app.route('/main')
def title_page( mail: str = None, password: str = None):
    # if there is a logged in user

    session['user'] = Buyer(0, 'Name Surname', 'email').__dict__()

    user = get_user_from_session(session)
    return user.render_buyers()

    return render_template

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/buy')
def buy_hemp():
    user = get_user_from_session(session)
    return user.render_buyers()


@app.route('/orders')
def orders():
    user = get_user_from_session(session)
    return user.render_orders()


@app.route('/agronoms')
def agronoms():
    user = get_user_from_session(session)
    return user.render_agronoms()


@app.route('/feed_backs')
def feed_backs():
    user = get_user_from_session(session)
    return user.render_feed_backs()


@app.route('/degustations')
def degustations():
    user = get_user_from_session(session)
    return user.render_degustations()


@app.route('/buyers')
def buyers():
    user = get_user_from_session(session)
    return user.render_buyers()


@app.route('/trips')
def trips():
    return get_user_from_session(session).render_trips()


#######################################################################
# ############## API part #############################################
#######################################################################

@app.route('/get_goods', methods=['POST'])
def get_goods():
    data = request.get_json()
    # TODO: make request to DB here
    return jsonify(({"name": 'Best hemp', 'price': '128', 'pack': '15', 'min_age': 18, 'id': 1},
                    {"name": 'Best hemp 2', 'price': '100', 'pack': '5', 'min_age': 16, 'id': 2},
                    {"name": 'Cool hemp', 'price': '10145', 'pack': '1', 'min_age': 0, 'id': 3}))


@app.route('/get_orders', methods=['POST'])
def get_orders():
    user = get_user_from_session(session)
    if user.role != UserRole.BUYER.value:
        return jsonify([])
    else:
        user_id = user.id
        filters = request.get_json()

        # Обережно з формаом дати. В запиті вона у форматі "yyyy-mm-dd"
        min_date = filters['minDate']
        max_date = filters['maxDate']
        # TODO: Request to db here
        return jsonify(
            ({"id": "1", "name": "Best hemp", "seller": "Ivan", "amount_of_product": 128, "made": "2020-01-01",
              "successful": True},))


@app.route('/get_agronoms', methods=['POST'])
def get_agronoms():
    data = request.get_json()
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:  # Превірка, бо в цьому випадку треба знайти спільні покупки та дегустації
        user_id = user.id
        min_buys = data['minBuys']
        max_buys = data['maxBuys']
        min_degustations = data['minDegustations']
        max_degustations = data['maxDegustations']
        # TODO: request to DB, using fields above here
        return jsonify(({"id": 0, "full_name": "Ostap Dyhdalovych", "location": "Lviv", "rating": "10", "buys": 10,
                         "degustations": 1},))
    elif user.role == UserRole.AGRONOMIST.value:
        min_trips = data['minTrips']
        max_trips = data['maxTrips']
        min_date = data['minDate']
        max_date = data['maxDate']
        # TODO: request to DB here
        return jsonify(({"id": 0, "full_name": "Ostap Dyhdalovych", "location": "Lviv", "rating": "10", "trips": 5},))


@app.route('/get_feed_backs', methods=['POST'])
def get_feed_backs():
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:  # Бо різні запити до БД для покупця і, наприклад, агронома
        user_id = user.id
        data = request.get_json()
        min_data = data['minDate']
        max_date = data['maxDate']
        # TODO: make request to DB here, using above fields
        return jsonify(({"id": 0, "agronom_name": "Ostap",
                         "message": "Good Good Good. I loved this hemp. The agronom is super cool",
                         "product_name": "Cool hemp"},
                        {"id": 0, "agronom_name": "Ostap",
                         "message": "Good Good Good. I loved this hemp. The agronom is super cool",
                         "product_name": "Cool hemp"}))


@app.route('/get_degustations', methods=['POST'])
def get_degustations():
    user = get_user_from_session(session)
    data = request.get_json()
    user_id = user.id
    if user.role == UserRole.BUYER.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        agronom_name = data['agronomName']
        # TODO: make request to BD using fields above
        return jsonify(({"id": 0, "product_name": "Cool hemp", "with": ['Denys', 'Ostap', 'Vlad', 'Anna']},))
    elif user.role == UserRole.AGRONOMIST.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        product_name = data['productName']
        min_buyers = data['minBuyers']
        # TODO: Request to DB here
        return jsonify(({'id': 1, 'product_name': 'Cool hemp', 'testers': ['Ostap', 'Vlad', 'Denys'],
                         'date': '2020-06-06', 'amount': '1'},))


@app.route('/get_buyers', methods=['POST'])
def get_buyers():
    user = get_user_from_session(session)
    if user.role == UserRole.AGRONOMIST.value:
        data = request.get_json()
        print(data)
        min_date = data['minDate']
        max_fate = data['maxDate']
        min_buys = data['minBuys']
        max_buys = data['maxBuys']
        # TODO: Make request to DB here
        return jsonify(({'id': 0, 'full_name': 'Ostap', 'buys': 10, 'degustations': 1, 'location': 'Lviv'},))


@app.route('/get_trips', methods=['POST'])
def get_tris():
    user = get_user_from_session(session)
    if user.role == UserRole.AGRONOMIST.value:
        data = request.get_json()
        user_id = user.id
        min_date = data['minDate']
        max_date = data['maxDate']
        # TODO: Request to DB here
        return jsonify(({'id': 0, 'with': ['Ostap', 'Denys', 'Vlad', 'Anya'], 'departion': '2020-05-06',
                        'arrival': '2020-05-07', 'location': 'Lviv'},))


if __name__ == '__main__':
    app.run(debug=True, port=1200)
