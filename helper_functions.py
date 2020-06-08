from classes.users import User, Admin, NoUser, Buyer, Agronom, UserRole


def get_user_from_session(session) -> User:
    if 'user' not in session:
        return NoUser()
    role = session['user']['role']
    if role == UserRole.BUYER.value:
        return Buyer(**session['user'])
    elif role == UserRole.AGRONOMIST.value:
        return Agronom(**session['user'])
    elif role == UserRole.ADMIN.value:
        return Admin(**session['user'])
    else:  # If something went wrong
        return NoUser()


def check_registered(mail, password):
    return True


def register_new(*args, **kwargs):
    return True
