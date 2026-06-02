import random

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import joblib
import boto3
from datetime import datetime, timedelta, timezone

app = FastAPI()

REGION = "eu-north-1"
INSTANCE_ID = "i-0e22a8a3112813a50"

CPU_THRESHOLD = 1.0
RAM_THRESHOLD = 10

SNS_TOPIC_ARN = "arn:aws:sns:eu-north-1:519197412697:cpu-alert-topic"

model = joblib.load("models/resource_model.pkl")

cloudwatch = boto3.client("cloudwatch", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)


# ----------------------CPU METRIC ----------------------------------
def get_cpu():
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": INSTANCE_ID}],
        StartTime=datetime.now(timezone.utc) - timedelta(minutes=5),
        EndTime=datetime.now(timezone.utc),
        Period=300,
        Statistics=["Average"]
    )

    data = response.get("Datapoints", [])
    if not data:
        return 0

    return round(sorted(data, key=lambda x: x["Timestamp"])[-1]["Average"], 2)


# ------------------------ RAM METRIC -----------------------------
def get_ram():
    response = cloudwatch.get_metric_statistics(
        Namespace="CWAgent",
        MetricName="mem_used_percent",
        Dimensions=[{"Name": "host", "Value": "ip-172-31-44-16"}],
        StartTime=datetime.now(timezone.utc) - timedelta(minutes=5),
        EndTime=datetime.now(timezone.utc),
        Period=60,
        Statistics=["Average"]
    )

    data = response.get("Datapoints", [])
    if not data:
        return 0

    return round(sorted(data, key=lambda x: x["Timestamp"])[-1]["Average"], 2)


# ---------------- ALERT FUNCTION ----------------
def send_alert(message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Scaling Alert 🚨",
        Message=message
    )


# ---------------- TIME ESTIMATION ----------------
def estimate_time_to_threshold(current, predicted, threshold):
    if predicted <= current:
        return None

    growth_rate = predicted - current
    if growth_rate <= 0:
        return None

    remaining = threshold - current
    if remaining <= 0:
        return 0

    minutes = (remaining / growth_rate) * 60
    return round(minutes, 2)


# ---------------- DASHBOARD ROUTE ----------------
@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


# ---------------- LIVE METRICS ROUTE ----------------
@app.get("/metrics")
def metrics():
    return {
        "cpu": get_cpu(),
        "ram": get_ram()
    }


# ---------------- PREDICTION ROUTE ----------------
@app.get("/predict")
def predict():

    current_cpu = get_cpu()
    current_ram = get_ram()
    active_users = random.randint(50, 200)
    current_hour = datetime.now().hour

    predicted_cpu = model.predict(
        [[current_ram, active_users, current_hour, current_cpu, current_ram]]
    )[0]

    status = "🟢 System Stable"

    if current_cpu >= CPU_THRESHOLD or current_ram >= RAM_THRESHOLD:
        status = "🔴 Scaling Required Immediately"

        send_alert(
            f"Scale Up Required 🚨\n"
            f"CPU: {current_cpu}%\n"
            f"RAM: {current_ram}%\n"
            f"Active Users: {active_users}"
        )

    predicted_time_minutes = estimate_time_to_threshold(
        current_cpu,
        predicted_cpu,
        CPU_THRESHOLD
    )

    if predicted_time_minutes:
        reach_time = datetime.now(timezone.utc) + timedelta(minutes=predicted_time_minutes)
        reach_time_str = reach_time.strftime("%H:%M:%S")
    else:
        reach_time_str = "N/A"

    return JSONResponse(content={
        "current_cpu": current_cpu,
        "current_ram": current_ram,
        "active_users": active_users,
        "predicted_cpu": round(predicted_cpu, 2),
        "status": status,
        "reach_time": reach_time_str
    })