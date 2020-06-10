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

def find_role(mail):
    roles = ['agronom', 'buyer', 'packing_seller', 'admin']
    for i in range(4):
        if comm.is_role(mail, i):
            return roles[i]


def check_registered(mail, password):
    id = comm.get_person_id(mail, password)
    return id

def register_new( role, name, surname, phone, bank_account, mail, password, location, optional = None ):
    if not (comm.get_person_id( mail )):
        comm.add_admin_person( name, surname, phone, bank_account, mail, location, password )
        id = comm.get_person_id( mail )
        if( role == UserRole.SELLER):
            comm.add_admin_seller(id, optional)
        if( role == UserRole.AGRONOMIST):
            comm.add_admin_agronom(id)
        if( role == UserRole.BUYER):
            comm.add_admin_buyer(id, optional)
        return True
    return False
