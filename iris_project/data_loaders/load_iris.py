
from sklearn.datasets import load_iris


@data_loader
def load_data(*args, **kwargs):
    """
    Load the Iris dataset as a Pandas DataFrame.
    """
    iris = load_iris(as_frame=True)
    return iris.frame


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 150
    assert "target" in output.columns
    assert output.shape[1] == 5
    assert output.isnull().sum().sum() == 0
