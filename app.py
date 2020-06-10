from helper_functions import check_registered, register_new, get_user_from_session, find_role
from classes.users import Buyer, UserRole, Agronom, Admin, NoUser
from flask import Flask, session, redirect, jsonify, request, render_template, make_response

from classes.dbCommunicator import dbCommunicator

app = Flask(__name__)
app.secret_key = b'HeLl0ThisIsRand0m8ytesHemp_st0resoCOOOOll'

comm = dbCommunicator("db14", host="142.93.163.88",
                      port=6006, user="team14", password="pas1swo4rd")
# comm = dbCommunicator(db_name="db_weed")

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

    user_id = check_registered(mail, pas)
    print(user_id)
    if user_id is not None:
        dosie = find_role(mail)
        info = comm.get_user_info(user_id)
        print(dosie)
        if dosie == 'agronom':
            session['user'] = Agronom(user_id, info['full_name'], mail).__dict__()
        elif dosie == 'buyer':
            session['user'] = Buyer(user_id,  info['full_name'], mail).__dict__()
        elif dosie == 'packing_seller':
            return render_template('packing_seller/packer.j2')
        elif dosie == 'admin':
            session['user'] = Admin(user_id,  info['full_name'], mail).__dict__()
        # else:
        #     session['user'] = NoUser().__dict__()
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

    if register_new(UserRole.BUYER, name, surname, phone, b_a, mail, location, password, money):
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

    if register_new(UserRole.SELLER, name, surname, phone, b_a, mail, location, password, productivity):
        return render_template("register/successful_register.html")
    else:
        return render_template("register/failed_register.html")


@app.route('/leave_feed_back/<target>/<target_id>', methods=['GET'])
def leave_feedback(target_id: int, target: str):
    if get_user_from_session(session).role == UserRole.BUYER.value:
        user = get_user_from_session(session)
        print("HERE")
        if target == 'agronom':
            person = comm.get_admin_person(id=target_id)
            if person:
                return user.render('feed_back_forms/feed_back_form.j2', -1, name=person[0]["name"])
            return make_response('', 400)
            # return user.render('feed_back_forms/feed_back_form.j2', -1, name='Agronom name')
        elif target == 'product':
            # Done: request to DB to get product name by id
            # TODO: Handle if there is no such product :1
            product = comm.get_admin_items(id=target_id)
            if (product):
                return user.render('feed_back_forms/feed_back_form.j2', -1, name=product[0]["name"])
            return make_response('', 400)
    return redirect('/')


@app.route('/leave_feed_back/<target>/<target_id>', methods=['POST'])
def save_feedback(target_id: int, target: str):
    if get_user_from_session(session).role == UserRole.BUYER.value:
        user = get_user_from_session(session)
        message = request.form['message']
        if target == 'agronom':
            if comm.add_agronom_feed_back(user_id=user.id, message=message, agronom_id=target_id):
                return user.render('result_messages/success.j2', -1, message='Відгук залишено успішно!')
            else:
                return user.render('result_messages/fail.j2', -1, message='Упс.. З відгуком виникли проблеми!')
        elif target == 'product':
            if comm.add_deal_feed_back(user_id=user.id, message=message, deal_id=target_id):
                return user.render('result_messages/success.j2', -1, message='Відгук залишено успішно!')
            else:
                return user.render('result_messages/fail.j2', -1, message='Упс.. З відгуком виникли проблеми!')
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
    # Done: Request to DB here. Note: dict can contain any keys. All will be displayed. Only item_name will be displayed with bold text
    res = comm.get_admin_agronom()
    if res:
        return get_user_from_session(session).render_item_view(
            {**{'item_name': " ".join(['Агроном', res[0]["name"], res[0]["surname"]])}, **res[0]})
    else:
        return make_response('', 404)


