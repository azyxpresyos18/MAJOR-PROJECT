from django.urls import path
from . import views

urlpatterns = [
    path('',                             views.login_view,             name='login'),
    path('logout/',                      views.logout_view,            name='logout'),
    path('home/',                        views.home,                   name='home'),
    path('clients/',                     views.clients,                name='clients'),
    path('products/',                    views.products,               name='products'),
    path('departmentalize/',             views.departmentalize,        name='departmentalize'),
    path('location/',                    views.location,               name='location'),
    path('schedule/',                    views.schedule,               name='schedule'),
    path('api/schedule/<int:pk>/status/',views.update_schedule_status, name='update_schedule_status'),
    path('api/schedule/<int:pk>/delete/',views.delete_schedule,        name='delete_schedule'),
]
