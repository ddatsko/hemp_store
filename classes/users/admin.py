from classes.users import User
from classes.users import UserRole
from flask import render_template


class Admin(User):
    top_nav_elements = ({'link': '/make_trip', 'text': 'Нове відрядження'},
                        {'link': '/logout', 'text': 'Log Out'})
    left_nav_elements = (
        {'link': '/buyers', 'text': 'Покупці'},
        {'link': '/agronoms', 'text': 'Агрономи'},
        {'link': '/sorts', 'text': 'Сорти коноплі'},
        {'link': '/products', 'text': 'Продукти'})

    def __init__(self, user_id: int, full_name: str, email: str, role: int = UserRole.ADMIN.value):
        super().__init__(user_id, full_name, email, role)

    def render_default(self):
        return self.render_buyers()

    def render_buyers(self):
        return self.render('admin/admin_buyers.j2', 0)

    def render_agronoms(self):
        return self.render('admin/admin_agronoms.j2', 1)

    def render_sorts(self):
        return self.render('admin/admin_sorts.j2', 2)

    def render_products(self):
        return self.render('admin/admin_products.j2', 3)

    def render_make_trip(self):
        return render_template('item_creations/trip_creation.j2', top_nav_elements=self.top_nav_elements)
