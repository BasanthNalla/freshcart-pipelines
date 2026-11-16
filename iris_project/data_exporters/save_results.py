
import pandas as pd
from pathlib import Path


@data_exporter
def save_results(model_output, *args, **kwargs):
    """
    Save model predictions and actual values to a CSV file.
    """

    output_df = pd.DataFrame({
        "actual": model_output["y_test"],
        "predicted": model_output["predictions"]
    })

    output_path = Path(
        "/content/freshcart-pipelines/iris_project/iris_predictions.csv"
    )

    output_df.to_csv(output_path, index=False)

    return {
        "file_path": str(output_path),
        "rows_saved": len(output_df),
        "accuracy": model_output["accuracy"]
    }


@test
def test_output(output, *args):
    assert output is not None
    assert output["rows_saved"] == 30
    assert Path(output["file_path"]).exists()
