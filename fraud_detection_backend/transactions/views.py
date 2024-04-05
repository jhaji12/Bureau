# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionAPIView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            # Process transaction data, apply fraud detection logic here
            # Return detection results in JSON format
            return Response({'status': 'ALERT/OK', 'ruleViolated': ['RULE-001'], 'timestamp': 'unix timestamp in string'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
