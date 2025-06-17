import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression, LinearRegression
import joblib

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y_class = iris.target
y_reg = X["petal width (cm)"]

clf = LogisticRegression().fit(X, y_class)
reg = LinearRegression().fit(X.drop(columns="petal width (cm)"), y_reg)

joblib.dump(clf, "classification_model.pkl")
joblib.dump(reg, "regression_model.pkl")