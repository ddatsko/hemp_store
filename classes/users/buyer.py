from classes.users.user import User
from classes.users.user_role import UserRole
from flask import render_template


class Buyer(User):
    top_nav_elements = ({'link': '/logout', 'text': 'Log Out'},)
    left_nav_elements = (
        {'link': '/buy', 'text': 'Купити коноплю'},
        {'link': '/orders', 'text': 'Мої замовлення'},
        {'link': '/agronoms', 'text': 'Агрономи'},
        {'link': '/feed_backs', 'text': 'Мої відгуки'},
        {'link': '/degustations', 'text': 'Дегустації'},
    )

    def __init__(self, user_id: int, full_name: str, email: str, role=UserRole.BUYER.value):
        super().__init__(user_id, full_name, email, role)

    def __render(self, template_filename: str, selected: int):
        return render_template(template_filename, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements,
                               selected=selected, full_name=self.full_name)

    def render_buyers(self):
        return self.__render('buyer/buyer_buy.j2', 0)

    def render_default(self):
        return self.render_buyers()

    def render_orders(self):
        return self.__render('buyer/buyer_orders.j2', 1)

    def render_agronoms(self):
        return self.__render('buyer/buyer_agronoms.j2', 2)

    def render_feed_backs(self):
        return self.__render('buyer/buyer_feed_backs.j2', 3)

    def render_degustations(self):
        return self.__render('buyer/buyer_degustations.j2', 4)
