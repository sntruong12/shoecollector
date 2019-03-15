from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator 
import datetime

CLEAN_STATE = (
  ('P', 'partially'),
  ('C', 'completely')
)

class Marketplace(models.Model):
  name = models.CharField(max_length=100)
  image_url = models.CharField(max_length=280)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('marketplaces_detail', kwargs={ 'pk': self.id })

class Shoe(models.Model):
  brand = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  color = models.CharField(max_length=100)
  style = models.CharField(max_length=100)
  retail = models.IntegerField(default=1 ,validators=[MinValueValidator(0, message='The retail needs to be greater than 0')])
  release = models.IntegerField()
  description = models.TextField(max_length=280)
  marketplaces = models.ManyToManyField(Marketplace)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={ 'shoe_id': self.id })

  def cleaned_in_past_30_days(self):
    last_cleaning_date = self.cleaning_set.first().date
    current_date = datetime.date.today()
    delta = current_date - last_cleaning_date
    days = delta.days

    return True if days > 30 else False

class Cleaning(models.Model):
  date = models.DateField('date of last cleaning')
  state = models.CharField(
    max_length=1,
    choices=CLEAN_STATE,
    default=CLEAN_STATE[0][0]
  )
  shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_state_display()} cleaned on {self.date}"

  class Meta:
    ordering =['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

    def __str__(self):
      return f"Photo for shoe_id: {self.shoe_id} @{self.url}"
