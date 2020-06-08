from classes.users import User
from classes.users import UserRole
from flask import render_template


class NoUser(User):
    def __init__(self):
        super().__init__(0, '', '', UserRole.NO_USER)

    def render_default(self):
        return render_template('welcome/welcome.html')

    def render_login(self):
        return render_template("log_in/log_in.html")
