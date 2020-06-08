from classes.users.user_role import UserRole
from flask import redirect
from flask import render_template


class User:
    top_nav_elements = {}
    left_nav_elements = {}

    def __init__(self, user_id: int, full_name: str, email: str, role: int):
        self.id = user_id
        self.full_name = full_name
        self.email = email
        self.role = role

    def render_default(self):
        return redirect('/')

    def render_buyers(self):
        return redirect('/')

    def render_orders(self):
        return redirect('/')

    def render_agronoms(self):
        return redirect('/')

    def render_feed_backs(self):
        return redirect('/')

    def render_degustations(self):
        return redirect('/')

    def render_trips(self):
        return redirect('/')

    def render_login(self):
        return redirect('/')

    def render_sorts(self):
        return redirect('/')

    def render_products(self):
        return redirect('/')

    def __dict__(self):
        return {'user_id': self.id,
                'full_name': self.full_name,
                'email': self.email,
                'role': self.role}

    def _render(self, template_filename: str, selected: int):
        return render_template(template_filename, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements,
                               selected=selected, full_name=self.full_name)
