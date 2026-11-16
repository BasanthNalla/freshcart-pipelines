
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


@transformer
def evaluate_model(model_output, *args, **kwargs):
    """
    Evaluate the trained Decision Tree model.
    """

    y_true = model_output["y_test"]
    y_pred = model_output["predictions"]

    cm = confusion_matrix(y_true, y_pred)

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(
        y_true, y_pred, average="weighted", zero_division=0
    )

    recall = recall_score(
        y_true, y_pred, average="weighted", zero_division=0
    )

    f1 = f1_score(
        y_true, y_pred, average="weighted", zero_division=0
    )

    print("Confusion Matrix:")
    print(cm)

    print("\nEvaluation Metrics:")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    return {
        "confusion_matrix": cm.tolist(),
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


@test
def test_evaluation(output, *args):
    assert output is not None
    assert len(output["confusion_matrix"]) == 3
    assert 0 <= output["accuracy"] <= 1
    assert 0 <= output["precision"] <= 1
    assert 0 <= output["recall"] <= 1
    assert 0 <= output["f1_score"] <= 1
