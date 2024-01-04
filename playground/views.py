from django.shortcuts import render
from store.models import Customer

# Create your views here.
def say_hello(request):
    customers = Customer.objects.filter(email__icontains = '.com')
    return render(request, 'hello.html', {'name': 'Abhinav', 'customers': list(customers)})

