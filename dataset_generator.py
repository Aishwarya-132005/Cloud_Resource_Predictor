# dataset_generator.py

import pandas as pd
import numpy as np

np.random.seed(42)

rows = 5000
timestamps = pd.date_range(start="2024-01-01", periods=rows, freq="H")

# Active users pattern (daily wave)
active_users = np.random.randint(50, 500, rows)

# RAM depends on users
ram_usage = active_users * 0.12 + np.random.normal(0, 5, rows)
ram_usage = np.clip(ram_usage, 20, 95)

# CPU depends on RAM + users
cpu_usage = ram_usage * 0.6 + active_users * 0.05 + np.random.normal(0, 3, rows)
cpu_usage = np.clip(cpu_usage, 5, 100)

data = pd.DataFrame({
    "timestamp": timestamps,
    "cpu_usage": cpu_usage,
    "ram_usage": ram_usage,
    "active_users": active_users
})

data.to_csv("server_usage.csv", index=False)

print("New dataset generated with CPU, RAM, Active Users")