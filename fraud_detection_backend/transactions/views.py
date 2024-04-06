# views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .tasks import process_csv_and_predict, create_csv_from_json
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionAPIView(APIView):
    def post(self, request):
        # Parse JSON data from request
        json_data = JSONParser().parse(request)
        
        # Deserialize the incoming data using TransactionSerializer
        serializer = TransactionSerializer(data=json_data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Get the deserialized data
            validated_data = serializer.validated_data
            
            # Call celery task to process JSON data
            csv_data  = create_csv_from_json.delay(validated_data)
            
            result = process_csv_and_predict.delay(csv_data)

            predictions = result.get()

            # Return response indicating processing started
            return JsonResponse({'predictions': predictions}, status=200)
        else:
            # If the data is invalid, return the validation errors
            return JsonResponse(serializer.errors, status=400)