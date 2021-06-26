from tortoise import fields

from app.models.base import TimestampedMixin
from app.models.user import User


class Note(TimestampedMixin):
    text = fields.TextField(null=False)
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", to_field="id")

    def __repr__(self):
        return "User(id='{}')".format(self.id)

    def to_dict(self):
        user_dict = self.__dict__.copy()
        user_dict.update({"_author": None})

        return user_dict
