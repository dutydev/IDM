from tortoise import fields
from tortoise import Model


class Chat(Model):
    uid = fields.CharField(max_length=50, pk=True)
    id = fields.IntField()
    title = fields.CharField(max_length=250)
    is_duty = fields.BooleanField(default=False)
    date = fields.DatetimeField(auto_now_add=True)


class Template(Model):
    tag = fields.CharField(max_length=70)
    text = fields.TextField(null=True)
    attachments = fields.TextField(null=True)


class Trusted(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()