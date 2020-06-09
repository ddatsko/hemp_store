import psycopg2
import datetime


class dbCommunicator:
    def __init__(self, db_name: str, user="postgres", password="postgres", host="localhost", port=5432):
        self.connection = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()
        return

    def get_user_items(self, min_price=None, max_price=None, min_age=None) -> tuple:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE True" + \
                  (f" and price >= {min_price}" if not(min_price is None) else "") +\
                  (f" and price <= {max_price}" if not(max_price is None) else "") +\
                  (f" and min_age >= {min_age}" if not(min_age is None) else "") +\
                  ";"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "pack":line[2], "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]

    def get_user_orders(self, user_id=None,  date_from=None, date_to=None):
        sql_select_deals = f"SELECT id, made, successful, item, amount_of_product FROM deals WHERE True" +\
            (f" and buyer = {user_id}" if not(user_id is None) else "") +\
            (f" and made >= '{date_from}'" if not(date_from is None) else "") +\
            (f" and made <= '{date_to}'" if not(date_to is None) else "") +\
            ""
        sql_req = f"SELECT product.name, product.price, cdeals.made, cdeals.successful, cdeals.amount_of_product, cdeals.id, cdeals.item FROM ({sql_select_deals})cdeals INNER JOIN product ON cdeals.item = product.id;"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "date":line[2], "successful":line[3], "amount":line[4], "deal_id":line[5], "product_id":line[6]} for line in self.cursor.fetchall()]

    # def get_user_agronoms(self, user_id, min_deals, max_deals, min_degustations, max_degustations):
    #     pass

    def get_user_feedbacks(self, user_id=None, date_from=None, date_to=None):
        sql_req = "SELECT about, message, about_order, feed_back.made, id from feed_back WHERE True" +\
            (f" and author = {user_id}" if not(user_id is None) else "") +\
            (f" and made >= '{date_from}'" if not(date_from is None) else "") +\
            (f" and made <= '{date_to}'" if not(date_to is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"agronom_id": line[0], "message":line[1], "order_id":line[2], "date":line[3], "id":line[3]} for line in self.cursor.fetchall()]

    def get_user_degustations(self, user_id=None,  date_from=None, date_to=None):
        sql_req = "SELECT id, seller, tester, made, product from testing_table WHERE True" +\
            (f" and author = {user_id}" if not(user_id is None) else "") +\
            (f" and made >= '{date_from}'" if not(date_from is None) else "") +\
            (f" and made <= '{date_to}'" if not(date_to is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "seller":line[1], "tester":line[2], "made":line[3], "product":line[3]} for line in self.cursor.fetchall()]


    def add_user_feedback(self, user_id, message, agronom="", order_id="NULL", date=None):
        sql_req = "INSERT INTO feed_back (author, message, about_order, about, feed_back.made) VALUES" +\
            f"({user_id}, '{message}', {order_id}, {agronom}, '{date}'')" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_user_order(self, user_id, product_id, date=None):
        product = self.get_item(product_id)
        if(not product):
            return -1
        packing = self.get_admin_packing(product[0]["pack"])
        if(not packing):
            return -1
        sql_req = "INSERT INTO deals (seller, buyer, successful, item, amount_of_product) VALUES"+\
            f"{packing['manufacturer']}, {user_id}, true, {product_id}, {packing['capacity_gr']}"+\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def change_user_cancel_deal(self, deal_id):
        sql_req = "UPDATE deals\n"+\
                "SET successful=false\n"+\
                f"WHERE id={deal_id};"

# #
#     def get_user_agronoms(self, user_id=None, min_buys=None, max_buys=None, min_degustations=None, max_degustations=None):
#         sql_req = "SELECT p.id, p.name, p.surname from person inner_join "

