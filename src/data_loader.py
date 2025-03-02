import pandas as pd
pd.set_option('future.no_silent_downcasting', True)


def data_preprocessing(df_path: str, devices_column: str, ts_column: str, order_by: str, to_datetime: bool = True) -> dict:
    """Creates Three datframes, one for each device, and process the data for the fake streaming: it change the timestamp to datetime and order the dataframes by datetime."""

    df_path = df_path
    df = pd.read_csv(df_path)

    print("Changing devices names:")
    device_map = {device: idx for idx, device in enumerate(df[devices_column].unique())}
    df[devices_column] = df[devices_column].map(device_map)
    print("Device mapping: ", device_map)

    df = df.sort_values(by=order_by, ascending=True)

    if to_datetime:
        df[ts_column] = pd.to_datetime(df[ts_column], unit="s")

    dfs_dict = {f"df{device}": df_device.reset_index() for device, df_device in df.groupby(devices_column)  }

    return dfs_dict

if __name__ == "__main__":
    path = "packages/data/iot_telemetry_data.csv"
    df_dict = data_preprocessing(path, "device", "ts", "ts")
    df0 = df_dict["df0"]
    print(df0.head())
