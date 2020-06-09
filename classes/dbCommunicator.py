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
            (f" and author = {user_id}" if not(user_id is None) else "")
        sql_req += \
            (f" and made >= '{date_from}'" if not(date_from is None) else "") +\
            (f" and made <= '{date_to}'" if not(date_to is None) else "")
        # Done: Add date to feed_back table
        sql_req += ";"
        self.cursor.execute(sql_req)
        return [{"agronom_id": line[0], "message":line[1], "order_id":line[2], "date":line[3], "id":line[3]} for line in self.cursor.fetchall()]

    def add_user_feedback(self, user_id, message, agronom, order_id, date=None):
        sql_req = "INSERT INTO feed_back (author, message, about_order, about, feed_back.made) VALUES" +\
            f"({user_id}, '{message}', {order_id}, {agronom}, '{date}'')" +\
            ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    #TODO:    # def get_user_agronoms(self, )


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

    def get_admin_items(self, id=None, name = None, pack=None, price=None, min_age=None) -> tuple:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE True" + \
                  (f" and id = {id}" if not(id is None) else "") +\
                  (f" and name = {name}" if not(name is None) else "") +\
                  (f" and pack = {pack}" if not(pack is None) else "") +\
                  (f" and price  = {price}" if not(price is None) else "") +\
                  (f" and min_age = {min_age}" if not(min_age is None) else "") +\
                  ";"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "pack":line[2], "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]

    # def get_admin_agronom(self, id=None, mail=None, password=None, name=None, surname=None, phone=None, bank_account=None, location=None):
    #     sql_req = f"SELECT id, mail, password, name, surname, phone, bank_account, location from person where True" +\
    #         (f" and (id = {id})" if id else "") +\
    #         (f" and (mail = '{mail}')" if mail else "") +\
    #         (f" and (password = '{password}')" if password else "") +\
    #         (f" and (name = '{name}')" if name else "") +\
    #         (f" and (surname = '{surname}')" if surname else "") +\
    #         (f" and (phone = '{phone}')" if phone else "") +\
    #         (f" and (bank_account = '{bank_account}')" if bank_account else "") +\
    #         (f" and (location = '{location}')" if location else "") +\
    #         ";"

    def get_admin_hemp(self, id=None, sort_name=None, days_growtime=None, crop_capacity=None, frost_resistance=None):
        sql_req = "SELECT sort_id, sort_name, days_growtime, crop_capacity, frost_resistance FROM hemp WHERE TRUE"+\
            (f" and (sort_id = {id})" if not(id is None)  else "") +\
            (f" and (sort_name = '{sort_name}'')" if not(sort_name is None)  else "") +\
            (f" and (days_growtime = {days_growtime})" if not(days_growtime is None)  else "") +\
            (f" and (crop_capacity = {crop_capacity})" if not(crop_capacity is None)  else "") +\
            (f" and (frost_resistance = {frost_resistance})" if not(frost_resistance is None)  else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "sort_name":line[1], "days_growtime":line[2], "crop_capacity":line[3], "frost_resistance":line[4]} for line in self.cursor.fetchall()]

    def get_admin_deal(self, id=None, seller=None, buyer=None, made=None, successful=None, item=None, amount_of_product=None):
        sql_req = "SELECT id, seller, buyer, made, successful, item, amount_of_product FROM deals WHERE TRUE"+\
            (f" and (id = {id})" if not(id is None)  else "") +\
            (f" and (seller = {seller})" if not(seller is None)  else "") +\
            (f" and (buyer = {buyer})" if not(buyer is None)  else "") +\
            (f" and (made = '{made}'')" if not(made is None)  else "") +\
            (f" and (successful = {successful})" if not(successful is None)  else "") +\
            (f" and (item = {item})" if not(item is None)  else "") +\
            (f" and (amount_of_product = {amount_of_product})" if not(amount_of_product is None)  else "") +\
            ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "seller":line[1], "buyer":line[2], "made":line[3], "successful":line[4], "item":line[5], "amount_of_product":line[6]} for line in self.cursor.fetchall()]


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
# ----------------------------------------------------Helper
    def get_item(self, item_id) -> dict:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE id={item_id}"
        self.cursor.execute(sql_req)
        res = [{"name": line[0], "price":line[1], "pack":line[2], "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]
        return res[0] if res else None

    def get_person_id(self, mail, password=None):
        sql_req = f"SELECT id from person where True" +\
            f" and (mail = '{mail}') " +\
            (f" and (password = '{password}')" if password else "") +\
            ";"
        print(mail, " ", password)
        self.cursor.execute(sql_req)
        for line in self.cursor.fetchall():
            return line[0]
        return None

    def __del__(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    # comm = dbCommunicator("db_weed")
    comm = dbCommunicator("db14", host="142.93.163.88",
                          port=6006, user="team14", password="pas1swo4rd")

    # sql_req = f"SELECT * from feed_back;"
    # # sql_req = """select table_schema, table_name from information_schema.tables where (table_schema = 'public')"""
    # comm.cursor.execute(sql_req)
    # print("\n".join([str(line) for line in comm.cursor.fetchall()]))

    # print(datetime.date(2019, 9, 9))
    # print("\n".join(str(dict) for dict in comm.get_user_items(min_age=18)))
    # print("\n".join(str(dict) for dict in comm.get_user_orders(user_id=22)))
    # print("\n".join(str(dict) for dict in comm.get_user_feedbacks(user_id=22, date_from = (datetime.date(1919, 9, 9)))))

    # print("\n".join(str(dict) for dict in comm.get_user_feedbacks(
    #     user_id=22, date_from=(datetime.date(1919, 9, 9)))))
    print("\n".join(str(dict) for dict in comm.get_admin_hemp(id=1)))

    # print(comm.get_person_id(mail = "wterry@gmail.com", password="Wenday"))
