from django.urls import path
from . import views 

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.signin, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.signout, name='logout'),
    path('parameters/categories', views.categories, name='categories'),
    path('parameters/measurement_units', views.measurement_units, name='measurement_units'),
    path('parameters/index/add_category', views.add_category, name='add_category'),
    path('parameters/index/edit_category', views.edit_category, name='edit_category'),
    path('parameters/index/delete_category', views.delete_category, name='delete_category'),
    path('parameters/index/add_measurement_unit', views.add_measurement_unit, name='add_measurement_unit'),
    path('parameters/index/edit_measurement_unit', views.edit_measurement_unit, name='edit_measurement_unit'),
    path('parameters/index/delete_measurement_unit', views.delete_measurement_unit, name='delete_measurement_unit'),
    path('elements/index', views.elements_index, name='elements.index'),
    path('elements/index/add_elements', views.add_elements, name='add_elements'),
    path('elements/index/edit_elements', views.edit_elements, name='edit_elements'),
    path('elements/index/delete_elements', views.delete_elements, name='delete_elements'),
    path('inventories/index', views.inventories_index, name='inventories.index'),   
    path('inventories/index/add_inventories', views.add_inventories, name='add_inventories'),
    path('inventories/index/edit_inventories', views.edit_inventories, name='edit_inventories'),
    path('inventories/index/delete_inventories', views.delete_inventories, name='delete_inventories'),
    path('domicilie', views.domicilie, name='domicilie'),
    path('save_domicilie', views.save_domicilie, name='save_domicilie'),
    path('my_domicilies/cancel', views.cancel, name='cancel'),
    path('domicilies/assign', views.assign_domicilies, name='assign_domicilies'),
    path('assign', views.assign, name='assign'),
    path('my_domicilies', views.my_domicilies, name='my_domicilies'),
    path('my_domicilies/complete', views.complete, name='complete'),
    path('my_domicilies/domicilies_user', views.domicilies_user, name='domicilies_user'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)