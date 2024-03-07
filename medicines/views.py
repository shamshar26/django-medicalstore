from django.shortcuts import render,redirect
from .forms import MedicineForm
from .models import Medicine
from django.core.paginator import Paginator

def medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'created.html')
        
    else:
        form =MedicineForm()
    return render(request, 'create.html', {'form': form})

def medicine_delete(request,pk):
    med=Medicine.objects.get(pk=pk)  
    if request.method == 'POST':
        med.delete()
        return render(request,'deleted.html')
    
    return render(request,'delete.html',{'medicine':med})


def medicine_read(request):
  search_query = request.GET.get('search_query', '')
    
  if search_query:
        medicine_list = Medicine.objects.filter(name__icontains=search_query)
  else:
        medicine_list = Medicine.objects.all()
  return render(request,'read.html',{'medicine_list':medicine_list}) 


def medicine_update(request, id):
    medicine = Medicine.objects.get(pk=id)
    if request.method == 'POST':
        form = MedicineForm(request.POST,instance=medicine)
        if form.is_valid():
            form.save()
            return render(request,'updated.html')
    else:
        form =MedicineForm(instance=medicine)           
    return render(request, 'update.html', {'form': form}) 



