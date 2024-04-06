import csv
import os
import json
from django.http import HttpResponse

def create_csv_from_json(json_data):
    csv_exists = os.path.isfile('data.csv')
    
    columns_to_include = ['dateTimeTransaction', 'latitude', 'longitude', 'cardBalance', 'cardAcceptorId', "cardAcceptorTerminalId", "transactionCurrencyCode", "cardAcceptorNameLocation", "transactionAmount", "international", "preValidated", "posDataCode", "channel"]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data.csv"'

    if csv_exists:
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,  fieldnames=json_data.keys())

            if not json_data:
                return response

            # Write data rows
            writer.writerow(json_data)
    else:
        # If CSV file doesn't exist, create it and write data
        with open('data.csv', 'w', newline='') as csvfile:
            #writer = csv.DictWriter(csvfile, fieldnames=columns_to_include)
            writer = csv.DictWriter(csvfile, fieldnames=json_data.keys())
            writer.writeheader()  # Write header row

            if not json_data:
                return response

            # Write data rows
            writer.writerow(json_data)

    return response
