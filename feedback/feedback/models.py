from pydantic import BaseModel


class Feedback(BaseModel):
    """
    Represents a feedback, used for post and get a specific feedback
    """

    image: bytes
    label: str
    correct: bool
    correct_label: str

    class Config:
        arbitrary_types_allowed = True


class FeedbackList(BaseModel):
    """
    Represents a feedback, used for listing feedbacks
    """

    id: str
    label: str
    correct: bool
    correct_label: str
