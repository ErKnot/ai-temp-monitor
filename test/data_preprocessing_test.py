from src.data_preprocessing import preprocess_and_split_data

df_path = "src/data/iot_telemetry_data.csv"
dfs_dict = preprocess_and_split_data(
        df_path = df_path,
        devices_column = "device",
        ts_column = "ts",
        order_by = "ts",
        )
df0 = dfs_dict["df0"]
print(df0)
