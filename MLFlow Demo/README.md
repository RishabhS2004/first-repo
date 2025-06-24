## MLFlow Demonstration  
  
This project showcases a complete ML experimentation and deployment pipeline using **MLflow** and **Scikit-learn** with the Iris dataset.  


# Folder Structure  

MLFlow Demonstration  
├── data_version.py # Trains models on 3 dataset versions  
├── best_model_flask.py # Flask API to serve champion/challenger models    
├── best_model/ # Best model saved locally for testing  
├── mlruns/ # MLflow tracking logs  
└── README.md # You are here  

#🌼 Dataset Versions  

Three versions of the Iris dataset are created:  

- `v1`: sepal length, sepal width, target class  
- `v2`: petal length, petal width, target class  
- `v3`: all 4 features, target class  

Each version is trained using 4 model types:  
- Logistic Regression (`LogisReg`)  
- Decision Tree  
- SVM  
- Random Forest (`RF`)  

Each model is trained with 3 different hyperparameter sets and logged to MLflow. Therefore total number of models trained= 4x3x3 = 36.   


#🔍 MLflow Tracking 

MLflow is used to:  
- Track model metrics: accuracy, precision, recall  
- Compare different dataset versions and algorithms  
- Register the top 2 models  
- Assign aliases:  
  - `champion`: Best performing model  
  - `challenger`: Second-best performing model  

#🚀 Serving with Flask  

Run the Flask app to expose the champion/challenger model as a prediction service.  

python best_model_flask.py  

Use Postman or cURL to send prediction requests:  

POST http://127.0.0.1:5001/predict  
{  
  "data": [[5.1, 3.5, 1.4, 0.2]]  
}  
Model is selected randomly between champion and challenger.  

#📌 Notes

Use MLflow UI (mlflow ui) to explore and compare all runs.  
Registered models and aliases are managed under the name BestIrisModel.  
