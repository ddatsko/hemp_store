from classes.users.user_role import UserRole
from flask import redirect

class User:
    def __init__(self, user_id: int, full_name: str, email: str, role=UserRole.BUYER):
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

    def render_degustations(selfself):
        return redirect('/')
