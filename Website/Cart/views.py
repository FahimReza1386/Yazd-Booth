from django.shortcuts import render


# Create your views here.
def Cart_Summary(request):
    return render(request=request, template_name='Cart_Summary.html' , context={})

def Cart_Add(request):
    pass

def Cart_Delete(request):
    pass

def Cart_Update(request):
    pass