@app.route('/buyer/<buyer_id>')
def buyer(buyer_id: int):
    # Done: Request to DB here. Note: dict can contain any keys. All will be displayed. Only item_name will be displayed with bold text
    res = comm.get_admin_agronom()
    if (res):
        return get_user_from_session(session).render_item_view(
            {**{'item_name': " ".join(['Покупець', res[0]["name"], res[0]["surname"]])}, **res[0]})
    # return get_user_from_session(session).render_item_view(
    #     {'item_name': 'Покупець Vlad Zadorozhnyi', 'Name': 'Vlad', 'Surname': 'Zadorozhnyi',
    #      'Location': 'Ternopil, Ukraine', 'Debt': '100 000 $'})
    else:
        return None
        # TODO: handle inexistent id


@app.route('/hemp/<hemp_id>')
def hemp(hemp_id: int):
    # Done: Request to DB here
    res = comm.get_admin_items(id=hemp_id)
    # return get_user_from_session(session).render_hemp(
    #     {'item_name': 'Cool hemo', 'Days growtime': '125', 'Frost Resistance': 'Good'})  # any items here
    if (res):
        # any items here
        return get_user_from_session(session).render_item_view(res[0])
    else:
        return None
        # TODO: handle inexistent id


@app.route('/product/<product_id>')
def product(product_id: int):
    # Done: Request to DB here
    res = comm.get_admin_items(id=product_id)
    if (res):
        # any items here
        return get_user_from_session(session).render_item_view(res[0])
    else:
        return None
        # TODO: handle inexistent id
    # return get_user_from_session(session).render_product(
    #     {'item_name': 'Cool product', 'Price': '12', 'Pack': '13 шт', 'Min Age': 18})  # any items here


@app.route('/degustation/<degustation_id>')
def degustation(degustation_id: int):
    # Done: Request to DB here
    res = comm.get_admin_degustation(degustation_id)
    if res:
        degustation = res[-1]
        print(degustation)
        return get_user_from_session(session).render_item_view(
            {
                'Agronom name': degustation["seller_name"],
                'Product name': degustation["product_name"],
                'Buyers': comm.get_admin_degustation_peers(degustation_id)}
        )
        # {'item_name': 'Maybe name of degustation', 'Agronom name': 'Vlad', 'Product name': 'Cool product',
        #  'Buyers': ['Denys', 'Ostap', 'Anya']})  # any items here


@app.route('/trip/<trip_id>')
def trip(trip_id: int):
    # Done: Request to DB here
    res = comm.get_trip_info(trip_id)
    if res:
        return get_user_from_session(session).render_item_view(res)

    # return get_user_from_session(session).render_trip(
    #     {'item_name': 'Ternopil', 'Date': '2020-01-01', 'Purpose': 'Degustation of Vlad`s hemp',
    #      'Agronoms': ['Denys', 'Ostap', 'Anya']})  # any items here
    else:
        return make_response('', 404)


@app.route('/make_trip', methods=['GET'])
def make_trip():
    user = get_user_from_session(session)
    return user.render_make_trip()


@app.route('/make_degustation', methods=['GET'])
def make_degustation():
    return get_user_from_session(session).render_make_degustation()


@app.route('/gather_crop', methods=['GET'])
def gather_crop():
    return get_user_from_session(session).render_gather_crop()


@app.route('/confirm_buy/<product_id>', methods=['GET'])
def confirm_buy(product_id):
    user = get_user_from_session(session)
    if user.role != UserRole.BUYER.value:
        return make_response('', 404)
    product = comm.get_item(product_id)
    return user.render('item_creations/buy_product.j2', -1, product_name=product['name'])


#######################################################################
# ############## API part #############################################
#######################################################################


@app.route('/confirm_buy/<product_id>', methods=['POST'])
def confirm_buy_post(product_id):
    user = get_user_from_session(session)
    if user.role != UserRole.BUYER.value:
        return make_response('', 404)
    agronom_id = request.form['agronom_id']
    amount = float(request.form['amount'])
    if amount <= 0:
        return user.render('result_messages/fail.j2', -1, message="Не можна куаляти від'ємну кількість продукту...")

    if comm.add_deal(user.id, product_id, agronom_id, amount):
        return user.render('result_messages/success.j2', -1,
                           message="Покупка пройшля успішно. Тепер ви можете переглянути її у своїх замовленнях")
    return user.render('result_messages/fail.j2', -1,
                       message="Упс... Щось пішло не так...")


