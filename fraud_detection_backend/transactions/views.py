# views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
# from .tasks import process_csv_and_predict
from .process_csv_and_prediction import process_csv_and_predict
from .json_to_csv import create_csv_from_json
from .models import Transaction
from .serializers import TransactionSerializer
from .serializers import PredictionSerializer

class TransactionAPIView(APIView):
    def post(self, request):
        try:
            # Parse JSON data from request
            json_data = JSONParser().parse(request)
            
            # Deserialize the incoming data using TransactionSerializer
            # serializer = TransactionSerializer(data=json_data)
            
            # Check if the data is valid
            
            csv_data  = create_csv_from_json(json_data)
            
            result = process_csv_and_predict(csv_data)
            
            # Return response indicating processing started
            return JsonResponse({'predictions': result}, status=200)
        except Exception as e:
            print(e)
