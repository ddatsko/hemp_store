from classes.users.user import User
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

    def render_buyers(self):
        return render_template('buyer/buyer_buy.j2', top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements,
                               selected=0, full_name=self.full_name)

    def render_default(self):
        return self.render_buyers()

    def __dict__(self):
        return {'user_id': self.id,
                'full_name': self.full_name,
                'email': self.email,
                'role': self.role}
