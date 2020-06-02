from flask import Flask, session, redirect, jsonify, request
from utils import get_user_from_session
from classes.users import Buyer, UserRole

app = Flask(__name__)
app.secret_key = b'HeLl0ThisIsRand0m8ytesHemp_st0resoCOOOOll'


@app.route('/')
def title_page():
    # if there is a logged in user
    session['user'] = Buyer(0, 'Name Surname', 'email').__dict__()
    user = get_user_from_session(session)
    return user.render_buyers()


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
    user = get_user_from_session(session)
    if user.role == UserRole.BUYER.value:  # Превірка, бо в цьому випадку треба знайти спільні покупки та дегустації
        user_id = user.id
        data = request.get_json()
        min_buys = data['minBuys']
        max_buys = data['maxBuys']
        min_degustations = data['minDegustations']
        max_degustations = data['maxDegustations']
        # TODO: request to DB, using fields above here
        return jsonify(({"id": 0, "full_name": "Ostap Dyhdalovych", "location": "Lviv", "rating": "10", "buys": 10,
                         "degustations": 1},))


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
    if user.role == UserRole.BUYER.value:
        data = request.get_json()
        user_id = user.id
        min_date = data['minDate']
        max_date = data['maxDate']
        agronom_name = data['agronomName']
        # TODO: make request to BD using fields above
        return jsonify(({"id": 0, "product_name": "Cool hemp", "with": ['Denys', 'Ostap', 'Vlad', 'Anna']},))


if __name__ == '__main__':
    app.run(debug=True, port=1200)
