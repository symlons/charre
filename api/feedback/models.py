from pydantic import BaseModel


class Feedback(BaseModel):
    image: bytes
    label: str
    correct: bool
    correct_label: str

    class Config:
        arbitrary_types_allowed = True


class FeedbackList(BaseModel):
    id: str
    label: str
    correct: bool
    correct_label: str
