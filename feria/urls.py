from django.urls import path
import feria.views as views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('tablero/', views.board),
    path('entregas/', views.epics),
    path('entregas/<int:epic_id>/', views.epic_detail),
    path('foros/', views.forum),
    path('foros/<int:forum_id>/', views.forum_detail),
    path('foros/mensaje/<int:message_id>/', views.message_detail),
    path('archivos/', views.archivos)
]
