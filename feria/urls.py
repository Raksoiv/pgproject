from django.urls import path
import feria.views as views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('tablero/', views.board),
    path('wbs/', views.wbs),
    path('foros/', views.forum),
    path('archivos/', views.archivos)
]
