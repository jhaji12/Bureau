# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionAPIView(APIView):
    def post(self, request):
        # Deserialize the incoming data using TransactionSerializer
        serializer = TransactionSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Get the deserialized data
            validated_data = serializer.validated_data
            
            # Extract transaction attributes from validated data
            transaction_amount = validated_data.get('transaction_amount')
            # Extract other transaction attributes similarly
            
            # Apply fraud detection logic
            if transaction_amount >= 0.7 * validated_data['card_balance'] and validated_data['card_balance'] >= 300000:
                # If the transaction amount violates RULE-001
                detection_result = {
                    'status': 'ALERT',
                    'ruleViolated': ['RULE-001'],
                    'timestamp': '1234567890'  # Replace with actual timestamp
                }
            else:
                # If no fraud detected
                detection_result = {
                    'status': 'OK',
                    'ruleViolated': [],
                    'timestamp': '1234567890'  # Replace with actual timestamp
                }
            
            # Return the detection result in JSON format
            return Response(detection_result)
        else:
            # If the data is invalid, return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
