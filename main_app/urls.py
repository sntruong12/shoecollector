from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('shoes/', views.shoes_index, name='index'),
  path('shoes/<int:shoe_id>/', views.shoes_detail, name='detail'),
  path('shoes/create/', views.ShoeCreate.as_view(), name='shoes_create'),
  path('shoes/<int:pk>/update/', views.ShoeUpdate.as_view(), name='shoes_update'),
  path('shoes/<int:pk>/delete/', views.ShoeDelete.as_view(), name='shoes_delete'),
  path('shoes/<int:shoe_id>/add_cleaning/', views.add_cleaning, name='add_cleaning'),
  path('marketplaces/', views.MarketplaceList.as_view(), name='marketplaces_index'),
  path('marketplaces/<int:pk>/', views.MarketplaceDetail.as_view(), name='marketplaces_detail'),
  path('marketplaces/create/', views.MarketplaceCreate.as_view(), name='marketplaces_create'),
  path('marketplaces/<int:pk>/update/', views.MarketplaceUpdate.as_view(), name='marketplaces_update'),
  path('marketplaces/<int:pk>/delete/', views.MarketplaceDelete.as_view(), name='marketplaces_delete'),
]