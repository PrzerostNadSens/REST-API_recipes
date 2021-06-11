import json
import mongoengine as me
#from werkzeug.security import generate_password_hash, check_password_hash

MOD_NAME = "User_"


class User(me.Document):
    name = me.StringField(required=True)
    subname = me.StringField(required=True)
    mail = me.EmailField(required=True, unique=True)
    login = me.StringField(required=True, unique=True)
    phone = me.StringField(unique=True, min_length=9)
    password = me.StringField(required=True, min_length=8)                      # TODO: __Kolejny__ Zabezpieczyć hasło
    birthday = me.DateTimeField()
    meta = {'collection': 'User'}

    '''def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)'''

    def to_json(self):
        return json.dumps({
            "_id": str(self.pk),
            "name": self.name,
            "subname": self.subname,
            "mail": self.mail,
            "login": self.login,
            "phone": self.phone.timestamp(),
            "password": self.password,
            "birthday": self.birthday
        })
