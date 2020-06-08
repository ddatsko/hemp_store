from app import comm
from classes.users import Buyer, UserRole, Agronom, Admin



def check_registered(mail, password):
    id = comm.get_person_id
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