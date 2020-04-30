from tortoise import fields
from tortoise import Model


class Chat(Model):
    uid = fields.CharField(max_length=50, pk=True)
    id = fields.IntField()
    date = fields.DatetimeField(auto_now_add=True)
    is_duty = fields.BooleanField(default=False)


class Template(Model):
    tag = fields.CharField(max_length=70)
    text = fields.TextField(null=True)
    attachments = fields.TextField(null=True)


class Trusted(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()