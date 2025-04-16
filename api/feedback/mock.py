from pathlib import Path

from feedback.models import Feedback
from feedback.mongo import MongoCollections, get_client

IMG_MOCK_DIR = Path(__file__).parent.parent / "mock"


def mock_data() -> None:
    """
    Mock data for local development

    :return: None
    """

    label_client = get_client(MongoCollections.LABELS)
    label_client.drop()
    _mock_labels(label_client)

    feedback_client = get_client(MongoCollections.FEEDBACK)
    feedback_client.drop()
    _mock_feedbacks(feedback_client)

    print("Mock data inserted")


def _mock_labels(label_client) -> None:
    """
    Mock car labels for local dev

    :param label_client: MongoDB client for labels
    :return: None
    """
    labels = [
        {"label": "Audi"},
        {"label": "BMW"},
        {"label": "Volkswagen"},
        {"label": "Dis Mami"},
    ]

    label_client.insert_many(labels)


def _mock_feedbacks(feedback_client) -> None:
    """
    Mock car classification feedback for local dev

    :param feedback_client: MongoDB client for feedback
    :return: None
    """
    audi = IMG_MOCK_DIR / "audi.jpg"
    bmw = IMG_MOCK_DIR / "bmw.jpg"
    vw = IMG_MOCK_DIR / "vw.jpg"

    # Mock data
    feedback = [
        Feedback(
            image=audi.read_bytes(),
            label="audi",
            correct=True,
            correct_label="audi",
        ),
        Feedback(
            image=bmw.read_bytes(),
            label="audi",
            correct=False,
            correct_label="bmw",
        ),
        Feedback(
            image=vw.read_bytes(),
            label="bmw",
            correct=False,
            correct_label="volkswagen",
        ),
    ]
    feedback_client.insert_many([feedback.model_dump() for feedback in feedback])
