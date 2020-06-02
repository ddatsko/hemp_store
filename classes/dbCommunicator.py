import psycopg2
import datetime

class DBCommunicator:
    def __init__(self, db_name: str, user="postgres", password="postgres", host="localhost"):
        self.connection = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host)
        self.cursor = self.connection.cursor()
        return

    def get_item(self, item_id)->dict:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE id={item_id}"
        self.cursor.execute(sql_req)

    def get_user_items(self, min_price=None, max_price=None, min_age=None) -> tuple:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE True"+ \
                  (f" and price >= {min_price}" if not(min_price is None) else "")+\
                  (f" and price <= {max_price}" if not(max_price is None) else "")+\
                  (f" and min_age >= {min_age}" if not(min_age is None) else "")+\
                  ";"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "pack":line[2], "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]

    def get_user_orders(self, user_id=None,  date_from=None, date_to=None):
        sql_select_deals = f"SELECT id, made, successful, item, amount_of_product FROM deals WHERE True" +\
            (f" and buyer = {user_id}" if not(user_id is None) else "") +\
            (f" and made >= '{date_from}'" if not(date_from is None) else "")+\
            (f" and made <= '{date_to}'" if not(date_to is None) else "")+\
            ""
        sql_req = f"SELECT product.name, product.price, cdeals.made, cdeals.successful, cdeals.amount_of_product, cdeals.id, cdeals.item FROM ({sql_select_deals})cdeals INNER JOIN product ON cdeals.item = product.id;"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "date":line[2], "successful":line[3], "amount":line[4], "deal_id":line[5], "product_id":line[6]} for line in self.cursor.fetchall()]

    # def get_user_agronoms(self, user_id, min_deals, max_deals, min_degustations, max_degustations):
    #     pass
    
    def get_user_feedbacks(self, user_id=None, date_from = None, date_to=None):
        sql_req = "SELECT about, message, about_order, id from feed_back WHERE True"+\
            (f" and author = {user_id}" if not(user_id is None) else "")
        # sql_req += \
        #     (f" and made >= '{date_from}'" if not(date_from is None) else "")+\
        #     (f" and made <= '{date_to}'" if not(date_to is None) else "")
        # TODO: Add date to feed_back table
        sql_req += ";"
        self.cursor.execute(sql_req)
        return [{"about_agronom":line[0], "message":line[1], "about_order":line[2], "id":line[3]} for line in self.cursor.fetchall()]

    def add_user_feedback():
        pass


    def __del__(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    comm = DBCommunicator("db_weed")
    # print(datetime.date(2019, 9, 9))
    print("\n".join(str(dict) for dict in comm.get_user_items(min_age=18)))
    print("\n".join(str(dict) for dict in comm.get_user_orders(user_id=22)))
    print("\n".join(str(dict) for dict in comm.get_user_feedbacks(user_id=22)))
