import psycopg2


class DBCommunicator:
    def __init__(self, db_name: str, user="postgres", password="postgres", host="localhost"):
        self.connection = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host)
        self.cursor = self.connection.cursor()
        return

    def get_goods(self, min_price=0, max_price=100000, min_age=0) -> tuple:
        sql_req = f"""select name, price, pack, min_age, id from product where price >= {min_price} and price <= {max_price} and min_age >={min_age};"""
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price":line[1], "pack":line[2], "min_age":line[3], "id":line[4]} for line in self.cursor.fetchall()]

    def __del__(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    comm = DBCommunicator("db_weed")
    print("\n".join(str(dict) for dict in comm.get_goods(min_age=18)))
