from django.contrib import admin
from account.models import Account, KYC
from userauths.models import User
from import_export.admin import ImportExportModelAdmin

class AccountAdminModel(ImportExportModelAdmin):
    list_per_page = 25
    list_editable = ['account_status', 'account_balance'] 
    list_display = ['user', 'account_number' ,'account_status', 'account_balance'] 
    list_filter = ['account_status']

class KYCAdmin(ImportExportModelAdmin):
    list_per_page = 25
    list_display = ['user'] 


admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)