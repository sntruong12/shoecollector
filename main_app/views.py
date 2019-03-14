from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Shoe, Marketplace
from .forms import CleaningForm
import datetime

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def shoes_index(request):
  shoes = Shoe.objects.all()
  return render(request, 'shoes/index.html', { 'shoes': shoes })

def shoes_detail(request, shoe_id):
  shoe = Shoe.objects.get(id=shoe_id)
  # Get the marketplaces the shoe doesn't have
  print(Shoe.objects.get(id=shoe_id).marketplaces.all())
  marketplaces_shoe_doesnt_have = Marketplace.objects.exclude(id__in = shoe.marketplaces.all().values_list('id'))
  print(marketplaces_shoe_doesnt_have.count())
  cleaning_form = CleaningForm()
  return render(request, 'shoes/detail.html', {
    'shoe': shoe,
    'cleaning_form': cleaning_form,
    'marketplaces': marketplaces_shoe_doesnt_have
  })

def assoc_marketplace(request, shoe_id, marketplace_id):
  Shoe.objects.get(id=shoe_id).marketplaces.add(marketplace_id)
  return redirect('detail', shoe_id=shoe_id)

def add_cleaning(request, shoe_id):
  form = CleaningForm(request.POST)

  if form.is_valid():
    new_cleaning = form.save(commit=False)
    new_cleaning.shoe_id = shoe_id
    new_cleaning.save()
  
  return redirect('detail', shoe_id=shoe_id)

class ShoeCreate(CreateView):
  model = Shoe
  fields = '__all__'
  success_url = '/shoes/'

class ShoeUpdate(UpdateView):
  model = Shoe
  fields = '__all__'

class ShoeDelete(DeleteView):
  model = Shoe
  success_url = '/shoes/'

class MarketplaceList(ListView):
  model = Marketplace

class MarketplaceDetail(DetailView):
  model = Marketplace

class MarketplaceCreate(CreateView):
  model = Marketplace
  fields = '__all__'

class MarketplaceUpdate(UpdateView):
  model = Marketplace
  fields = ['name', 'image_url']

class MarketplaceDelete(DeleteView):
  model = Marketplace
  success_url = '/marketplaces/'
