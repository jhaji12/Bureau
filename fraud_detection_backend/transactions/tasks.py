from celery import shared_task
import csv
import os
import json
from django.http import HttpResponse
from .ml_model import predict_fraud

@shared_task
def process_csv_and_predict(csv_data):
    # Process CSV data (e.g., convert to DataFrame)
    # Call ML model function
    predictions = predict_fraud()
    predictions = []
    return predictions

@shared_task
def create_csv_from_json(json_data):
    csv_exists = os.path.isfile('data.csv')
    
    columns_to_include = ['dateTimeTransaction', 'latitude', 'longitude', 'cardBalance', 'cardAcceptorId', "cardAcceptorTerminalId", "transactionCurrencyCode", "cardAcceptorNameLocation", "transactionAmount", "international", "preValidated", "posDataCode", "channel"]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    if csv_exists:
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not json_data:
                return response

            # If CSV file is empty, write header row
            if os.path.getsize('data.csv') == 0:
                writer.writerow(json_data[0].keys())

            # Write data rows
            for item in json_data:
                row = [item[column] for column in columns_to_include]
                writer.writerow(row)
    else:
        # If CSV file doesn't exist, create it and write data
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not json_data:
                return response

            writer.writerow(json_data[0].keys())  # Write header row
            for item in json_data:
                row = [item[column] for column in columns_to_include]
                writer.writerow(row)

    return response
