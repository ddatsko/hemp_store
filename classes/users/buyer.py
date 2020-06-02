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

    def render_buyers(self):
        return render_template('buyer/buyer_buy.j2', top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements,
                               selected=0, full_name=self.full_name)

    def render_default(self):
        return self.render_buyers()

    def render_orders(self):
        return render_template('buyer/buyer_orders.j2', selected=1, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements, full_name=self.full_name)

    def render_agronoms(self):
        return render_template('buyer/buyer_agronoms.j2', selected=2, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements, full_name=self.full_name)

    def render_feed_backs(self):
        return render_template('buyer/buyer_feed_backs.j2', selected=3, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements, full_name=self.full_name)

    def render_degustations(self):
        return render_template('buyer/buyer_degustations.j2', selected=4, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements, full_name=self.full_name)

    def __dict__(self):
        return {'user_id': self.id,
                'full_name': self.full_name,
                'email': self.email,
                'role': self.role}
