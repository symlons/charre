from pydantic import BaseModel, ConfigDict


class Feedback(BaseModel):
    """
    Represents a feedback, used for post and get a specific feedback
    """

    image: bytes
    label: str
    correct: bool
    correct_label: str
    trained: bool = False

    class Config:
        arbitrary_types_allowed = True


class FeedbackPatch(BaseModel):
    """
    Object for patching feedback from trained=false to trained=true
    """

    trained: bool
    model_config = ConfigDict(extra="forbid")


class FeedbackList(BaseModel):
    """
    Represents a feedback, used for listing feedbacks
    """

    id: str
    label: str
    correct: bool
    correct_label: str