@app.route('/gather_crop', methods=['POST'])
def register_crop():
    user = get_user_from_session(session)
    if user.role == UserRole.AGRONOMIST.value:
        data = request.form
        date = data['date']
        amount = float(data['amount'])
        sort_id = int(data['sortId'])
        # Done: Request to DB here
        res = comm.add_agronom_crop(user.id, sort_id, amount, date, False)
        if res:
            return user.render('result_messages/success.j2', -1, message='Урожай успішно зареєстровано')
    return user.render('result_messages/fail.j2', -1, message="Помилка. Урожай не зареєстровано")


@app.route('/make_degustation', methods=['POST'])
def make_new_degustation():
    user = get_user_from_session(session)
    if user.role == UserRole.AGRONOMIST.value:
        data = request.get_json()
        date = data['date']
        amount = data['amount']
        product_id = data['productId']
        buyer_ids = data['buyerIds']
        # Done: Request to DB here

        if comm.add_agronom_degustation(user.id, date, product_id, amount, buyer_ids):  # If request was successful
            return make_response('', 200)

    return make_response('', 400)


@app.route('/make_trip', methods=['POST'])
def create_new_trip():
    if get_user_from_session(session).role == UserRole.ADMIN.value:
        data = request.get_json()
        departion = data['departion']
        arrival = data['arrival']
        location = data['location']
        purpose = data['purpose']
        agronom_ids = data['agronomIds']
        # Done: request to DB to create trip
        comm.add_admin_trip(location, departion, arrival, purpose)
        # TODO: better way to get vacation_id?
        vacation_id = comm.get_admin_trip(
            None, location, departion, arrival, purpose)[-1]["id"]
        comm.add_admin_trip_agronoms(vacation_id, agronom_ids)
        if True:
            return make_response('', 200)
    return make_response('', 400)


