from django.shortcuts import render

def where_find_us_view(request):
    return render(request, 'where_find_us/where_find_us.html')


