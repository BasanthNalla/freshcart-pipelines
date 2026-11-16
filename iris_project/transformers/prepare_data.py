
from sklearn.model_selection import train_test_split

if "transformer" not in globals():
    def transformer(function):
        return function

if "test" not in globals():
    def test(function):
        return function

@transformer
def transform(df, *args, **kwargs):
    """
    Split the Iris dataset into 80% training data
    and 20% testing data.
    """

    train_indices, test_indices = train_test_split(
        df.index,
        test_size=0.2,
        random_state=42,
        stratify=df["target"]
    )

    output = df.copy()

    output["split"] = "train"
    output.loc[test_indices, "split"] = "test"

    return output


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 150

    assert (output["split"] == "train").sum() == 120
    assert (output["split"] == "test").sum() == 30
