import csv
import os
import json
from django.http import HttpResponse

def create_csv_from_json(request):
    csv_exists = os.path.isfile('data.csv')
    with open('input.json', 'r') as f:
        data = json.load(f)

        columns_to_include = ['dateTimeTransaction', 'latitude', 'longitude', 'cardBalance', 'cardAcceptorId', "cardAcceptorTerminalId", "transactionCurrencyCode", "cardAcceptorNameLocation", "transactionAmount", "international", "preValidated", "posDataCode", "channel"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)

        if csv_exists:
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not data:
                    return response

                # If CSV file is empty, write header row
                if os.path.getsize('data.csv') == 0:
                    writer.writerow(data[0].keys())

                # Write data rows
                for item in data:
                    row = [item[column] for column in columns_to_include]
                    writer.writerow(row)
        else:
             # If CSV file doesn't exist, create it and write data
            with open('data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not data:
                    return response

                writer.writerow(data[0].keys())  # Write header row
                for item in data:
                    row = [item[column] for column in columns_to_include]
                    writer.writerow(row)

        return response