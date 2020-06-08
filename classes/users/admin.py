from classes.users import User
from classes.users import UserRole


class Admin(User):
    top_nav_elements = ({'link': '/logout', 'text': 'Log Out'},)
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
        return self._render('admin/admin_buyers.j2', 0)

    def render_agronoms(self):
        return self._render('admin/admin_agronoms.j2', 1)

    def render_sorts(self):
        return self._render('admin/admin_sorts.j2', 2)

    def render_products(self):
        return self._render('admin/admin_products.j2', 3)




