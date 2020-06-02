from classes.users import User
from classes.users import UserRole


class NoUser(User):
    def __init__(self):
        super().__init__(0, '', '', UserRole.NO_USER)

