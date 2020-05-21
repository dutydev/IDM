from tortoise import fields
from tortoise import Model
from module.objects.enums import TokenType

__all__ = (
    "Chat", "Setting",
    "Template", "Trusted",
    "Token"
)


class ABCModel(Model):
    def load_model(self) -> dict:
        ...


class Chat(ABCModel):
    uid = fields.CharField(max_length=50, pk=True)
    id = fields.IntField()
    title = fields.CharField(max_length=250)
    is_duty = fields.BooleanField(default=False)
    date = fields.DatetimeField(auto_now_add=True)

    def load_model(self) -> dict:
        return {self.uid: {
            "id": self.id,
            "title": self.title
        }}


class Setting(ABCModel):
    page_limit = fields.IntField(default=30)

    def load_model(self) -> dict:
        return {"page_limit": self.page_limit}


class Token(ABCModel):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=85)
    type = fields.CharEnumField(TokenType)

    def load_model(self) -> dict:
        return {self.id: {
            "type": self.type,
            "token": self.token
        }}


class Template(ABCModel):
    tag = fields.CharField(max_length=70)
    text = fields.TextField(null=True)
    attachments = fields.TextField(null=True)

    def load_model(self) -> dict:
        return {self.tag: {
            "message": self.text,
            "attachment": self.attachments
        }}


class Trusted(ABCModel):
    uid = fields.IntField()
    name = fields.TextField()

    def load_model(self) -> dict:
        return {self.uid: self.name}