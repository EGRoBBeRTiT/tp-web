from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('settings', views.settings, name='settings'),
    path('ask', views.ask, name='ask'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('hot', views.hot, name='hot')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

