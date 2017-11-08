from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.HomePage.as_view(),name='home'),
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^accounts/',include('django.contrib.auth.urls')),
    url(r'^thanks/$',views.ThanksPage.as_view(),name='thanks'),
    url(r'^test/$',views.TestPage.as_view(), name ='test'),

]
