# ☁️ Predictive Cloud Resource Scaling

A machine learning-powered cloud monitoring dashboard that **predicts CPU and RAM usage** of an AWS EC2 instance in real time, triggers **SNS alerts** when thresholds are crossed, and visualizes everything through a sleek web dashboard built with **FastAPI**.

---

## 🚀 Features

- 📊 **Live Metrics** — Fetches real-time CPU & RAM usage from AWS CloudWatch
- 🤖 **ML Prediction** — Uses a trained Random Forest model to predict future CPU usage
- ⏱️ **Threshold Time Estimation** — Estimates how many minutes until CPU/RAM hits critical levels
- 🚨 **Auto Alerts** — Sends email/SMS alerts via AWS SNS when scaling is required
- 🌐 **Web Dashboard** — Interactive UI to view live metrics and predictions

---

## 🛠️ AWS Services Used (Free Tier Friendly)

| AWS Service | Usage | Free Tier Limit |
|---|---|---|
| **EC2** | Hosts the monitored server instance | 750 hrs/month (t2.micro or t3.micro) |
| **CloudWatch** | Collects CPU & RAM metrics from EC2 | 10 custom metrics, 1M API requests/month |
| **CloudWatch Agent** | Sends RAM usage (mem_used_percent) to CloudWatch | Included in CloudWatch free tier |
| **SNS (Simple Notification Service)** | Sends scaling alert emails/SMS | 1,000 email notifications/month free |

> ✅ All AWS services used in this project are available within the **AWS Free Tier** for 12 months.

---

## 🧠 How It Works

```
EC2 Instance (Running)
        │
        ▼
CloudWatch Agent ──► CloudWatch Metrics (CPU + RAM)
        │
        ▼
FastAPI Backend (/metrics)
   - Fetches live CPU & RAM from CloudWatch API
        │
        ▼
ML Model (Random Forest)
   - Predicts next CPU usage based on:
     [RAM, Active Users, Hour, Prev CPU, Prev RAM]
        │
        ├── If threshold exceeded ──► SNS Alert 🚨
        │
        ▼
Dashboard (dashboard.html)
   - Displays CPU%, RAM%, Active Users
   - Shows predicted CPU & estimated time to threshold
```

---

## 📁 Project Structure

```
Cloud_Resource_Predictor/
│
├── main.py                 # FastAPI app - routes, metrics, prediction, alerts
├── train_model.py          # Trains the Random Forest model
├── preprocessor.py         # Data preprocessing for model training
├── dataset_generator.py    # Generates synthetic server usage dataset
├── server_usage.csv        # Training dataset (CPU, RAM, Active Users)
├── dashboard.html          # Frontend monitoring dashboard
├── requirements.txt        # Python dependencies
├── models/
│   └── resource_model.pkl  # Trained ML model (generated locally)
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- AWS Account (Free Tier)
- AWS CLI configured

### 1. Clone the Repository
```bash
git clone https://github.com/Aishwarya-132005/Cloud_Resource_Predictor.git
cd Cloud_Resource_Predictor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure AWS Credentials
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `eu-north-1`
- Output format: `json`

### 4. Train the ML Model (first time only)
```bash
python train_model.py
```

### 5. Start EC2 Instance
- Go to **AWS Console → EC2 → Instances**
- Start your instance and ensure **CloudWatch Agent** is running for RAM metrics

### 6. Run the Application
```bash
uvicorn main:app --reload
```

Open your browser at: **http://127.0.0.1:8000**

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Web dashboard (HTML) |
| `/metrics` | GET | Live CPU & RAM from CloudWatch |
| `/predict` | GET | ML prediction + scaling status + alert |

---

## 🔧 Configuration

Edit these values in `main.py` to match your AWS setup:

```python
REGION = "eu-north-1"                          # Your AWS region
INSTANCE_ID = "i-xxxxxxxxxxxxxxxxx"            # Your EC2 Instance ID
CPU_THRESHOLD = 80.0                           # CPU alert threshold (%)
RAM_THRESHOLD = 75                             # RAM alert threshold (%)
SNS_TOPIC_ARN = "arn:aws:sns:..."              # Your SNS Topic ARN
```

---

## 🧪 ML Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: `ram_usage`, `active_users`, `hour`, `prev_cpu`, `prev_ram`
- **Target**: `cpu_usage` (next hour prediction)
- **Training Data**: 5,000 synthetic data points
- **Estimators**: 200 trees, max depth 15

---

## 📸 Dashboard Preview

The dashboard displays:
- 📈 CPU Usage progress bar with live %
- 🧠 RAM Usage progress bar with live %
- 👥 Active Users count
- 🤖 Predicted CPU % (from ML model)
- ⏰ Estimated time to reach CPU threshold
- 🔴/🟢 System status (Stable / Scaling Required)

---

## ⚠️ Important Notes

- Ensure your EC2 instance is **Running** before fetching metrics
- **CloudWatch Agent** must be installed and running on EC2 for RAM metrics
- The `models/resource_model.pkl` file is excluded from Git (56MB). Run `python train_model.py` to regenerate it
- **Never commit AWS credentials** to GitHub

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
