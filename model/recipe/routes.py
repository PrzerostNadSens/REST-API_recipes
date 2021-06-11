import json
from flask import abort

import mongoengine as me
import datetime

from mongoengine.errors import ValidationError

from model.user import User

MOD_NAME = "Recipe_"


def re_User_id(val):
    try:
        if not User.objects.filter(id=val):
            pass
    except ValidationError:
        abort(400, description={
            "message": "Błędny Id użytkownika.",
            "status": 400
        })

class Recipe(me.Document):
    name = me.StringField(required=True)
    type = me.StringField()
    photo = me.StringField()
    recipe = me.StringField()
    userId = me.StringField(required=True, validation=re_User_id)
    lastUpdate = me.DateTimeField(default=datetime.datetime.now)
    meta = {'collection': 'Recipe'}

    def update_date(object):
        object.lastUpdate = datetime.datetime.now()
        return object.save()


    def to_json(self):
        return json.dumps({
            "_id": str(self.pk),
            "name": self.name,
            "type": self.type,
            "photo": self.photo,
            "recipe": self.recipe,
            "userId": self.userId,
            "lastUpdate": self.lastUpdate.timestamp()
        })
