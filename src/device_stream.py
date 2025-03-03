from typing import Generator
import pandas as pd

def output_stream(dataframe: pd.DataFrame) -> Generator[dict]:
    """Generator that yield each row of a DataFrame as a dictionary"""
    for row in dataframe.itertuples():
        yield row._asdict()




if __name__ == "__main__":

    path = "src/data/iot_telemetry_data.csv"
    df = pd.read_csv(path)
    stream = output_stream(df)
    for new_data in stream:
        print(new_data)
