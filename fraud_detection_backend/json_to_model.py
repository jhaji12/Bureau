import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fraud_detection_backend.settings')
django.setup()

from transactions.models import Transaction

def check_json_keys():
    expected_keys = [
        "mti", "processingCode", "transactionAmount", "dateTimeTransaction",
        "cardholderBillingConversionRate", "stan", "timeLocalTransaction",
        "dateLocalTransaction", "expiryDate", "conversionDate", "merchantCategoryCode",
        "posEntryMode", "acquiringInstitutionCode", "forwardingInstitutionCode", "rrn",
        "cardAcceptorTerminalId", "cardAcceptorId", "cardAcceptorNameLocation",
        "cardBalance", "additionalData48", "transactionCurrencyCode",
        "cardholderBillingCurrencyCode", "posDataCode", "originalDataElement", "channel",
        "encryptedPan", "network", "dcc", "kitNo", "factorOfAuthorization",
        "authenticationScore", "contactless", "international", "preValidated",
        "enhancedLimitWhiteListing", "transactionOrigin", "transactionType",
        "isExternalAuth", "encryptedHexCardNo", "isTokenized", "entityId",
        "moneySendTxn", "mcRefundTxn", "mpqrtxn", "authorisationStatus",
        "latitude", "longitude"
    ]
    
    with open('input.json', 'r') as f:
        data = json.load(f)
        missing_keys = [key for key in expected_keys if key not in data]
        if missing_keys:
            print(f"The following keys are missing from the JSON data: {missing_keys}")
        else:
            print("All expected keys are present in the JSON data.")

def populate_data():
    try:
        with open('input.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):  # Check if data is a dictionary
                Transaction.objects.create(**data)  # Assuming Transaction model accepts kwargs
                print("Data populated successfully.")
            else:
                print("The data loaded from the JSON file is not a dictionary.")
    except Exception as e:
        print(f"An error occurred while populating data: {str(e)}")

if __name__ == '__main__':
    check_json_keys()
    populate_data()
