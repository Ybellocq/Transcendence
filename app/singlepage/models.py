from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.postgres.fields import ArrayField

# Model is a class that represents a table in the database and where every attribute of the class is a field of the table


############################################################################################################
# User model
# This model represents the user table in the database
# It has the following fields:
# - profile_image: an image field that stores the profile picture of the user
# - created_at: a datetime field that stores the date and time when the user was created
# - updated_at: a datetime field that stores the date and time when the user was last updated
# - total_matches: an integer field that stores the total number of matches played by the user
# - win: an integer field that stores the total number of matches won by the user
# - lose: an integer field that stores the total number of matches lost by the user
# - is_online: a boolean field that stores whether the user is online or not
############################################################################################################

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile-picture', default='default_profile_picture.png', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    total_matches = models.IntegerField(default=0, blank=True)
    win = models.IntegerField(default=0, blank=True)
    lose = models.IntegerField(default=0, blank=True)   
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return self.usernames

# Signal to assign a default profile image to a user when it is created
@receiver(post_save, sender='singlepage.User')
def assign_default_image(sender, instance, created, **kwargs):
    if created and not instance.profile_image:
        instance.profile_image = 'default_profile_picture.png'
        instance.save()

# Signal to delete the old profile image when a new one is uploaded
@receiver(pre_save, sender=User)
def delete_old_profile_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
            if old_instance.profile_image != instance.profile_image:
                if old_instance.profile_image:
                    old_image_path = old_instance.profile_image.path
                    default_image_path = default_storage.path(instance.profile_image.field.default)
                    if default_storage.exists(old_image_path) and old_image_path != default_image_path:
                        default_storage.delete(old_image_path)
        except User.DoesNotExist:
            pass

# Signal to update the is_online field of a user when they log in or log out
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    user.is_online = True
    user.save()

# Signal to update the is_online field of a user when they log in or log out
@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    user.is_online = False
    user.save()


############################################################################################################
# Game model
# This model represents the game table in the database
# It has the following fields:
# - local: a boolean field that stores whether the game is local or not
# - tournament: a boolean field that stores whether the game is a tournament or not
# - ended: a boolean field that stores whether the game has ended or not
# - winner_uid: a foreign key field that stores the user who won the game
# - created_at: a datetime field that stores the date and time when the game was created
############################################################################################################

class Game(models.Model):
    player_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player', null=True)
    local = models.BooleanField(default=False)
    tournament = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    winner_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


############################################################################################################
# Friend model
# This model represents the friend table in the database
# It has the following fields:
# - user1_uid: a foreign key field that stores the first user in the friendship
# - user2_uid: a foreign key field that stores the second user in the friendship
# - created_at: a datetime field that stores the date and time when the friendship was created
############################################################################################################

class Friend(models.Model):
    user1_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    created_at = models.DateTimeField(auto_now_add=True)

############################################################################################################
# Tournament model
# This model represents the tournament table in the database
# It has the following fields:
# - owner_uid: a foreign key field that stores the user who created the tournament
# - username_virutal_player: a char array field that stores the username of the virtual players
# - created_at: a datetime field that stores the date and time when the tournament was created
# - state : a char array field that stores the state of the tournament
# - winner_uid: a foreign key field that stores the user who won the tournament
# - number_of_players: an integer field that stores the number of players in the tournament
# - number_of_rounds: an integer field that stores the number of rounds in the tournament
# - current_round: an integer field that stores the current round of the tournament
# - current_match: an integer field that stores the current match of the tournament
# - current_player: an integer field that stores the current player of the tournament
# - current_virtual_player: an integer field that stores the current virtual player of the tournament
############################################################################################################

class Tournament(models.Model):
    owner_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    username_virtual_player = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=False)
    winner_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_winner', null=True)
    number_of_players = models.IntegerField(default=0, blank=True)
    number_of_rounds = models.IntegerField(default=0, blank=True)
    