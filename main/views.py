from django.shortcuts import render

def main(request):
    return render(request, 'landing_page.html')
