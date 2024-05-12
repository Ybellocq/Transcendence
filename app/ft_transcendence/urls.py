"""
URL configuration for ft_transcendence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from singlepage import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler500

handler500 = 'singlepage.views.handler500'
handler404 = 'singlepage.views.handler404'

urlpatterns = [
    # Main pages
    path('admin/', admin.site.urls), # Admin page localhost:8000/admin
    path('', views.index, name='index'), # Index page localhost:8000
    path('game/', views.game, name='game'), # Game page localhost:8000/game
    path('ia', views.gameia, name='gameia'), # Game page localhost:8000/game/ia
    path('register/', views.register, name='register'), # Register page localhost:8000/register
    path('welcome/', views.welcome, name='welcome'), # Welcome page localhost:8000/welcome
    path('profile/', views.profile, name='profile'), # Profile page localhost:8000/profile
    path('friends/', views.friends, name='friends'), # Friends page localhost:8000/friends
    path('gamepage/', views.gamepage, name='gamepage'), # Game page localhost:8000/gamepage
    path('settings/', views.settings, name='settings'), # Settings page localhost:8000/settings
    path('tournaments/', views.tournaments, name='tournaments'), # Tournament page localhost:8000/tournament
    path('tournament_match/', views.tournament_match, name='tournament_match'), # Tournament page localhost:8000/tournament
    path('tournaments_overview/', views.tournaments_overview, name='tournaments_overview'), # Tournament page localhost:8000/tournament
    path('404/', views.handler404, name='404'), # 404 page localhost:8000/404
    # API endpoints
    path('search_friends/', views.search_friends, name='search_friends'), # Search friends endpoint
    path('add_friends/', views.add_friends, name='add_friends'), # Friend request endpoint
    path('update_score/', views.update_score, name='update_score'), # Update score endpoint for game
    path('update_loss/', views.update_loss, name='update_loss'), # Update loss endpoint for game 
    path('logout/', views.logout_view, name='logout'), # Logout endpoint
    path('create_tournament/', views.create_tournament, name='create_tournament'), # Create tournament endpoint
    path('update_tournament_match/', views.update_tournament_match, name='update_tournament_match'), # Update tournament match endpoint
    path('', include('django_prometheus.urls')) # Is the localhost:8000/metrics endpoint
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)