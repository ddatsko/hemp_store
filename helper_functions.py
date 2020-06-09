from classes.users import User, Admin, NoUser, Buyer, Agronom, UserRole
# from app import comm
from classes.dbCommunicator import dbCommunicator
comm = dbCommunicator("db14", host = "142.93.163.88",port = 6006, user = "team14", password = "pas1swo4rd")



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
    id = comm.get_person_id(mail)
    return (id is None)

def register_new(user_role, name, surname, phone, b_a, mail, location, password, *args, **kwargs):
    if not (comm.get_person_id(mail)):
        comm.add_admin_person(name,surname, phone, b_a, mail, location, password, **kwargs)
        id = comm.get_person_id(mail)
        if(user_role == UserRole.SELLER.value):
            comm.add_admin_seller(id, *args, **kwargs)
        if(user_role == UserRole.AGRONOMIST.value):
            comm.add_admin_agronom(id, *args, **kwargs)
        if(user_role == UserRole.BUYER.value):
            comm.add_admin_buyer(id, *args, **kwargs)
    return False