# -------------------------------------------------------------------------------Agronom functions


    def get_agronom_degustations(self, agronom_id, date_from=None, date_to=None, product_name=None, min_buyers=None):
        sql_req = "SELECT id, seller, tester, made, product.name from testing_table"+\
            "INNER JOIN (SELECT deal_id, count(tester_id) as num_testers, FROM degustations)counts ON testing_table.id = counts.deal_id"+\
            (f" INNER JOIN product ON product.id = testing_table.product WHERE True") +\
            (f" and seller = {agronom_id}" if not(agronom_id is None) else "") +\
            (f" and made >= '{date_from}'" if not(date_from is None) else "") +\
            (f" and made <= '{date_to}'" if not(date_to is None) else "") +\
            (f" and product.name = '{product_name}'" if not(product_name is None) else "") +\
            (f" and counts.num_testers >= '{min_buyers}'" if not(min_buyers is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "seller":line[1], "tester":line[2], "made":line[3], "product_name":line[3]} for line in self.cursor.fetchall()]


    def get_agronom_trips(self, agronom_id, date_from=None, date_to=None):
        sql_req = "SELECT id, destination, departion, arrival, from vacation"+\
            (f"INNER JOIN vacations ON vacations.vacation = vacation.id WHERE True")+\
            (f" and vacations.member={agronom_id}" if not(agronom_id is None) else "") +\
            (f" and departion >= '{date_from}'" if not(date_from is None) else "") +\
            (f" and arrival <= '{date_to}'" if not(date_to is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "destination":line[1], "departion":line[2], "arrival":line[3]} for line in self.cursor.fetchall()]

    
    def add_agronom_crop(self, owner, sort, amount, operation_day, take):
        sql_req = "INSERT INTO feed_back (owner, sort, amount, operation_day, take) VALUES" +\
            f"({owner}, '{sort}', {amount}, '{operation_day}', {take})" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0
    
    def add_agronom_degustation(self, agronom_id, tester, made, successful, product, amount, testers):
        sql_req = "INSERT INTO testing_table(seller, tester, made, successful, product, amount) VALUES" +\
            f"({agronom_id}, {tester}, '{made}', '{successful}',{product}, {amount})"+\
            "RETURNING id;"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        degustation_id = self.cursor.fetchone()[0]
        add_admin_degustation_testers(degustation_id, testers)
        return 0

    
    
    # def add_agronom_to_vacation(self, agronom_id, vacation_id):
    #     sql_req = "INSERT INTO vaations(member, vacation)"

