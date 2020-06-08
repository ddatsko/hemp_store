from classes.users.user_role import UserRole
from flask import redirect
from flask import render_template

class User:
    def __init__(self, user_id: int, full_name: str, email: str, role: UserRole):
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

    def __dict__(self):
        return {'user_id': self.id,
                'full_name': self.full_name,
                'email': self.email,
                'role': self.role}
