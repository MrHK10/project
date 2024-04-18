from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import requests 
from .models import Job
from geopy.geocoders import Nominatim
from django.db.models import Avg
import re
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Avg, F
from django.contrib.auth.decorators import login_required
from .models import Job
from geopy.geocoders import Nominatim
import re
from django.db.models import Func, F, Value, CharField
from django.db.models import Value, DecimalField
from django.db.models.functions import Cast
from django.db.models import Min, Max
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models.functions import Substr, Length
import base64
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import Job
from django.db.models import Q







class ExtractNumeric(Func):
    function = 'regexp_replace'
    template = "%(function)s(%(expressions)s, '[^\d.]+', '', 'g')"
    output_field = CharField()
# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

def dashboard(request):
    total_companies = Job.objects.values('company_name').distinct().count()
    total_website_count = Job.objects.values('website').distinct().count()

    # Fetch the data of the first 10 companies excluding those with unknown or non-applicable revenue
    first_10_companies = Job.objects.exclude(Q(revenue='Unknown') | Q(revenue='Non-Applicable')).order_by('revenue')[:10]

    # Prepare data for the chart
    companies = [company.company_name for company in first_10_companies]
    revenues = [company.revenue for company in first_10_companies]

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the figure size here (width, height)
    bars = ax.bar(companies, revenues)
    ax.set_ylabel('Revenue')
    ax.set_title('First 10 Companies with Known Revenue')
    ax.tick_params(axis='x', rotation=30)  # Rotate x-axis tick labels by 30 degrees

    # Annotate the bars with revenue values
    for bar, revenue in zip(bars, revenues):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{revenue}', ha='center', va='bottom')

    # Save the chart to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)

    # Convert the buffer content to base64 encoding
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'dashboard.html', {
        'chart_data': chart_data,
        'total_companies': total_companies,
        'total_website_count': total_website_count,
        'first_10_companies': first_10_companies
    })


from .models import Job
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import JobForm  # Import your JobForm

def Company_list(request):
    jobs_list = Job.objects.all()

    # Filter based on search query
    search_query = request.GET.get('search_query')
    if search_query:
        jobs_list = jobs_list.filter(company_name__icontains=search_query)
    else:
        search_query = "search by company"  # Set search_query to None if it's empty

    # Get the total number of unique company names
    total_companies = jobs_list.values('company_name').distinct().count()

    paginator = Paginator(jobs_list, 20)  # Show 8 jobs per page

    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    if request.method == 'POST':
        form = JobForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('company_list')  # Redirect to the same page after successful submission
    else:
        form = JobForm()  # Create a new instance of the form

    return render(request, 'Company_list.html', {'jobs': jobs, 'search_query': search_query, 'total_companies': total_companies, 'form': form})

def companylocation(request, company_name):
    
    # Fetch locations associated with the specified company name
    locations = Job.objects.filter(company_name=company_name).values_list('job_location', flat=True).distinct()

    geolocator = Nominatim(user_agent="company_locations")
    location_data = []
    total_latitude = 0
    total_longitude = 0
    total_locations = 0

    for location in locations:
        try:
            geocoded_location = geolocator.geocode(location)
            if geocoded_location:
                total_latitude += geocoded_location.latitude
                total_longitude += geocoded_location.longitude
                total_locations += 1
                location_data.append({
                    'location': location,
                    'latitude': geocoded_location.latitude,
                    'longitude': geocoded_location.longitude
                })
        except Exception as e:
            print(f"Error geocoding {location}: {str(e)}")

    # Calculate the average latitude and longitude
    if total_locations > 0:
        avg_latitude = total_latitude / total_locations
        avg_longitude = total_longitude / total_locations
    else:
        # Default to a location if no valid locations are found
        avg_latitude = 0
        avg_longitude = 0

    return render(request, 'companylocations.html', {'location_data': location_data, 'avg_latitude': avg_latitude, 'avg_longitude': avg_longitude},)

def geocode_address(location, address):
    query = f"{location}, {address}"
    endpoint = f"https://nominatim.openstreetmap.org/search?format=json&q={query}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        results = response.json()
        if results:
            location = results[0]
            latitude = location['lat']
            longitude = location['lon']
            return latitude, longitude
        else:
            print("No results found for the address:", query)
    else:
        print("HTTP error:", response.status_code, "for address:", query)
    return None

def extract_location_info(all_location_info):
    locations = all_location_info.split('\n\n')
    extracted_info = []
    for loc in locations:
        lines = loc.split('\n')
        if len(lines) > 1:  # Check if lines list has at least two elements
            location_name = lines[0].split(': ')[1]
            address = lines[1].split(': ')[1]
            extracted_info.append((location_name, address))
        else:
            print("Invalid format for location info:", loc)
    return extracted_info
from django.shortcuts import get_object_or_404
def Alllocations(request, company_name):
    locations_data = Job.objects.filter(company_name=company_name).values_list('all_location_info', flat=True).distinct()
    job = get_object_or_404(Job, company_name=company_name)
    all_locations = []
    for data in locations_data:
        extracted_info = extract_location_info(data)
        for location_name, address in extracted_info:
            coordinates = geocode_address(location_name, address)
            if coordinates:
                latitude, longitude = coordinates
                all_locations.append({
                    'location_name': location_name,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude
                })
            else:
                print("Failed to geocode the location:", location_name)
    current_industry = job.industry
    random_companies = Job.objects.filter(industry=current_industry).exclude(company_name=company_name).order_by('?')[:9]  # Change 5 to the desired number of recommendations
    
    return render(request, 'ALL_locations.html', {'locations': all_locations, 'job': job, 'random_companies': random_companies})

def about(request):
        return render(request, 'about.html')