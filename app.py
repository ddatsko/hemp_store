from flask import Flask, session, redirect, jsonify, request, render_template

from classes.users import Buyer, UserRole, Agronom, Admin
from helper_functions import check_registered, register_new, get_user_from_session

app = Flask(__name__, static_url_path='/home/vlad/Desktop/2_year/Database/project_final/hemp_store/static')
app.secret_key = b'HeLl0ThisIsRand0m8ytesHemp_st0resoCOOOOll'


@app.route('/', methods=["GET", "POST"])
def render_welcome():
    user = get_user_from_session(session)
    return user.render_default()


@app.route('/log_in')
def render_login():
    # takes login data from user
    user = get_user_from_session(session)
    return user.render_login()


@app.route('/log_in', methods=["POST"])
def process_input():
    # processes user's input
    if 'user' in session:
        return redirect('/')
    pas = request.form['password']
    mail = request.form['mail']

    if check_registered(pas, mail):
        # JUST FOR TEST
        if mail == 'admin@gmail.com':
            session['user'] = Admin(0, 'Denys', 'admin@gmail.com').__dict__()
        elif mail == 'agronom@gmail.com':
            session['user'] = Agronom(0, 'Denys', 'agronom@gmail.com').__dict__()
        else:
            session['user'] = Buyer(0, 'Name Surname', 'email').__dict__()
        return redirect('/')
    else:
        return render_template("log_in/failed_log.html")


@app.route('/agro_register')
def process_a_reg():
    # processes agro registration
    if 'user' in session:
        return redirect('/')
    return render_template("register/agro_register.html")


@app.route('/agro_register', methods=["POST"])
def process_a_reg_response():
    # processes agro registration
    session.clear()
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    b_a = request.form['bank_account']
    mail = request.form['mail']
    location = request.form['location']
    password = request.form['password']

    if register_new(UserRole.AGRONOMIST, name, surname, phone, b_a, mail, location, password):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")


@app.route('/buyer_register')
def process_b_reg():
    # processes buyer registration
    if 'user' in session:
        return redirect('/')
    return render_template("register/buyer_register.html")


@app.route('/buyer_register', methods=["POST"])
def process_b_reg_response():
    # processes agronom registration
    session.clear()
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    b_a = request.form['bank_account']
    mail = request.form['mail']
    location = request.form['location']
    money = request.form['money']
    password = request.form['password']

    if register_new(UserRole.BUYER, name, surname, phone, b_a, mail, location, password):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")


@app.route('/seller_register')
def process_s_reg():
    # processes buyer registration
    if 'user' in session:
        return redirect('/')
    return render_template("register/seller_register.html")


@app.route('/seller_register', methods=["POST"])
def process_s_reg_response():
    # processes agro registration
    session.clear()
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']
    b_a = request.form['bank_account']
    mail = request.form['mail']
    location = request.form['location']
    productivity = request.form['productivity']
    password = request.form['password']

    if register_new(UserRole.SELLER, name, surname, phone, b_a, mail, location, password):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")


@app.route('/leave_feed_back/<target>/<target_id>', methods=['GET'])
def leave_feedback(target_id: int, target: str):
    if get_user_from_session(session).role == UserRole.BUYER.value:
        user = get_user_from_session(session)
        print("HERE")
        if target == 'agronom':
            # TODO: request to DB to get agronom name by id
            return user._render('feed_back_forms/feed_back_form.j2', -1, name='Agronom name')
        elif target == 'product':
            # TODO: request to DB to get product name by id
            return user._render('feed_back_forms/feed_back_form.j2', -1, name='Product name')
    return redirect('/')


@app.route('/leave_feed_back/<target>/<target_id>', methods=['POST'])
def save_feedback(target_id: int, target: str):
    if get_user_from_session(session).role == UserRole.BUYER.value:
        user = get_user_from_session(session)
        message = request.form['message']
        grade = request.form['grade']
        print(message, grade)
        if target == 'agronom':
            # TODO: request to DB to save the feed_back
            if True:  # if feed_back saved successfully
                return user._render('result_messages/success.j2', -1, message='Відгук залишено успішно!')
            else:
                return user._render('result_messages/fail.j2', -1, message='Упс.. З відгуком виникли проблеми!')
        elif target == 'product':
            # TODO: request to DB to save the feed_back
            if False:  # if feed_back saved successfully
                return user._render('result_messages/success.j2', -1, message='Відгук залишено успішно!')
            else:
                return user._render('result_messages/fail.j2', -1, message='Упс.. З відгуком виникли проблеми!')
    return redirect('/')


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


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


@app.route('/sorts')
def sorts():
    return get_user_from_session(session).render_sorts()


@app.route('/products')
def products():
    return get_user_from_session(session).render_products()


@app.route('/agronom/<agronom_id>')
def agronom(agronom_id: int):
    # TODO: Request to DB here. Note: dict can contain any keys. All will be displayed. Only item_name will be displayed with bold text
    return get_user_from_session(session).render_user(
        {'item_name': 'Агроном Vlad Zadorozhnyi', 'Name': 'Vlad', 'Surname': 'Zadorozhnyi',
         'Location': 'Ternopil, Ukraine', 'Debt': '100 000 $'})


