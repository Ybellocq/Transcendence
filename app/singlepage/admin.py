from django.contrib import admin
from .models import User, Game, Friend

 # Register User, Game and Friend models to the admin page
admin.site.register(User)
admin.site.register(Game)
admin.site.register(Friend)

# Change the title of the admin page
admin.site.site_header = 'Transcendence Administration'
admin.site.site_title = 'Transcendence Administration'

