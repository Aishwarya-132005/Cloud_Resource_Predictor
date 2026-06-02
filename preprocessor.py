import pandas as pd

def load_and_preprocess(path):

    df = pd.read_csv(path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    df["prev_cpu"] = df["cpu_usage"].shift(1)
    df["prev_ram"] = df["ram_usage"].shift(1)

    df = df.dropna()

    X = df[["ram_usage", "active_users", "hour", "prev_cpu", "prev_ram"]]
    y = df["cpu_usage"]

    return X, y