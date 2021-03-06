from classes.users import User
from flask import render_template
from classes.users import UserRole


class Agronom(User):
    top_nav_elements = ({'link': '/make_degustation', 'text': 'Нова дегустація'},
                        {'link': '/gather_crop', 'text': 'Новий врожай'},
                        {'link': '/logout', 'text': 'Вийти'})
    left_nav_elements = (
        {'link': '/buyers', 'text': 'Покупці'},
        {'link': '/agronoms', 'text': 'Агрономи'},
        {'link': '/trips', 'text': 'Мої відрядження'},
        {'link': '/degustations', 'text': 'Проведені дегустації'}
    )

    def __init__(self, user_id: int, full_name: str, email: str, role=UserRole.AGRONOMIST.value):
        super().__init__(user_id, full_name, email, role)

    def render_default(self):
        return self.render_buyers()

    def render_buyers(self):
        return self.render('agronom/agronom_buyers.j2', 0)

    def render_agronoms(self):
        return self.render('agronom/agronom_agronoms.j2', 1)

    def render_trips(self):
        return self.render('agronom/agronom_trips.j2', 2)

    def render_degustations(self):
        return self.render('agronom/agronom_degustations.j2', 3)

    def render_make_degustation(self):
        return render_template('item_creations/degustation_creation.j2', top_nav_elements=self.top_nav_elements)

    def render_gather_crop(self):
        return render_template('item_creations/gather_crop.j2', top_nav_elements=self.top_nav_elements)

