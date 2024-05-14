from django.urls import path
from core import views, transfer, transaction, payment_request
from core import transaction

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    
    #Transfers
    path("search-account/", transfer.search_users_account_number, name="search-account"),
    path("amount-transfer/<account_number>/", transfer.AmountTransfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.TransferConfirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/", transfer.TransferProcess, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>/", transfer.TransferCompleted, name="transfer-completed"),
    
    # transactions
    path("transactions/", transaction.transaction_lists, name="transactions"),
    path("transaction-detail/<transaction_id>", transaction.transaction_detail, name="transaction-detail"),
    
    #Paymente request
     path("request-search-account/",payment_request.SearchUserRequest, name="request-search-account"),
     path("amount-request/<account_number>/",payment_request.AmountRequest, name="amount-request"),
     
]