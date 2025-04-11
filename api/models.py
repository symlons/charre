from pydantic import BaseModel

class Feedback(BaseModel):
    image: str
    label: str
    correct: bool
    correct_label: str


class Label(BaseModel):
    label: str
