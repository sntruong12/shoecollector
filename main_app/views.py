from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Shoe, Marketplace, Photo
from .forms import CleaningForm
import datetime
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'shoecollector9000'

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def shoes_index(request):
  shoes = Shoe.objects.filter(user=request.user)
  return render(request, 'shoes/index.html', { 'shoes': shoes })

@login_required
def shoes_detail(request, shoe_id):
  shoe = Shoe.objects.get(id=shoe_id)
  # Get the marketplaces the shoe doesn't have
  marketplaces_shoe_doesnt_have = Marketplace.objects.exclude(id__in = shoe.marketplaces.all().values_list('id'))
  cleaning_form = CleaningForm()
  return render(request, 'shoes/detail.html', {
    'shoe': shoe,
    'cleaning_form': cleaning_form,
    'marketplaces': marketplaces_shoe_doesnt_have
  })

@login_required
def assoc_marketplace(request, shoe_id, marketplace_id):
  Shoe.objects.get(id=shoe_id).marketplaces.add(marketplace_id)
  return redirect('detail', shoe_id=shoe_id)

@login_required
def unassoc_marketplace(request, shoe_id, marketplace_id):
  Shoe.objects.get(id=shoe_id).marketplaces.remove(marketplace_id)
  return redirect('detail', shoe_id=shoe_id)

@login_required
def add_cleaning(request, shoe_id):
  form = CleaningForm(request.POST)

  if form.is_valid():
    new_cleaning = form.save(commit=False)
    new_cleaning.shoe_id = shoe_id
    new_cleaning.save()
  
  return redirect('detail', shoe_id=shoe_id)

@login_required
def add_photo(request, shoe_id):
	# photo-file was the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to shoe_id or shoe if you have a shoe object
      photo = Photo(url=url, shoe_id=shoe_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', shoe_id=shoe_id)

class ShoeCreate(LoginRequiredMixin, CreateView):
  model = Shoe
  fields = ['brand', 'name', 'color', 'style', 'retail', 'release', 'description']
  # This method is called when a valid
  # cat form has being submitted
  def form_valid(self, form):
    # Assign the logged in user
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class ShoeUpdate(LoginRequiredMixin, UpdateView):
  model = Shoe
  fields = '__all__'

class ShoeDelete(LoginRequiredMixin, DeleteView):
  model = Shoe
  success_url = '/shoes/'

class MarketplaceList(LoginRequiredMixin, ListView):
  model = Marketplace

class MarketplaceDetail(LoginRequiredMixin, DetailView):
  model = Marketplace

class MarketplaceCreate(LoginRequiredMixin, CreateView):
  model = Marketplace
  fields = '__all__'

class MarketplaceUpdate(LoginRequiredMixin, UpdateView):
  model = Marketplace
  fields = ['name', 'image_url']

class MarketplaceDelete(LoginRequiredMixin, DeleteView):
  model = Marketplace
  success_url = '/marketplaces/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)