@app.route('/return/<deal_id>')
def return_deal(deal_id: int):
    user = get_user_from_session(session)
    # Done: check if the user made this deal and if it can be returned (date and if not returned already)
    res = comm.get_admin_deal(deal_id)
    if res:
        can_be_returned = (res["successful"])
        # Done: make DB request to return deal
        if can_be_returned:
            if comm.change_user_cancel_deal(deal_id):
                return user.render('result_messages/success.j2', -1, message="Угоду успішно відмінено")
    return user.render('result_messages/fail.j2', -1, message="Угоду не вдалося відмінити. Перевірте, чи вона "
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
        # Done: make request to DB here
        return jsonify(comm.get_user_items(min_price=min_price, max_price=max_price, min_age=min_age))
        # return jsonify(({"name": 'Best hemp', 'price': '128', 'pack': '15', 'min_age': 18, 'id': 1},
        #                 {"name": 'Best hemp 2', 'price': '100', 'pack': '5', 'min_age': 16, 'id': 2},
        #                 {"name": 'Cool hemp', 'price': '10145', 'pack': '1', 'min_age': 0, 'id': 3}))
    elif user.role == UserRole.ADMIN.value:
        min_distinct_buyers = data['minDistinctBuyers']
        min_date = data['minDate']
        max_date = data['maxDate']
        return (jsonify(comm.get_admin_items(min_distinct_buyers=min_distinct_buyers, min_date=min_date, max_date=max_date)))
        return jsonify(({'id': 4, 'name': 'Best hemp', 'return_percent': '15', 'pack': 1, 'price': 16, 'min_age': 18},))
    elif user.role == UserRole.AGRONOMIST.value:
        # Done: request to DB here. Need only names and ids
        return jsonify(comm.get_goods())


@app.route('/get_orders', methods=['POST'])
def get_orders():
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:
        user_id = user.id
        filters = request.get_json()

        # Обережно з формаом дати. В запиті вона у форматі "yyyy-mm-dd"
        min_date = filters['minDate']
        max_date = filters['maxDate']
        # Done: Request to db here
        return jsonify(comm.get_user_orders(user_id, min_date, max_date))



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
        return jsonify(comm.get_user_agronoms(user_id, min_buys, max_buys, min_degustations, max_degustations))
    elif user.role == UserRole.AGRONOMIST.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        return jsonify(comm.get_agronom_agronoms(user.id, min_date, max_date))

        # return jsonify(({"id": 0, "full_name": "Osta Dyhdalovych", "location": "Lviv", "rating": "10", "trips": 5},))
    elif user.role == UserRole.ADMIN.value:
        min_sorts = data['minSorts']
        min_date = data['minDate']
        max_date = data['maxDate']
        return jsonify(comm.get_admin_agronoms(min_sorts, min_date, max_date))


@app.route('/get_feed_backs', methods=['POST'])
def get_feed_backs():
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:  # Бо різні запити до БД для покупця і, наприклад, агронома
        user_id = user.id
        data = request.get_json()
        min_date = data['minDate']
        max_date = data['maxDate']
        res = comm.get_user_feedbacks(user_id, date_from=min_date, date_to=max_date)
        print(res)
        return jsonify(res)


@app.route('/get_degustations', methods=['POST'])
def get_degustations():
    user = get_user_from_session(session)
    data = request.get_json()
    user_id = user.id
    if user.role == UserRole.BUYER.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        agronom_name = data['agronomName']
        return jsonify(comm.get_user_degustations(
            user_id, min_date, max_date, agronom_name))

      
    elif user.role == UserRole.AGRONOMIST.value:
        print(data)
        min_date = data['minDate']
        max_date = data['maxDate']
        product_name = data['productName'] or ''
        min_buyers = int(data['minBuyers'])
        print(product_name)
        # Done: Request to DB here
        res = comm.get_agronom_degustations(
            user_id, min_date, max_date, product_name, min_buyers)
        print(res)
        return jsonify(res)
        # return jsonify(({'id': 1, 'product_name': 'Cool hemp', 'testers': ['Ostap', 'Vlad', 'Denys'],
        #                  'date': '2020-06-06', 'amount': '1'},))


@app.route('/get_all_buyers', methods=['POST'])
def get_all_buyers():
    return jsonify(comm.get_all_buyers())

@app.route('/get_buyers', methods=['POST'])
def get_buyers():
    user = get_user_from_session(session)
    data = request.get_json()
    if user.role == UserRole.AGRONOMIST.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        min_buys = data['minBuys']
        max_buys = data['maxBuys']

        return jsonify( comm.agronom_buyers(user.id, min_date, max_date, min_buys, max_buys) )

    if user.role == UserRole.ADMIN.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        min_buys = data['minBuys']

        # TODO: Request to DB here
        # return jsonify()
        return jsonify(comm.get_admin_buyers(min_buys, min_date, max_date))
        return jsonify(({'id': 0, 'full_name': 'Ostap', 'buys': 10, 'location': 'Lviv'},))


@app.route('/get_trips', methods=['POST'])
def get_trips():
    user = get_user_from_session(session)
    if user.role == UserRole.AGRONOMIST.value:
        data = request.get_json()
        user_id = user.id
        min_date = data['minDate']
        max_date = data['maxDate']

        trips = comm.get_agronom_trips(agronom_id=user_id, date_from=min_date, date_to=max_date)
        return jsonify(trips)
        # return jsonify(({'id': 0, 'with': ['Ostap', 'Denys', 'Vlad', 'Anya'], 'departion': '2020-05-06',
        #                  'arrival': '2020-05-07', 'location': 'Lviv'},))


@app.route('/get_sorts', methods=['POST'])
def get_sorts():
    user = get_user_from_session(session)
    data = request.get_json()
    if user.role == UserRole.ADMIN.value:
        min_date = data['minDate']
        max_date = data['maxDate']
        min_harvesting = data['minHarvesting']
        res = comm.get_sorts_by_harvesting(min_harvesting, min_date, max_date)
        return jsonify(res)
    if user.role == UserRole.AGRONOMIST.value:
        res = comm.get_sorts()
        return jsonify(res)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return get_user_from_session(session).render('result_messages/fail.j2', -1, message="Сторінку не знайдено..")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1200)
    # app.run(host='localhost', debug=True, port=1200)

