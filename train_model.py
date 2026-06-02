# Train_model.py

import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from preprocessor import load_and_preprocess


def main():

    print("Loading and preprocessing dataset...")
    X, y = load_and_preprocess("server_usage.csv")

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print("Initializing model...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )

    print("Training model...")
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\nModel Performance:")
    print("-------------------")
    print(f"MAE: {mae:.4f}")
    print(f"R2 Score: {r2:.4f}")

    # Create models folder if not exists
    os.makedirs("models", exist_ok=True)

    # Save trained model
    model_path = "models/resource_model.pkl"
    joblib.dump(model, model_path)

    print(f"\nModel saved successfully at: {model_path}")


if __name__ == "__main__":
    main()