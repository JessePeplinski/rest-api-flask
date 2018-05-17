from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username) # get the username, set to None by default if there is none
    if user and safe_str_cmp(user.password, password): # better way to do ==, dealing with ascii
        return user

# payload is the contents of JWT token
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)