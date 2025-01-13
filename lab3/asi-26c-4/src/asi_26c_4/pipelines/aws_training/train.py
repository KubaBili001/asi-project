import argparse
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib
import boto3

def send_metrics_to_cloudwatch(namespace, metric_name, value, unit="None"):
    try:
        cloudwatch = boto3.client("cloudwatch", region_name="eu-north-1")
        response = cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": value,
                    "Unit": unit,
                }
            ],
        )
        print(f"Metric {metric_name} sent to CloudWatch: {response}")
    except Exception as e:
        print(f"Error sending metrics to CloudWatch: {e}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--test-size', type=float, default=0.2, help="Proporcja zbioru testowego")
    parser.add_argument('--random-state', type=int, default=42, help="Losowy seed dla podziału danych")

    parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))

    args, _ = parser.parse_known_args()

    print(f"Wczytywanie danych z: {args.train}")
    train_data_path = os.path.join(args.train, "verified_employees.pq")
    data = pd.read_parquet(train_data_path)

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    print(f"Podział danych: test_size={args.test_size}, random_state={args.random_state}")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.random_state)

    print("Rozpoczęcie treningu modelu...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error (MSE) na zbiorze testowym: {mse}")

    send_metrics_to_cloudwatch("asi", "MSE", mse, unit="None")

    print(f"Zapis modelu do katalogu: {args.model_dir}")
    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, model_path)

    print(f"Model zapisany w: {model_path}")
