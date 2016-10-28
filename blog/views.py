from django.shortcuts import render

# Create views
def home(request):
	return render(request, 'home.html', {})
