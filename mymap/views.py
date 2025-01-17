from django.shortcuts import render
from mymap.models import MapPoint, Schools
from mymap.forms import CSVUploadForm   # Import the form class
import pandas as pd
import numpy as np

from django.http import JsonResponse
from django.db.models import F
from django.db.models.functions import Sqrt, Power


# Create your views here.
def index(request):
    # allpoints = MapPoint.objects.all()    
    allpoints = Schools.objects.filter(stage_number__gte=1)
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file_content'])
            return render(request, "mymap/index.html", {'allpoints':allpoints, 'form':CSVUploadForm()})
        else:
            return render(request, "mymap/index.html", {'allpoints':allpoints, 'form':form})
    else:
        form = CSVUploadForm()
        return render(request, "mymap/index.html", {'allpoints':allpoints, 'form':form}) 
    
def handle_uploaded_file(f):
    df = pd.read_csv(f)
    df['# Classrooms'] = df['# Classrooms'].fillna(0)
    # loop thru rows
    for index, row in df.iterrows():
        school=Schools.objects.get_or_create(
            name=row['Name'], 
            lat=row['Latitude'], 
            lon=row['Longitude'], 
            Level=row['Level'], 
            Status=row['Status'], 
            Sponsor=row['Sponsor'], 
            Classrooms=row['# Classrooms'])

    print(df.head())

# New view function for the school map (this was the simple version, but too may points included)
# def school_map(request):
#     # Fetch only schools with stage_number = 1 or stage_number = 2
#     allpoints = Schools.objects.filter(stage_number__in=[1, 2])
#     return render(request, 'index.html', {'allpoints': allpoints})

# New view function for the school map
def school_map(request):
    # Fetch up to 10 schools with stage_number = 1
    stage1_points = Schools.objects.filter(stage_number=1)[:10]
    
    # Fetch up to 10 schools with stage_number = 2
    stage2_points = Schools.objects.filter(stage_number=2)[:10]
    
    # Combine the querysets
    allpoints = list(stage1_points) + list(stage2_points)
    
    return render(request, 'index.html', {'allpoints': allpoints})

def get_nearby_schools(request, lat, lon):
    lat = float(lat)
    lon = float(lon)

    # Calculate distance using the Haversine formula approximation
    nursery_schools = Schools.objects.filter(stage_number=1).annotate(
        distance=Sqrt(
            Power(F('lat') - lat, 2) + Power(F('lon') - lon, 2)
        )
    ).order_by('distance')[:10]

    primary_schools = Schools.objects.filter(stage_number=2).annotate(
        distance=Sqrt(
            Power(F('lat') - lat, 2) + Power(F('lon') - lon, 2)
        )
    ).order_by('distance')[:10]

    schools = list(nursery_schools) + list(primary_schools)

    schools_data = [
        {'name': school.name, 'lat': school.lat, 'lon': school.lon, 'stage_number': school.stage_number}
        for school in schools
    ]

    return JsonResponse(schools_data, safe=False)
