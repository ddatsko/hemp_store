from classes.users.user_role import UserRole


class User:
    def __init__(self, user_id: int, full_name: str, email: str, role=UserRole.BUYER):
        self.id = user_id
        self.full_name = full_name
        self.email = email
        self.role = role

    def render_default(self):
        return ''

    def render_buyers(self):
        return ''
