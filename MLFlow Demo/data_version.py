import os
import shutil
import tempfile
import pandas as pd
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient
import subprocess
import mlflow.sklearn

from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Set MLflow experiment name
mlflow.set_experiment("Iris_Classification_Experiment")

# Load the iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target, name='target')

# Create 3 versions of the dataset
dataset_versions = {
    "v1": pd.concat([X.iloc[:, :2], y], axis=1),  # Sepal only
    "v2": pd.concat([X.iloc[:, 2:], y], axis=1),  # Petal only
    "v3": pd.concat([X, y], axis=1),              # All features
}

# Define models and parameter grids
models = {
    "LogisReg": (
        LogisticRegression,
        [
            {"C": 1.0, "solver": "lbfgs", "multi_class": "multinomial", "max_iter": 200},
            {"C": 0.5, "solver": "lbfgs", "multi_class": "multinomial", "max_iter": 200},
            {"C": 2.0, "solver": "lbfgs", "multi_class": "multinomial", "max_iter": 200}
        ]
    ),
    "SVM": (
        SVC,
        [
            {"C": 1.0, "kernel": "linear"},
            {"C": 1.0, "kernel": "rbf"},
            {"C": 0.5, "kernel": "rbf"}
        ]
    ),
    "Tree": (
        DecisionTreeClassifier,
        [
            {"max_depth": 3},
            {"max_depth": 5},
            {"max_depth": None}
        ]
    ),
    "RF": (
        RandomForestClassifier,
        [
            {"n_estimators": 10},
            {"n_estimators": 50},
            {"n_estimators": 100}
        ]
    )
}

best_score = 0
best_model_uri = ""
best_run_id = ""

# Run the full grid of experiments
for version_name, version_df in dataset_versions.items():
    X = version_df.drop(columns='target')
    y = version_df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for model_name, (model_class, param_list) in models.items():
        for params in param_list:
            with mlflow.start_run(run_name=f"{version_name}-{model_name}") as run:
                model = model_class(**params)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Metrics
                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, average='macro')
                rec = recall_score(y_test, y_pred, average='macro')

                # Log to MLflow
                mlflow.log_param("dataset_version", version_name)
                mlflow.log_param("model_name", model_name)
                for p, v in params.items():
                    mlflow.log_param(p, v)
                mlflow.log_metric("accuracy", acc)
                mlflow.log_metric("precision", prec)
                mlflow.log_metric("recall", rec)

                # Log model to MLflow
                mlflow.sklearn.log_model(model, name="model")

                # Save predictions as CSV
                predictions_df = pd.DataFrame({"actual": y_test, "predicted": y_pred})
                with tempfile.TemporaryDirectory() as tmp_dir:
                    predictions_path = os.path.join(tmp_dir, "predictions.csv")
                    predictions_df.to_csv(predictions_path, index=False)
                    mlflow.log_artifact(predictions_path, artifact_path="predictions")

                # Save best model separately
                if acc > best_score:
                    best_score = acc
                    best_model_uri = mlflow.get_artifact_uri("model")
                    best_run_id = run.info.run_id

                    if os.path.exists("best_model"):
                        shutil.rmtree("best_model")
                    mlflow.sklearn.save_model(model, path="best_model")

# Final status
print("\n✅ Best model saved to 'best_model/'")
print(f"✅ Best accuracy: {best_score}")
print(f"✅ Best run ID: {best_run_id}")

from mlflow import register_model

# Construct URI to the model artifact in the run
model_uri = f"runs:/{best_run_id}/model"

# Register the model under a name
registered_model = mlflow.register_model(model_uri, name="BestIrisModel")
print(f"✅ Registered model: {registered_model.name}, version: {registered_model.version}")

client = MlflowClient()

# 1. Get all runs from current experiment
experiment = client.get_experiment_by_name("Default")
runs = client.search_runs([experiment.experiment_id], order_by=["metrics.accuracy DESC"])

# 2. Get top 2 runs
champion_run = runs[0]
challenger_run = runs[1]

def ensure_model_registered(run_id):
    model_uri = f"runs:/{run_id}/model"
    return mlflow.register_model(model_uri, name="BestIrisModel")

champion_model = ensure_model_registered(champion_run.info.run_id)
challenger_model = ensure_model_registered(challenger_run.info.run_id)

# 3. Assign aliases via subprocess
def assign_alias(version, alias):
    subprocess.run([
        "python", "-m", "mlflow", "models", "alias", "set",
        "-n", "BestIrisModel",
        "-v", str(version),
        "-a", alias
    ], check=True)
    print(f"✅ Alias '{alias}' assigned to version {version}")

assign_alias(champion_model.version, "champion")
assign_alias(challenger_model.version, "challenger")