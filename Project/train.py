import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import mlflow
import mlflow.sklearn

X_train, X_test, y_train, y_test = joblib.load("processed/data_split.pkl")

os.makedirs("model", exist_ok=True)

mlflow.set_experiment("churn_prediction")

model_scores = {}

# Random Forest Training
with mlflow.start_run(run_name="RandomForest"):
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    model_scores['RandomForest'] = (acc_rf, rf)

    print("\n Random Forest Results:")
    print(classification_report(y_test, y_pred_rf))

    mlflow.log_param("model", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", acc_rf)
    mlflow.sklearn.log_model(rf, "random_forest_model")

    joblib.dump(rf, "model/random_forest_model.pkl")

# Logistic Regression Training
with mlflow.start_run(run_name="LogisticRegression"):
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    acc_lr = accuracy_score(y_test, y_pred_lr)
    model_scores['LogisticRegression'] = (acc_lr, lr)

    print("\n Logistic Regression Results:")
    print(classification_report(y_test, y_pred_lr))

    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_metric("accuracy", acc_lr)
    mlflow.sklearn.log_model(lr, "logistic_regression_model")

    joblib.dump(lr, "model/logistic_regression_model.pkl")

# Select Champion Model
best_model_name = max(model_scores, key=lambda k: model_scores[k][0])
best_model_acc, best_model = model_scores[best_model_name]

print(f"\n🏆 Champion Model: {best_model_name} with Accuracy = {best_model_acc:.4f}")
joblib.dump(best_model, "model/churn_model.pkl")
print(" Saved champion model as 'model/churn_model.pkl'")
