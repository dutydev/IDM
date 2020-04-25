import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        allow_mutation = True
        use_enum_values = True

    def __str__(self):
        return str(self.dict())

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.dict())