@app.route('/buyer/<buyer_id>')
def buyer(buyer_id: int):
    # TODO: Request to DB here. Note: dict can contain any keys. All will be displayed. Only item_name will be displayed with bold text
    return get_user_from_session(session).render_user(
        {'item_name': 'Покупець Vlad Zadorozhnyi', 'Name': 'Vlad', 'Surname': 'Zadorozhnyi',
         'Location': 'Ternopil, Ukraine', 'Debt': '100 000 $'})


@app.route('/hemp/<hemp_id>')
def hemp(hemp_id: int):
    # TODO: Request to DB here
    return get_user_from_session(session).render_hemp(
        {'item_name': 'Cool hemo', 'Days growtime': '125', 'Frost Resistance': 'Good'})  # any items here


@app.route('/product/<product_id>')
def product(product_id: int):
    # TODO: Request to DB here
    return get_user_from_session(session).render_product(
        {'item_name': 'Cool product', 'Price': '12', 'Pack': '13 шт', 'Min Age': 18})  # any items here


@app.route('/degustation/<degustation_id>')
def degustation(degustation_id: int):
    # TODO: Request to DB here
    return get_user_from_session(session).render_degustation(
        {'item_name': 'Maybe name of degustation', 'Agronom name': 'Vlad', 'Product name': 'Cool product',
         'Buyers': ['Denys', 'Ostap', 'Anya']})  # any items here


@app.route('/trip/<trip_id>')
def trip(trip_id: int):
    # TODO: Request to DB here
    return get_user_from_session(session).render_trip(
        {'item_name': 'Ternopil', 'Date': '2020-01-01', 'Purpose': 'Degustation of Vlad`s hemp',
         'Agronoms': ['Denys', 'Ostap', 'Anya']})  # any items here


#######################################################################
# ############## API part #############################################
#######################################################################

@app.route('/return/<deal_id>')
def return_deal(deal_id: int):
    user = get_user_from_session(session)
    # TODO: check if the user made this deal and if it can be returned (date and if not returned already)
    if True:
        return user._render('result_messages/success.j2', -1, message="Угоду успішно відмінено")
    else:
        return user._render('result_messages/fail.j2', -1, message="Угоду не вдалося відмінити. Перевірте, чи вона "
                                                                   "вже не відмінена та чи не пройшло 14 "
                                                                   "днів з моменту укладання")


@app.route('/get_goods', methods=['POST'])
def get_goods():
    data = request.get_json()
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:
        min_age = data['minAge']
        min_price = data['minPrice']
        max_price = data['maxPrice']
        # TODO: make request to DB here
        return jsonify(({"name": 'Best hemp', 'price': '128', 'pack': '15', 'min_age': 18, 'id': 1},
                        {"name": 'Best hemp 2', 'price': '100', 'pack': '5', 'min_age': 16, 'id': 2},
                        {"name": 'Cool hemp', 'price': '10145', 'pack': '1', 'min_age': 0, 'id': 3}))
    elif user.role == UserRole.ADMIN.value:
        min_distinct_buyers = data['minDistinctBuyers']
        min_date = data['minDate']
        max_date = data['maxDate']
        return jsonify(({'id': 4, 'name': 'Best hemp', 'return_percent': '15', 'pack': 1, 'price': 16, 'min_age': 18},))


@app.route('/get_orders', methods=['POST'])
def get_orders():
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:
        user_id = user.id
        filters = request.get_json()

        # Обережно з формаом дати. В запиті вона у форматі "yyyy-mm-dd"
        min_date = filters['minDate']
        max_date = filters['maxDate']
        # TODO: Request to db here
        return jsonify(
            ({"id": "1", "name": "Best hemp", "seller": "Ivan", "amount_of_product": 128, "made": "2020-01-01",
              "successful": True, 'deal_id': 10},))


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
    elif user.role == UserRole.ADMIN.value:
        min_sorts = data['minSorts']
        min_date = data['minDate']
        max_date = data['maxDate']
        # TODO REQUEST TO DB here
        return jsonify(({"id": 0, "full_name": "Ostap Dyhdalovych", "location": "Lviv", "rating": "10", "sorts": 5},))


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
    data = request.get_json()
    if user.role == UserRole.AGRONOMIST.value:
        min_date = data['minDate']
        max_fate = data['maxDate']
        min_buys = data['minBuys']
        max_buys = data['maxBuys']
        # TODO: Make request to DB here
        return jsonify(({'id': 0, 'full_name': 'Ostap', 'buys': 10, 'degustations': 1, 'location': 'Lviv'},))
    if user.role == UserRole.ADMIN.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        min_buys = data['minBuys']
        # TODO: Request to DB here
        return jsonify(({'id': 0, 'full_name': 'Ostap', 'buys': 10, 'location': 'Lviv'},))


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


@app.route('/get_sorts', methods=['POST'])
def get_sorts():
    user = get_user_from_session(session)
    data = request.get_json()
    if user.role == UserRole.ADMIN.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        min_harvesting = data['minHarvesting']
        # TODO: Request to DB here
        return jsonify(({'id': 0, 'average_trips': 1.4, 'name': 'Cool sort'},))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=1200)