# -------------------------------------------------------------------------------Admin functions


    def get_admin_person(self, id=None, mail=None, password=None, name=None, surname=None, phone=None, bank_account=None, location=None):
        sql_req = f"SELECT id, mail, password, name, surname, phone, bank_account, location from person where True" +\
            (f" and (id = {id})" if id else "") +\
            (f" and (mail = '{mail}')" if mail else "") +\
            (f" and (password = '{password}')" if password else "") +\
            (f" and (name = '{name}')" if name else "") +\
            (f" and (surname = '{surname}')" if surname else "") +\
            (f" and (phone = '{phone}')" if phone else "") +\
            (f" and (bank_account = '{bank_account}')" if bank_account else "") +\
            (f" and (location = '{location}')" if location else "") +\
            ";"
        print(mail, " ", password)
        self.cursor.execute(sql_req)
        return [{"id": line[0], "mail":line[1], "password":line[2], "name":line[3], "surname":line[4], "phone":line[5], "bank_account":line[6], "location":line[7]} for line in self.cursor.fetchall()]

    def get_admin_items(self, id=None, name=None, pack=None, price=None, min_age=None) -> tuple:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE True" + \
                  (f" and id = {id}" if not(id is None) else "") +\
                  (f" and name = {name}" if not(name is None) else "") +\
                  (f" and pack = {pack}" if not(pack is None) else "") +\
                  (f" and price  = {price}" if not(price is None) else "") +\
                  (f" and min_age = {min_age}" if not(min_age is None) else "") +\
                  ";"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "pack":line[2], "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]

    def get_admin_packing(self, id):
        sql_req = f"SELECT id, capacity_gr, price, manufacturer FROM packing WHERE True" + \
                  (f" and id = {id}" if not(id is None) else "") +\
                  ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "capacity_gr":line[1], "price":line[2], "manufacturer":line[3]} for line in self.cursor.fetchall()]

    def get_admin_agronom(self, id=None):
        sql_req = f"SELECT person.id, mail, password, name, surname, phone, bank_account, agronom.location, agronom.debt, agronom.reputation from person INNER JOIN agronom on (agronom.id = person.id) WHERE True" +\
            (f" and (id = {id})" if id else "") +\
            ";"
        # (f" and (mail = '{mail}')" if mail else "") +\
        # (f" and (password = '{password}')" if password else "") +\
        # (f" and (name = '{name}')" if name else "") +\
        # (f" and (surname = '{surname}')" if surname else "") +\
        # (f" and (phone = '{phone}')" if phone else "") +\
        # (f" and (bank_account = '{bank_account}')" if bank_account else "") +\
        # (f" and (location = '{location}')" if location else "") +\
        self.cursor.execute(sql_req)
        return [{"id": line[0], "mail":line[1], "password":line[2], "name":line[3], "surname":line[4], "phone":line[5], "bank_account":line[6], "location":line[7], "debt":line[7], "reputation":line[8]} for line in self.cursor.fetchall()]

    def get_admin_buyer(self, id=None):
        sql_req = f"SELECT person.id, mail, password, name, surname, phone, bank_account, agronom.location, buyer.money,  from person INNER JOIN agronom on (buyer.id = buyer.id) WHERE True" +\
            (f" and (id = {id})" if id else "") +\
            ";"
        # (f" and (mail = '{mail}')" if mail else "") +\
        # (f" and (password = '{password}')" if password else "") +\
        # (f" and (name = '{name}')" if name else "") +\
        # (f" and (surname = '{surname}')" if surname else "") +\
        # (f" and (phone = '{phone}')" if phone else "") +\
        # (f" and (bank_account = '{bank_account}')" if bank_account else "") +\
        # (f" and (location = '{location}')" if location else "") +\
        self.cursor.execute(sql_req)
        return [{"id": line[0], "mail":line[1], "password":line[2], "name":line[3], "surname":line[4], "phone":line[5], "bank_account":line[6], "location":line[7], "money":line[7]} for line in self.cursor.fetchall()]

    def get_admin_hemp(self, id=None, sort_name=None, days_growtime=None, crop_capacity=None, frost_resistance=None):
        sql_req = "SELECT sort_id, sort_name, days_growtime, crop_capacity, frost_resistance FROM hemp WHERE TRUE" +\
            (f" and (sort_id = {id})" if not(id is None) else "") +\
            (f" and (sort_name = '{sort_name}'')" if not(sort_name is None) else "") +\
            (f" and (days_growtime = {days_growtime})" if not(days_growtime is None) else "") +\
            (f" and (crop_capacity = {crop_capacity})" if not(crop_capacity is None) else "") +\
            (f" and (frost_resistance = {frost_resistance})" if not(frost_resistance is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "sort_name":line[1], "days_growtime":line[2], "crop_capacity":line[3], "frost_resistance":line[4]} for line in self.cursor.fetchall()]

    def get_admin_deal(self, id=None, seller=None, buyer=None, made=None, successful=None, item=None, amount_of_product=None):
        sql_req = "SELECT id, seller, buyer, made, successful, item, amount_of_product FROM deals WHERE TRUE" +\
            (f" and (id = {id})" if not(id is None) else "") +\
            (f" and (seller = {seller})" if not(seller is None) else "") +\
            (f" and (buyer = {buyer})" if not(buyer is None) else "") +\
            (f" and (made = '{made}'')" if not(made is None) else "") +\
            (f" and (successful = {successful})" if not(successful is None) else "") +\
            (f" and (item = {item})" if not(item is None) else "") +\
            (f" and (amount_of_product = {amount_of_product})" if not(amount_of_product is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "seller":line[1], "buyer":line[2], "made":line[3], "successful":line[4], "item":line[5], "amount_of_product":line[6]} for line in self.cursor.fetchall()]

    def get_admin_trip(self, id=None, destination=None, departion=None, arrival=None, purpose="-"):
        sql_req = "SELECT id, destination, departion, arrival, purpose FROM vacation WHERE TRUE" +\
            (f" and (id = {id})" if not(id is None) else "") +\
            (f" and (destination = '{destination}')" if not(destination is None) else "") +\
            (f" and (departion = '{departion}')" if not(departion is None) else "") +\
            (f" and (arrival = '{arrival}')" if not(arrival is None) else "") +\
            (f" and (arrival = '{arrival}')" if not(arrival is None) else "") +\
            (f" and (purpose = '{purpose}')" if not(purpose is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        vacations = [{"id": line[0], "destination":line[1], "departion":line[2],
                      "arrival":line[3], "purpose":line[4]} for line in self.cursor.fetchall()]
        for vacation in vacations:
            sql_req = f"SELECT id, name FROM vacations INNER JOIN people ON people.id = vacations.member WHERE vacations.vacation = {vacation['id']};"
            self.cursor.execute(sql_req)
            vacation["people"] = [line[1] for line in self.cursor.fetchall()]
        return vacations

    def get_admin_trip_peers(self, trip_id, agronom_id=None):
        sql_req = "SELECT person.id, person.name from person INNER JOIN vacations ON person.id = vacations.member WHERE True" +\
            (f" and vacations.vacation = {trip_id}" if not(trip_id is None) else "") +\
            (f" and person.id != {agronom_id}" if not(agronom_id is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "name":line[1]} for line in self.cursor.fetchall()]
    
    def get_admin_degustation(self, id = None, seller_id=None, product_id=None, product_name=None, date=None):
        sql_req = "SELECT testing_table.id, seller, tester, made, testing_table.product, product.name, person.name from testing_table"+\
            " INNER JOIN product ON product.id = testing_table.product"+\
            " INNER JOIN person ON person.id = testing_table.seller WHERE True" +\
            (f" and testing_table.id = {id}" if not(id is None) else "") +\
            (f" and author = {seller_id}" if not(seller_id is None) else "") +\
            (f" and made = '{date}'" if not(date is None) else "") +\
            (f" and testing_table.product <= {product_id}" if not(product_id is None) else "") +\
            (f" and product.name = {product_name}'" if not(product_name is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "seller":line[1], "tester":line[2], "made":line[3], "product":line[3], "product_name":line[4], "seller_name":line[5]} for line in self.cursor.fetchall()]

    def get_admin_degustation_peers(self, degustation_id, user_id=None):
        sql_req = "SELECT person.id, person.name from person INNER JOIN degustations ON person.id = degustations.tester_id WHERE True" +\
            (f" and degustations.deal_id = {degustation_id}" if not(degustation_id is None) else "") +\
            (f" and person.id != {user_id}" if not(user_id is None) else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "name":line[1]} for line in self.cursor.fetchall()]

    def add_admin_trip(self, destination, departion, arrival, purpose="-", agronoms=[]):
        sql_req = "INSERT into VACATION (destination, departion, arrival, purpose) VALUES" +\
                  f"({destination},'{departion}','{arrival}','{purpose}'" +\
            "RETURNING id;"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        trip_id = self.cursor.fetchone()[0]
        add_admin_trip_agronoms(trip_id, agronoms)
        return 0

    def add_admin_trip_agronoms(self, vacation_id, agronoms):
        sql_req = "INSERT INTO vacations (member, vacation) VALUES" +\
            "\n".join([f"({agronom_id}, {vacation_id})"] for agronom_id in agronoms)+\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_degustation_testers(self, degustation_id, testers):
        sql_req = "INSERT INTO degustations (deal_id, user_id) VALUES" +\
            "\n".join([f"({degustation_id}, {user_id})"] for user_id in testers)+\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0
    
    def add_admin_person(self, mail, password, name, surname='', phone='', bank_account='', **kwargs):
        sql_req = "INSERT into person (name, surname, phone, bank_account, mail, password) VALUES" +\
                  f"('{name}',,'{surname}','{phone}','{bank_account}','{mail}', '{password})" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_seller(self, id, productivity_per_month=0, location=""):
        sql_req = "INSERT into seller(id, productivity_per_month, location) VALUES" +\
            f"({id},{productivity_per_month},'{location}')" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_agronom(self, id, location="", debt=0, reputation=0):
        sql_req = "INSERT into seller(id, location, debt, reputation) VALUES" +\
            f"({id},{location},{debt}, {reputation})" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_buyer(self, id, money=0, location=""):
        sql_req = "INSERT into seller(id, money, location) VALUES" +\
            f"({id},{money},'{location}')" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_hemp(self, sort_name, days_growtime, crop_capacity, frost_resistance):
        sql_req = "INSERT into hemp(sort_name, days_growtime, crop_capacity, frost_resistance) VALUES" +\
            f"('{sort_name}',{days_growtime}, {crop_capacity}, {frost_resistance})" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0


    # def add_admin_degustation(self, )

# ----------------------------------------------------Helper
    def get_item(self, item_id) -> dict:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE id={item_id}"
        self.cursor.execute(sql_req)
        res = [{"name": line[0], "price":line[1], "pack":line[2],
                "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]
        return res[0] if res else None

    def get_person_id(self, mail, password=None):
        sql_req = f"SELECT id from person where True" +\
            f" and (mail = '{mail}') " +\
            (f" and (password = '{password}')" if password else "") +\
            ";"
        # print(mail, " ", password)
        self.cursor.execute(sql_req)
        for line in self.cursor.fetchall():
            return line[0]
        return None

    def get_sorts_by_harvesting(self, min_harvesting, date_from, date_to):
        sql_req = f"SELECT current_sort, p.name, cast (a.harvest_taken as decimal) / count(current_sort) as harvest_per_vacations FROM vacation"+\
            f" INNER JOIN vacations v ON vacation.id = v.vacation"+\
            f" INNER JOIN field f on vacation.destination = f.id"+\
            f" INNER JOIN product p on p.id = current_sort" +\
            f" INNER JOIN (SELECT sort, count(sort) as harvest_taken FROM store_and_spend GROUP BY sort) as a ON current_sort = a.sort"+\
            f" WHERE true"+\
            (f" and arrival > '{date_from}'" if not(date_from is None) else "")+\
            (f"and arrival < '{date_to}''"if not(date_from is None) else "")+\
            "GROUP BY p.name, current_sort, a.harvest_taken HAVING true"+\
                (f" and count(current_sort) >= {min_harvesting}"if not(min_harvesting is None) else "")+\
                "ORDER BY harvest_per_vacations;"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "name":line[1], "average_trips":line[2]} for line in self.cursor.fetchall()]
        

    def __del__(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    # comm = dbCommunicator("db_weed")
    comm = dbCommunicator("db14", host="142.93.163.88",
                          port=6006, user="team14", password="pas1swo4rd")

    sql_req = f"SELECT deal_id FROM degustations;"
    # # sql_req = """select table_schema, table_name from information_schema.tables where (table_schema = 'public')"""
    comm.cursor.execute(sql_req)
    print("\n".join([str(line) for line in comm.cursor.fetchall()]))

    # print(datetime.date(2019, 9, 9))
    # print("\n".join(str(dict) for dict in comm.get_user_items(min_age=18)))
    # print("\n".join(str(dict) for dict in comm.get_user_orders(user_id=22)))
    # print("\n".join(str(dict) for dict in comm.get_user_feedbacks(user_id=22, date_from = (datetime.date(1919, 9, 9)))))

    # print("\n".join(str(dict) for dict in comm.get_user_feedbacks(
    #     user_id=22, date_from=(datetime.date(1919, 9, 9)))))
    # print("\n".join(str(dict) for dict in comm.get_admin_hemp(id=1)))

    # print(comm.get_person_id(mail = "wterry@gmail.com", password="Wenday"))
