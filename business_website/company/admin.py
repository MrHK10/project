from django.contrib import admin
from .models import Job

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'job_location', 'industry']
    list_filter = ['job_type', 'industry', 'employees']

admin.site.register(Job, CompanyAdmin)
