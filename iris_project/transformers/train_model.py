
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


@transformer
def train_model(df, *args, **kwargs):
    """
    Train a Decision Tree classifier and calculate test accuracy.
    """

    train_df = df[df["split"] == "train"]
    test_df = df[df["split"] == "test"]

    feature_columns = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)"
    ]

    X_train = train_df[feature_columns]
    y_train = train_df["target"]

    X_test = test_df[feature_columns]
    y_test = test_df["target"]

    max_depth = kwargs.get("max_depth", 3)

    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    return {
        "model": model,
        "predictions": predictions.tolist(),
        "y_test": y_test.tolist(),
        "accuracy": accuracy,
        "max_depth": max_depth
    }


@test
def test_model_accuracy(output, *args):
    assert output is not None
    assert 0 <= output["accuracy"] <= 1
    assert output["accuracy"] >= 0.85
