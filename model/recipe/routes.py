import json

import mongoengine as me
import datetime


MOD_NAME = "Recipe_"

class Recipe(me.Document):
    name = me.StringField(required=True)
    type = me.StringField()
    photo = me.StringField()
    recipe = me.StringField()
    lastUpdate = me.DateTimeField(default=datetime.datetime.now)
    added_by = me.ReferenceField('User')
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
            "lastUpdate": self.lastUpdate.timestamp(),
            "added_by": str(self.added_by)
        })
