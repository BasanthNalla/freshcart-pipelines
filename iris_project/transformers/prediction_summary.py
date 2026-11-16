
@transformer
def prediction_summary(model_output, *args, **kwargs):
    """
    Generate a summary of model predictions.
    """
    actual = model_output["y_test"]
    predicted = model_output["predictions"]

    total = len(actual)
    correct = sum(a == p for a, p in zip(actual, predicted))
    incorrect = total - correct
    accuracy = correct / total if total > 0 else 0

    summary = {
        "total_predictions": total,
        "correct_predictions": correct,
        "incorrect_predictions": incorrect,
        "accuracy": accuracy
    }

    print("Prediction Summary:")
    print(summary)

    return summary


@test
def test_prediction_summary(output, *args):
    assert output is not None
    assert output["total_predictions"] == 30
    assert output["correct_predictions"] + output["incorrect_predictions"] == 30
    assert 0 <= output["accuracy"] <= 1
