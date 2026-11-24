from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('nuevo/', views.alta, name='alta'),
    path('estudiante/<int:student_id>/', views.detalle, name='detalle'),
    path('estudiante/<int:student_id>/editar/', views.editar, name='editar'),
    path('estudiante/<int:student_id>/eliminar/', views.eliminar, name='eliminar'),
    path('dato/<str:tipo>/<str:pk>/eliminar/', views.eliminar_dato, name='eliminar_dato'),
    path('estudiante/<int:student_id>/<str:tipo>/nuevo/', views.dato, name='dato_nuevo'),
    path('estudiante/<int:student_id>/<str:tipo>/<str:pk>/editar/', views.dato, name='dato_editar'),
]