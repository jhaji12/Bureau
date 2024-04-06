from django.http import HttpResponse
from .ml_model import predict_fraud
from datetime import datetime

def process_csv_and_predict(csv_data):
    # Process CSV data (e.g., convert to DataFrame)
    # Call ML model function
    predictions = predict_fraud()
    if predictions == []:
        return {"status": "OK", "ruleViolated": [], "timestamp": datetime.now()}
    
    return {"status": "ALERT", "ruleViolated": predictions, "timestamp": datetime.now()}