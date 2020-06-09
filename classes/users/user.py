from classes.users.user_role import UserRole
from flask import redirect
from flask import render_template, abort
from typing import Dict


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
        return abort(404)

    def render_orders(self):
        return abort(404)

    def render_agronoms(self):
        return abort(404)

    def render_feed_backs(self):
        return abort(404)

    def render_degustations(self):
        return abort(404)

    def render_trips(self):
        return abort(404)

    def render_login(self):
        return abort(404)

    def render_sorts(self):
        return abort(404)

    def render_products(self):
        return abort(404)

    def render_make_trip(self):
        return abort(404)

    def render_item_view(self, info: Dict[str, str]):
        return self.render('item_views/item_view.j2', -1, info=info)

    def __dict__(self):
        return {'user_id': self.id,
                'full_name': self.full_name,
                'email': self.email,
                'role': self.role}

    def render(self, template_filename: str, selected: int, **kwargs):
        return render_template(template_filename, top_nav_elements=self.top_nav_elements,
                               left_nav_elements=self.left_nav_elements,
                               selected=selected, full_name=self.full_name, **kwargs)
