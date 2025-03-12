import pandas as pd
pd.set_option('future.no_silent_downcasting', True)


def preprocess_and_split_data(df_path: str, devices_column: str, ts_column: str, order_by: str, to_datetime: bool = True) -> dict:
    """
    Reads a CSV file, processes the data for fake streaming, and splits it into separate DataFrames by device.

    Args:
        df_path (str): Path to the CSV file.
        devices_column (str): Column containing device identifiers.
        ts_column (str): Column containing timestamps.
        order_by (str): Column used for sorting the data.
        to_datetime (bool, optional): Whether to convert the timestamp column to datetime. Defaults to True.

    Returns:
        dict: A dictionary where keys are 'df{device_id}' and values are Pandas DataFrames.
    """
    df = pd.read_csv(df_path)

    # maps devices' names to numeric IDs
    print("Changing devices names:")
    device_map = {device: idx for idx, device in enumerate(df[devices_column].unique())}
    df[devices_column] = df[devices_column].map(device_map)
    print("Device mapping: ", device_map)

    df = df.sort_values(by=order_by, ascending=True)

    if to_datetime:
        df[ts_column] = pd.to_datetime(df[ts_column], unit="s")

    dfs_dict = {f"df{device}": df_device.reset_index(drop=True) for device, df_device in df.groupby(devices_column)  }

    return dfs_dict

