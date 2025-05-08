from pathlib import Path

from pymongo.collection import Collection

from feedback.models import Feedback
from feedback.mongo import MongoCollections, get_collection

IMG_MOCK_DIR = Path(__file__).parent / "mock"


def mock_labels(label_client: Collection) -> None:
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


def mock_feedbacks(feedback_client: Collection) -> None:
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


if __name__ == "__main__":
    label_client = get_collection(MongoCollections.LABELS)
    label_client.drop()
    mock_labels(label_client)

    feedback_client = get_collection(MongoCollections.FEEDBACK)
    feedback_client.drop()
    mock_feedbacks(feedback_client)

    print("Mock data inserted")
