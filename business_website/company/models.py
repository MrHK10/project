from django.db import models

class Job(models.Model):
    company_name = models.CharField(primary_key=True, max_length=100)  # Company Name (Primary Key)
    website = models.URLField(max_length=200)  # Website
    job_location = models.CharField(max_length=100)  # Location
    employees = models.CharField(max_length=100)  # Employees
    locations = models.CharField(max_length=100)  # Locations
    job_type = models.CharField(max_length=100)  # Type
    founded = models.CharField(max_length=100)   # Founded
    revenue = models.CharField(max_length=100)  # Revenue
    industry = models.CharField(max_length=100)  # Industry
    all_location_info = models.TextField()  # All Location Info
    
    def __str__(self):
        return self.company_name + ' - ' + self.job_location

    def get_revenue_range(self):
        if " to " in self.revenue and "(USD)" in self.revenue:
            lower, upper = self.revenue.split(" to ")
            lower = lower.strip().replace("$", "").replace(" million", "").replace(" billion", "")
            upper = upper.strip().replace("$", "").replace(" million", "").replace(" billion", "")
            return f"${lower} million to ${upper} billion (USD)"
        else:
            return self.revenue
