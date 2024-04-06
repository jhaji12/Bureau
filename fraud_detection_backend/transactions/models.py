# transactions/models.py
from django.db import models


class Transaction(models.Model):
    mti = models.CharField(max_length=4, null=True)
    processingCode = models.CharField(max_length=6, null=True)
    transactionAmount = models.DecimalField(max_digits=10, decimal_places=2)
    dateTimeTransaction = models.CharField(max_length=12)
    cardholderBillingConversionRate = models.CharField(max_length=8, null=True)
    stan = models.CharField(max_length=10, null=True)
    timeLocalTransaction = models.CharField(max_length=6, null=True)
    dateLocalTransaction = models.CharField(max_length=4, null=True)
    expiryDate = models.CharField(max_length=4, null=True)
    conversionDate = models.CharField(max_length=4, null=True)
    merchantCategoryCode = models.CharField(max_length=4, null=True)
    posEntryMode = models.CharField(max_length=3, null=True)
    acquiringInstitutionCode = models.CharField(max_length=6, null=True)
    forwardingInstitutionCode = models.CharField(max_length=6, null=True)
    rrn = models.CharField(max_length=10, null=True)
    cardAcceptorTerminalId = models.CharField(max_length=10)
    cardAcceptorId = models.CharField(max_length=9)
    cardAcceptorNameLocation = models.CharField(max_length=50)
    cardBalance = models.DecimalField(max_digits=10, decimal_places=2)
    additionalData48 = models.CharField(max_length=1, null=True)
    transactionCurrencyCode = models.CharField(max_length=3)
    cardholderBillingCurrencyCode = models.CharField(max_length=3, null=True)
    posDataCode = models.CharField(max_length=24)
    originalDataElement = models.CharField(max_length=50, null=True) 
    channel = models.CharField(max_length=4)
    encryptedPan = models.CharField(max_length=44, null=True)
    network = models.CharField(max_length=10, null=True)
    dcc = models.BooleanField(null=True)
    kitNo = models.CharField(max_length=10, null=True)
    factorOfAuthorization = models.IntegerField(null=True)
    authenticationScore = models.IntegerField(null=True)
    contactless = models.BooleanField(null=True)
    international = models.BooleanField()
    preValidated = models.BooleanField()
    enhancedLimitWhiteListing = models.BooleanField(null=True)
    transactionOrigin = models.CharField(max_length=4, null=True)
    transactionType = models.CharField(max_length=4, null=True)
    isExternalAuth = models.BooleanField(null=True)
    encryptedHexCardNo = models.CharField(max_length=64, null=True)
    isTokenized = models.BooleanField(null=True)
    entityId = models.CharField(max_length=10, null=True)
    moneySendTxn = models.BooleanField(null=True)
    mcRefundTxn = models.BooleanField(null=True)
    mpqrtxn = models.BooleanField(null=True)
    authorisationStatus = models.BooleanField(null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


