from typing import List
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseAPIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Semester(BaseAPIModel):
    code: str
    description: str

class Subject(BaseAPIModel):
    code: str
    description: str