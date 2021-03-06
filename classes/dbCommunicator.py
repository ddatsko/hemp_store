import psycopg2
import datetime


def js_date_to_sql(date: str):
    year, month, day = date.split('-')
    return f'{month}/{day}/{year}'


class dbCommunicator:
    def __init__(self, db_name: str, user="postgres", password="postgres", host="localhost", port=5432):
        self.connection = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

        return

    def get_user_items(self, min_price=None, max_price=None, min_age=None) -> tuple:
        sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE True" + \
                  (f" and price >= {min_price}" if not (min_price is None) else "") + \
                  (f" and price <= {max_price}" if not (max_price is None) else "") + \
                  (f" and min_age >= {min_age}" if not (min_age is None) else "") + \
                  ";"
        self.cursor.execute(sql_req)
        return [{"name": line[0], "price": line[1], "pack": line[2], "min_age": line[3], "id": line[4]} for line in
                self.cursor.fetchall()]

    def get_user_orders(self, user_id=None, date_from=None, date_to=None):
        sql_select_deals = f"""
            SELECT deals.id, product.name, person.name, person.surname, deals.amount_of_product, deals.made, deals.successful, product.id
            FROM deals
                     INNER JOIN product ON deals.item = product.id
                     INNER JOIN person ON deals.seller = person.id
            WHERE deals.buyer = {user_id} AND deals.made > '{js_date_to_sql(date_from)}' AND deals.made < '{js_date_to_sql(date_to)}';"""
        try:
            self.cursor.execute(sql_select_deals)
            return [{"id": line[0], "name": line[1], "seller": f'{line[2]} {line[3]}', "successful": line[6],
                     "amount": line[4],
                     "made": line[5], "product_id": line[7]} for line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()

    # def get_user_agronoms(self, user_id, min_deals, max_deals, min_degustations, max_degustations):
    #     pass

    def get_user_feedbacks(self, user_id=None, date_from=None, date_to=None):
        try:
            sql_req = f"""
                SELECT feed_back.id, feed_back.message, person.name, person.surname, product.name
                    FROM feed_back
                             LEFT JOIN person on person.id = feed_back.about
                             LEFT JOIN deals on feed_back.about_order = deals.id
                             LEFT JOIN product on deals.item = product.id
                    WHERE feed_back.made < '{js_date_to_sql(date_to)}'
                      AND feed_back.made > '{js_date_to_sql(date_from)}' AND feed_back.author = {user_id};
            """
            self.cursor.execute(sql_req)
            return [{'id': line[0], 'agronom_name': f'{line[2] or ""} {line[3] or ""}', 'message': line[1],
                     'product_name': line[4] or ''}
                    for
                    line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()

    def get_user_degustations(self, user_id, date_from, date_to, agronom_name):
        print(agronom_name)
        sql_req = f"""
            SELECT foo.id, foo.name, p2.name
            FROM (select testing_table.id, testing_table.tester, testing_table.seller, p.name
                  FROM testing_table
                           INNER JOIN product p on testing_table.product = p.id
                  WHERE testing_table.tester = {user_id}
                    AND testing_table.made < '{js_date_to_sql(date_to)}'
                    AND testing_table.made > '{js_date_to_sql(date_from)}') as foo
                     LEFT JOIN degustations d on foo.id = d.deal_id
                     LEFT JOIN person p2 on d.tester_id = p2.id
                     LEFT JOIN person seller ON foo.seller = seller.id
            WHERE seller.name ilike '%{agronom_name}%'
               OR seller.surname ilike '%{agronom_name}%'
            ORDER BY id;
        """
        try:
            self.cursor.execute(sql_req)
            req_res = self.cursor.fetchall()
            cur_id = -1
            cur_obj = {}
            res = []
            for line in req_res:
                if line[0] == cur_id:
                    cur_obj['with'].append(line[2])
                else:
                    if cur_obj:
                        res.append(cur_obj)
                    cur_obj = {'id': line[0], 'product_name': line[1], 'with': [line[2]]}
                    cur_id = cur_obj['id']
            if cur_obj:
                res.append(cur_obj)
            return res
        except Exception as e:
            print(e)

    def add_agronom_feed_back(self, user_id: int, message: str, agronom_id: int) -> bool:
        sql_req = f"""
                INSERT INTO feed_back (about, author, message, made)
                VALUES ({agronom_id}, {user_id}, '{message}', current_date);
                """
        try:
            self.cursor.execute(sql_req)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def agronom_buyers(self, id, start_date, fin_date, min_count=0, max_count=10000):

        sql_req = f"""
                    select distinct buyer, b.name, b.surname, p.location, count(buyer), count(foo.tester) as tests from deals inner join agronom on deals.seller = agronom.id
                    inner join person p on agronom.id = p.id inner join person b on deals.buyer = b.id left outer join

                    (select tester, count(tester) from testing_table inner join degustations d on testing_table.id = d.deal_id
                    where seller = 11 and made >= '01/01/2000' and made <= '01/01/2025' group by tester) as foo on buyer = foo.tester

                    group by buyer, made, b.name, b.surname, seller, p.location HAVING count(buyer) >= {min_count}
                    and count(buyer) <= {max_count} and seller = {id} and made >= '{start_date}' and made <= '{fin_date}';
                    """

        try:
            self.cursor.execute(sql_req)
            self.connection.commit()

            return [{'id': line[0], 'full_name': f'{line[1]} {line[2]}',
                     'buys': line[4], 'degustations': line[5], 'location': line[3]} for line in self.cursor.fetchall()]

            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

        # return [{'id': line[0], 'full_name': f'{line[1]} {line[2]}',
        #          'location': line[3]} for line in self.cursor.fetchall()]

    def add_deal_feed_back(self, user_id: int, message: str, deal_id: int) -> bool:
        sql_req = f"""
                INSERT INTO feed_back (about_order, author, message, made)
                VALUES ({deal_id}, {user_id}, '{message}', current_date);

                """
        try:
            self.cursor.execute(sql_req)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False


    def get_goods(self):
        sql_req = """SELECT id, name FROM product"""
        try:
            self.cursor.execute(sql_req)
            return [{'id': line[0], 'name': line[1]} for line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()

    def get_all_buyers(self):
        sql_req = """SELECT person.id, person.name, person.surname FROM person INNER JOIN buyer ON buyer.id = person.id;"""
        try:
            self.cursor.execute(sql_req)
            return [{'id': line[0], 'name': f'{line[1]} {line[2]}'} for line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()

    def add_user_order(self, user_id, product_id, date=None):
        try:
            product = self.get_item(product_id)
            if not product:
                return -1
            packing = self.get_admin_packing(product["pack"])[0]
            if not packing:
                return -1
            sql_req = "INSERT INTO deals (seller, buyer, successful, item, amount_of_product) VALUES " + \
                      f"({packing['manufacturer']}, {user_id}, true, {product_id}, {packing['capacity_gr']})" + \
                      ";"

            self.cursor.execute(sql_req)
            self.cursor.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
            return -1
        return 0

    def change_user_cancel_deal(self, deal_id) -> bool:
        sql_req = f"""
            UPDATE deals
                SET successful = false
                WHERE id = {deal_id};"""
        try:
            self.cursor.execute(sql_req)
            return True
        except Exception as e:
            print(e)

            self.connection.rollback()
            return False

    def get_user_agronoms(self, user_id, min_deals, max_deals, min_degustations, max_degustations):
        print(min_deals)
        sql_select_agronoms = f"""
            SELECT agronom.id,
                   COALESCE(buys.buys, 0),
                   COALESCE(degustations.degustations, 0),
                   CONCAT(person.name, ' ', person.surname),
                   person.location,
                   agronom.reputation
            FROM agronom
                     LEFT JOIN
                 (SELECT agronom.id, count(agronom.id), 0 AS buys
                  FROM agronom 
                           INNER JOIN deals on agronom.id = deals.seller AND deals.buyer = {user_id}
                  GROUP BY agronom.id) as buys on agronom.id = buys.id
                     LEFT JOIN
                 (SELECT agronom.id, count(agronom.id) AS degustations
                  FROM agronom
                           INNER JOIN testing_table on agronom.id = testing_table.seller AND testing_table.tester = {user_id}
                  GROUP BY agronom.id) as degustations on agronom.id = degustations.id
                     INNER JOIN person on person.id = agronom.id  WHERE COALESCE(buys.buys, 0) >= {min_deals} AND COALESCE(buys.buys, 0) <= {max_deals} AND 
                    COALESCE(degustations.degustations, 0) >= {min_degustations} AND COALESCE(degustations.degustations, 0) <= {max_degustations};"""
        try:
            self.cursor.execute(sql_select_agronoms)
            return [{'id': line[0], 'full_name': line[3], 'buys': line[1], 'degustations': line[2],
                     'rating': line[5], 'location': line[4]} for line in self.cursor.fetchall()]
        except:
            self.connection.rollback()

    def get_agronom_agronoms(self, agronom_id, min_date, max_date):
        min_date = js_date_to_sql(min_date)
        max_date = js_date_to_sql(max_date)
        sql_req = f"""
            select distinct vacations.member, person.name, person.surname, person.location, agronom.reputation from
                vacations
            inner join
                (select distinct with_agronom.id as vacation from
                    (select distinct vacation as id from vacations where member = {agronom_id})with_agronom
                        inner join
                    (select distinct id from vacation where (departion >= '{min_date}' and arrival <= '{max_date}'))within_date
                    on with_agronom.id = within_date.id
                )chosen
            on vacations.vacation = chosen.vacation INNER JOIN agronom on vacations.member = agronom.id INNER JOIN person on vacations.member = person.id;
            """
        self.cursor.execute(sql_req)
        return [{'id': line[0], 'full_name': f'{line[1]} {line[2]}',
                 'location': line[3], 'rating': line[4]} for line in self.cursor.fetchall()]

    # -------------------------------------------------------------------------------Admin functions
    def get_admin_agronoms(self, min_sorts, min_date, max_date):
        print(min_sorts)

        sql_req = f"""SELECT person.name, person.surname, person.location, foo.id, foo.count, foo.reputation
                        FROM (SELECT agronom.id, count(distinct store_and_spend.sort), agronom.reputation
                              FROM agronom
                                       INNER JOIN store_and_spend
                                                  on agronom.id = store_and_spend.owner
                              WHERE store_and_spend.operation_day <= '{js_date_to_sql(max_date)}'
                                AND store_and_spend.operation_day >= '{js_date_to_sql(min_date)}'
                                AND NOT store_and_spend.take
                              GROUP BY agronom.id
                              HAVING count(distinct store_and_spend.sort) >= {min_sorts}) as foo
                                 INNER JOIN person on person.id = foo.id;"""
        self.cursor.execute(sql_req)

        return [{'id': line[3], 'full_name': f'{line[0]} {line[1]}',
                 'location': line[2], 'rating': line[5], 'sorts': line[4]} for line in self.cursor.fetchall()]

    # -------------------------------------------------------------------------------Agronom functions

    def get_agronom_degustations(self, agronom_id, date_from, date_to, product_name, min_buyers):
        print(product_name)
        sql_req = f"""
                SELECT foo.id, foo.name, p2.name, foo.amount, foo.made
                FROM (select testing_table.id, testing_table.tester, testing_table.seller, p.name, testing_table.amount, testing_table.made
                      FROM testing_table
                               INNER JOIN product p on testing_table.product = p.id
                      WHERE testing_table.seller = {agronom_id}
                        AND testing_table.made
                          < '{js_date_to_sql(date_to)}'
                        AND testing_table.made
                          > '{js_date_to_sql(date_from)}') as foo
                         LEFT JOIN degustations d on foo.id = d.deal_id
                         INNER JOIN person p2 on d.tester_id = p2.id
                         LEFT JOIN person seller ON foo.seller = seller.id
                WHERE foo.name ilike '%{product_name}%'
                ORDER BY id;
        """
        try:
            self.cursor.execute(sql_req)
            req_res = self.cursor.fetchall()
            cur_id = -1
            cur_obj = {}
            res = []
            for line in req_res:
                if line[0] == cur_id:
                    cur_obj['testers'].append(line[2])
                else:
                    if cur_obj and len(cur_obj['testers']) >= min_buyers:
                        res.append(cur_obj)
                    cur_obj = {'id': line[0], 'product_name': line[1], 'testers': [line[2]], 'amount': line[3],
                               'date': line[4]}
                    cur_id = cur_obj['id']
            if cur_obj and len(cur_obj['testers']) >= min_buyers:
                res.append(cur_obj)
            return res
        except Exception as e:
            print(e)

    def get_agronom_trips(self, agronom_id, date_from, date_to):
        sql_req = f"""
            SELECT vacation.id, person.name, person.surname, vacation.departion, vacation.arrival, vacation.purpose, f.location
            FROM person
                     INNER JOIN vacations ON person.id = vacations.member INNER JOIN (SELECT vacation FROM vacations
                                 WHERE member = {agronom_id}) AS agronom_vacations ON vacations.vacation=agronom_vacations.vacation
                    INNER JOIN vacation on vacations.vacation = vacation.id
                    INNER JOIN field f on vacation.destination = f.id WHERE vacation.departion < '{js_date_to_sql(date_to)}' AND vacation.arrival > '{js_date_to_sql(date_from)}' ORDER BY vacation.id;

                """
        try:
            self.cursor.execute(sql_req)
            req_res = self.cursor.fetchall()
            cur_id = -1
            cur_obj = {}
            res = []
            for line in req_res:
                if line[0] == cur_id:
                    cur_obj['with'].append(f'{line[1]} {line[2]}')
                else:
                    if cur_obj:
                        res.append(cur_obj)
                    cur_obj = {'id': line[0], 'departion': line[3], 'arrival': line[4], 'location': line[6],
                               'with': [f'{line[1]} {line[2]}']}
                    cur_id = cur_obj['id']
            if cur_obj:
                res.append(cur_obj)
            return res
        except Exception as e:
            print(e)

    def add_agronom_crop(self, owner, sort, amount, operation_day, take) -> bool:
        sql_req = "INSERT INTO store_and_spend (owner, sort, amount, operation_day, take) VALUES" + \
                  f"({owner}, '{sort}', {amount}, '{js_date_to_sql(operation_day)}', {take})" + \
                  ";"
        try:
            self.cursor.execute(sql_req)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def add_agronom_degustation(self, agronom_id, made, product_id, amount, testers) -> bool:
        sql_req = "INSERT INTO testing_table(seller, made, successful, product, amount) VALUES " + \
                  f"({agronom_id}, '{js_date_to_sql(made)}', True, '{product_id}', {amount})" + \
                  "RETURNING id;"
        try:
            self.cursor.execute(sql_req)
            degustation_id = self.cursor.fetchall()
            degustation_id = degustation_id[0][0]
            self.connection.commit()
            print(degustation_id)

            for tester in testers:
                query = f"""INSERT INTO degustations (deal_id, tester_id) VALUES ({degustation_id}, {tester})"""
                self.cursor.execute(query)
                self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def get_admin_agronom(self, id=None):
        sql_req = f"SELECT person.id, mail, password, name, surname, phone, bank_account, person.location, agronom.debt, agronom.reputation from person INNER JOIN agronom on (agronom.id = person.id) WHERE True" + \
                  (f" and (id = {id})" if id else "") + \
                  ";"
        try:
            self.cursor.execute(sql_req)
            return [
                {"id": line[0], "mail": line[1], "name": line[3], "surname": line[4], "phone": line[5],
                 "bank_account": line[6], "location": line[7], "debt": line[8], "reputation": line[9]} for line in
                self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()
            return []

    # def add_agronom_to_vacation(self, agronom_id, vacation_id):
    #     sql_req = "INSERT INTO vaations(member, vacation)"

    # -------------------------------------------------------------------------------Admin functions

    def get_admin_person(self, id=None, mail=None, password=None, name=None, surname=None, phone=None,
                         bank_account=None, location=None):
        sql_req = f"SELECT id, mail, password, name, surname, phone, bank_account, location from person where True" + \
                  (f" and (id = {id})" if id else "") + \
                  (f" and (mail = '{mail}')" if mail else "") + \
                  (f" and (password = '{password}')" if password else "") + \
                  (f" and (name = '{name}')" if name else "") + \
                  (f" and (surname = '{surname}')" if surname else "") + \
                  (f" and (phone = '{phone}')" if phone else "") + \
                  (f" and (bank_account = '{bank_account}')" if bank_account else "") + \
                  (f" and (location = '{location}')" if location else "") + \
                  ";"
        print(mail, " ", password)
        self.cursor.execute(sql_req)
        return [
            {"id": line[0], "mail": line[1], "password": line[2], "name": line[3], "surname": line[4], "phone": line[5],
             "bank_account": line[6], "location": line[7]} for line in self.cursor.fetchall()]

# def get_admin_items(self, id=None, name=None, pack=None, price=None, min_age=None) -> tuple:
    #     sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE True" + \
    #               (f" and id = {id}" if not (id is None) else "") + \
    #               (f" and name = {name}" if not (name is None) else "") + \
    #               (f" and pack = {pack}" if not (pack is None) else "") + \
    #               (f" and price  = {price}" if not (price is None) else "") + \
    #               (f" and min_age = {min_age}" if not (min_age is None) else "") + \
    #               ";"
    #     self.cursor.execute(sql_req)
    #     return [{"name": line[0], "price": line[1], "pack": line[2], "min_age": line[3], "id": line[4]} for line in
#             self.cursor.fetchall()]

    def get_admin_items(self, min_distinct_buyers, min_date, max_date):
        sql_req = f"""select item,
                        p.name,
                        cast(count(*) filter ( where not successful ) as decimal) / count(*) as percent,
                        p.pack,
                        p.price,
                        p.min_age
                    FROM deals
                        inner join product p on p.id = item
                    WHERE made > '{js_date_to_sql(min_date)}'
                        and made < '{js_date_to_sql(max_date)}'
                    group by p.name,
                        deals.item,
                        p.pack,
                        p.price,
                        p.min_age
                    having count(distinct buyer) >= {min_distinct_buyers}
                    order by cast(
                            count(*) filter ( where not successful ) as decimal) / count(*) desc;
                    """
        self.cursor.execute(sql_req)
        res = [{"id": line[0], "name": line[1], "return_percent": str(int(line[2]*100))+"%", "pack": line[3], "price": line[4], "min_age":line[5]} for line in
                self.cursor.fetchall()]
        # print(res)
        return res


    def get_admin_packing(self, id):
        sql_req = f"SELECT id, capacity_gr, price, manufacturer FROM packing WHERE True" + \
                  (f" and id = {id}" if not (id is None) else "") + \
                  ";"
        self.cursor.execute(sql_req)
        return [{"id": line[0], "capacity_gr": line[1], "price": line[2], "manufacturer": line[3]} for line in
                self.cursor.fetchall()]

    # def get_admin_agronom(self, id=None):
    #     sql_req = f"SELECT person.id, mail, password, name, surname, phone, bank_account, person.location, agronom.debt, agronom.reputation from person INNER JOIN agronom on (agronom.id = person.id) WHERE True" + \
    #               (f" and (id = {id})" if id else "") + \
    #               ";"
    #     try:
    #         self.cursor.execute(sql_req)
    #         return [
    #             {"id": line[0], "mail": line[1], "name": line[3], "surname": line[4], "phone": line[5],
    #              "bank_account": line[6], "location": line[7], "debt": line[8], "reputation": line[9]} for line in
    #             self.cursor.fetchall()]
    #     except Exception as e:
    #         print(e)
    #         self.connection.rollback()
    #         return []

    # def get_admin_agronoms(self, min_sorts, min_date, max_date):
    #     sql_req = f"""select buyer,
    #                     p.name,
    #                     p.surname,
    #                     p.location,
    #                     p.rating,
    #                     count(),
    #                     p.reputation
    #                 from deals
    #                     inner join person p on deals.buyer = p.id
    #                 where made > '01/01/2000'
    #                     and made < '01/01/2021'
    #                 group by buyer,
    #                     p.name,
    #                     p.surname,
    #                     p.location
    #                 having count(distinct item) >= 2;"""
    #     self.cursor.execute(sql_req)
    #     return [{'id': line[3], 'full_name': f'{line[0]} {line[1]}',
    #         'location': line[2], 'rating': line[5], 'sorts': line[4]} for line in self.cursor.fetchall()]



    def get_admin_buyer(self, id=None):
        sql_req = f"SELECT person.id, mail, password, name, surname, phone, bank_account, agronom.location, buyer.money from person INNER JOIN agronom on (buyer.id = buyer.id) WHERE True" + \
                  (f" and (id = {id})" if id else "") + \
                  ";"
        # (f" and (mail = '{mail}')" if mail else "") +\
        # (f" and (password = '{password}')" if password else "") +\
        # (f" and (name = '{name}')" if name else "") +\
        # (f" and (surname = '{surname}')" if surname else "") +\
        # (f" and (phone = '{phone}')" if phone else "") +\
        # (f" and (bank_account = '{bank_account}')" if bank_account else "") +\
        # (f" and (location = '{location}')" if location else "") +\
        self.cursor.execute(sql_req)
        return [
            {"id": line[0], "mail": line[1], "password": line[2], "name": line[3], "surname": line[4], "phone": line[5],
             "bank_account": line[6], "location": line[7], "money": line[7]} for line in self.cursor.fetchall()]

    # def get_admin_hemp(self, id=None, sort_name=None, days_growtime=None, crop_capacity=None, frost_resistance=None):
    #     sql_req = "SELECT sort_id, sort_name, days_growtime, crop_capacity, frost_resistance FROM hemp WHERE TRUE" + \
    #               (f" and (sort_id = {id})" if not (id is None) else "") + \
    #               (f" and (sort_name = '{sort_name}'')" if not (sort_name is None) else "") + \
    #               (f" and (days_growtime = {days_growtime})" if not (days_growtime is None) else "") + \
    #               (f" and (crop_capacity = {crop_capacity})" if not (crop_capacity is None) else "") + \
    #               (f" and (frost_resistance = {frost_resistance})" if not (frost_resistance is None) else "") + \
    #               ";"
    #     self.cursor.execute(sql_req)
    #     return [{"id": line[0], "sort_name": line[1], "days_growtime": line[2], "crop_capacity": line[3],
    #              "frost_resistance": line[4]} for line in self.cursor.fetchall()]

    # def get_admin_hemp():
    #     sql_req = f"""select current_sort,
    #                     p.name,
    #                     p.
    #                     cast (a.harvest_taken as decimal) / count(current_sort) as harvest_per_vacations
    #                 from vacation
    #                     inner join vacations v on vacation.id = v.vacation
    #                     inner join field f on vacation.destination = f.id
    #                     inner join product p on p.id = current_sort
    #                     inner join (
    #                         select sort,
    #                             count(sort) as harvest_taken
    #                         from store_and_spend
    #                         group by sort
    #                     ) as a on current_sort = a.sort
    #                 where arrival > '01/01/2000'
    #                     and arrival < '01/01/2025'
    #                 group by p.name,
    #                     current_sort,
    #                     a.harvest_taken
    #                 having count(current_sort) >= 2
    #                 order by harvest_per_vacations;"""
    #     self.cursor.execute(sql_req)
    #     return [{"id":line[0], "full_name":f'{line[1]} {line[2]}', "buys":line[3], "location":line[4]} for line in sqlf.cursor.fetchall()]

    def get_admin_deal(self, deal_id):
        sql_req = f"SELECT id, seller, buyer, made, successful, item, amount_of_product FROM deals WHERE deals.id = {deal_id};"

        try:
            self.cursor.execute(sql_req)
            return [{"id": line[0], "seller": line[1], "buyer": line[2], "made": line[3], "successful": line[4],
                     "item": line[5], "amount_of_product": line[6]} for line in self.cursor.fetchall()][0]
        except:
            self.connection.rollback()

    def get_admin_trip(self, id=None, destination=None, departion=None, arrival=None, purpose="-"):
        sql_req = "SELECT id, destination, departion, arrival, purpose FROM vacation WHERE TRUE" + \
                  (f" and (id = {id})" if not (id is None) else "") + \
                  (f" and (destination = '{destination}')" if not (destination is None) else "") + \
                  (f" and (departion = '{departion}')" if not (departion is None) else "") + \
                  (f" and (arrival = '{arrival}')" if not (arrival is None) else "") + \
                  (f" and (arrival = '{arrival}')" if not (arrival is None) else "") + \
                  (f" and (purpose = '{purpose}')" if not (purpose is None) else "") + \
                  ";"
        self.cursor.execute(sql_req)
        vacations = [{"id": line[0], "destination": line[1], "departion": line[2],
                      "arrival": line[3], "purpose": line[4]} for line in self.cursor.fetchall()]

        for vacation in vacations:
            sql_req = f"SELECT id, name FROM vacations INNER JOIN people ON people.id = vacations.member WHERE vacations.vacation = {vacation['id']};"
            self.cursor.execute(sql_req)
            vacation["people"] = [line[1] for line in self.cursor.fetchall()]
        return vacations

    def get_trip_info(self, trip_id: int):
        sql_req = f"""
            SELECT person.name, person.surname, vacation.departion, vacation.arrival, vacation.purpose, f.location
            FROM person
                     INNER JOIN vacations on person.id = vacations.member
                     INNER JOIN
                 vacation ON vacation.id = vacations.vacation
                     INNER JOIN field f on vacation.destination = f.id
            WHERE vacation.id = {trip_id};
        """
        try:
            self.cursor.execute(sql_req)
            sql_res = self.cursor.fetchall()
            res = {'Agronoms': [], 'item_name': sql_res[0][5], 'Departion': sql_res[0][2], 'Arrival': sql_res[0][3],
                   'Purpose': sql_res[0][4]}
            res['Agronoms'] = [f'{line[0]} {line[1]}' for line in sql_res]
            return res

        except Exception as e:
            print(e)
            self.connection.rollback()

    def add_deal(self, user_id: int, product_id: int, agronom_id: int, amount: int) -> bool:
        try:
            sql_req = f"""
                INSERT INTO deals (seller, buyer, made, successful, item, amount_of_product)
                VALUES ({agronom_id}, {user_id}, current_date, True, {product_id}, {amount})
            """
            self.cursor.execute(sql_req);
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def get_admin_trip_peers(self, trip_id, agronom_id=None):
        sql_req = "SELECT person.id, person.name from person INNER JOIN vacations ON person.id = vacations.member WHERE True" + \
                  (f" and vacations.vacation = {trip_id}" if not (trip_id is None) else "") + \
                  (f" and person.id != {agronom_id}" if not (agronom_id is None) else "") + \
                  ";"

        self.cursor.execute(sql_req)
        return [{"id": line[0], "name": line[1]} for line in self.cursor.fetchall()]

    def get_admin_degustation(self, degustation_id):
        sql_req = f"""
                SELECT person.name, person.surname, p.name
            FROM person
                     INNER JOIN testing_table ON person.id = testing_table.seller
                     INNER JOIN product p on testing_table.product = p.id
            WHERE testing_table.id = {degustation_id};
            """
        try:
            self.cursor.execute(sql_req)
            res = self.cursor.fetchall()
            return [{'seller_name': f'{res[0][0]} {res[0][1]}', 'product_name': res[0][2]}]
        except Exception as e:
            print(e)
            self.connection.rollback()

    def get_admin_degustation_peers(self, degustation_id: int) -> list:
        sql_req = f"""
            SELECT person.name, person.surname
            FROM person
                     INNER JOIN degustations ON person.id = degustations.tester_id
                     INNER JOIN
                 testing_table ON degustations.deal_id = testing_table.id
            WHERE testing_table.id = {degustation_id};
            """
        try:
            self.cursor.execute(sql_req)
            return [f'{line[0]} {line[1]}' for line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()

    def add_admin_trip(self, destination, departion, arrival, purpose="-", agronoms=[]):
        sql_req = "INSERT into VACATION (destination, departion, arrival, purpose) VALUES" + \
                  f"({destination},'{departion}','{arrival}','{purpose}'" + \
                  "RETURNING id;"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        trip_id = self.cursor.fetchone()[0]
        self.add_admin_trip_agronoms(trip_id, agronoms)
        return 0

    def add_admin_trip_agronoms(self, vacation_id, agronoms):
        sql_req = "INSERT INTO vacations (member, vacation) VALUES" + \
                  "\n".join([f"({agronom_id}, {vacation_id})"] for agronom_id in agronoms) + \
                  ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_degustation_testers(self, degustation_id, testers):
        sql_req = "INSERT INTO degustations (deal_id, user_id) VALUES" + \
                  "\n".join([f"({degustation_id}, {user_id})"] for user_id in testers) + \
                  ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    def add_admin_person(self, name, surname, phone, bank_account, mail, password, location):
        sql_req = "INSERT into person (name, surname, phone, bank_account, mail, password, location) VALUES" + \
                  f"('{name}','{surname}','{phone}','{bank_account}','{mail}', '{password}', '{location}')" + \
                  ";"

        self.cursor.execute(sql_req)
        self.connection.commit()
        return 0

    def add_admin_seller(self, id, productivity_per_month=0):
        sql_req = "INSERT into packing_seller(id, productivity_per_month) VALUES" + \
                  f"({id},{productivity_per_month})" + \
                  ";"
        self.cursor.execute(sql_req)
        self.connection.commit()
        return 0

    def add_admin_agronom(self, id, debt=0, reputation=0):
        sql_req = "INSERT into agronom(id, debt, reputation) VALUES" + \
                  f"({id},{debt}, {reputation})" + \
                  ";"

        self.cursor.execute(sql_req)
        self.connection.commit()
        return 0

    def add_admin_buyer(self, id, money=0):
        sql_req = "INSERT into buyer(id, money) VALUES" + \
                  f"({id},{money})" + \
                  ";"

        self.cursor.execute(sql_req)
        self.connection.commit()
        return 0

    def get_admin_buyers(self, min_buys, min_date, max_date):
        sql_req = f"""select buyer,
                        p.name,
                        p.surname,
                        count(distinct item),
                        p.location
                    from deals
                        inner join person p on deals.buyer = p.id
                    where made > '{js_date_to_sql(min_date)}'
                        and made < '{js_date_to_sql(max_date)}'
                    group by buyer,
                        p.name,
                        p.surname,
                        p.location
                    having count(distinct item) >= {min_buys};"""
        self.cursor.execute(sql_req)
        return [{"id":line[0], "full_name":f'{line[1]} {line[2]}', "buys":line[3], "location":line[4]} for line in self.cursor.fetchall()]


    def add_admin_hemp(self, sort_name, days_growtime, crop_capacity, frost_resistance):
        sql_req = "INSERT into hemp(sort_name, days_growtime, crop_capacity, frost_resistance) VALUES" + \
                  f"('{sort_name}',{days_growtime}, {crop_capacity}, {frost_resistance})" + \
                  ";"
        self.cursor.execute(sql_req)
        self.cursor.commit()
        return 0

    # def add_admin_degustation(self, )

    # ----------------------------------------------------Helper
    def get_item(self, item_id) -> dict:
        try:
            sql_req = f"SELECT name, price, pack, min_age, id FROM product WHERE id={item_id}"
            self.cursor.execute(sql_req)
            res = [{"name": line[0], "price": line[1], "pack": line[2],
                    "min_age": line[3], "id": line[4]} for line in self.cursor.fetchall()]
            return res[0] if res else None
        except Exception as e:
            print(e)
            self.connection.rollback()

    def is_role(self, mail, i):
        roles = ['agronom', 'buyer', 'packing_seller', 'admin']
        id = self.get_person_id(mail)
        sql_req = f"SELECT id from {roles[i]} where (id = '{id}') " + ";"
        self.cursor.execute(sql_req)
        for line in self.cursor.fetchall():
            return line[0]
        return None

    def get_user_info(self, user_id):
        sql_req = f"""SELECT name, surname, mail FROM person WHERE id = {user_id}"""
        try:
            self.cursor.execute(sql_req)
            res = self.cursor.fetchall()
            return {'full_name': f'{res[0][0]} {res[0][1]}', 'mail': res[0][2]}
        except Exception as e:
            print(e)
            self.connection.rollback()

    def get_person_id(self, mail, password=None):
        sql_req = f"""
            SELECT id FROM person 
                WHERE mail = '{mail}' """ + \
                  (f"AND password = '{password}'" if password is not None else '')
        try:
            self.cursor.execute(sql_req)
            for line in self.cursor.fetchall():
                return line[0]
            return None

        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def get_person_name(self, mail):
        sql_req = f"SELECT name, surname from person WHERE (mail = '{mail}') ;"

        self.cursor.execute(sql_req)
        for line in self.cursor.fetchall():
            return line[0] + " " + line[1] + " "
        return None

    def get_sorts_by_harvesting(self, min_harvesting, date_from, date_to):
        sql_req = f"SELECT current_sort, sort_name, cast (a.harvest_taken as decimal) / count(current_sort) as harvest_per_vacations FROM vacation" + \
                  f" INNER JOIN vacations v ON vacation.id = v.vacation" + \
                  f" INNER JOIN field f on vacation.destination = f.id" + \
                  f" INNER JOIN hemp p on p.sort_id = current_sort" + \
                  f" INNER JOIN (SELECT sort, count(sort) as harvest_taken FROM store_and_spend GROUP BY sort) as a ON current_sort = a.sort" + \
                  f" WHERE true" + \
                  (f" and arrival > '{js_date_to_sql(date_from)}'" if not (date_from is None) else "") + \
                  (f" and arrival < '{js_date_to_sql(date_to)}'" if not (date_from is None) else "") + \
                  " GROUP BY sort_name, current_sort, a.harvest_taken HAVING true" + \
                  (f" and count(current_sort) >= {min_harvesting}" if not (min_harvesting is None) else "") + \
                  "ORDER BY harvest_per_vacations;"
        try:
            self.cursor.execute(sql_req)
            return [{"id": line[0], "name": line[1], "average_trips": str(line[2])[:3]} for line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_sorts(self):
        sql_req = """SELECT sort_id, sort_name FROM hemp;"""
        try:
            self.cursor.execute(sql_req)
            return [{'id': line[0], 'name': line[1]} for line in self.cursor.fetchall()]
        except Exception as e:
            print(e)
            self.connection.rollback()


if __name__ == "__main__":
    # comm = dbCommunicator("db_weed")
    comm = dbCommunicator("db14", host="142.93.163.88",
                          port=6006, user="team14", password="pas1swo4rd")

    sql_req = f"SELECT * FROM admin;"
    # sq
    # sql_req = """select table_schema, table_name from information_schema.tables where (table_schema = 'public')"""
    # sql_req = """INSERT INTO admin(id) VALUES
    #             ();
    # """
    comm.cursor.execute(sql_req)
    # comm.connection.commit()
    print("\n".join([str(line) for line in comm.cursor.fetchall()]))
    # comm.add_admin_person("Eru", "Iluvatar", "123456789", "12345678", "admin@admin.com", "eru", "Valinor")
    res = comm.get_admin_person()
    print("\n".join(str(dict) for dict in res))
    # print(datetime.date(2019, 9, 9))
    # print("\n".join(str(dict) for dict in comm.get_user_items(min_age=18)))
    # print("\n".join(str(dict) for dict in comm.get_user_orders(user_id=22)))
    # print("\n".join(str(dict) for dict in comm.get_user_feedbacks(user_id=22, date_from = (datetime.date(1919, 9, 9)))))

    # print("\n".join(str(dict) for dict in comm.get_user_feedbacks(
    #     user_id=22, date_from=(datetime.date(1919, 9, 9)))))
    # print("\n".join(str(dict) for dict in comm.get_admin_hemp(id=1)))

    # print(comm.get_person_id(mail = "wterry@gmail.com", password="Wenday"))
