from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UsernamesForm, PasswordForm, SignupForm, UpdateUserNameForm, UpdatePictureForm, UpdatePasswordForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from singlepage.models import User, Friend, Game, Tournament, Tournament_Match
import time
import json
from django.contrib.auth import get_user_model
from django.utils import timezone


############################################################################################################
# All the views of the application
# Each view is a function that takes a request as an argument and returns a response
# The response can be a rendered template, a redirect, a JSON response, etc.
############################################################################################################

# View Index page : localhost:8000/ 
# This view is the main page of the application
# It displays a login form and a register link
# If the user is already authenticated, it redirects to the welcome page

def index(request):
    if request.user.is_authenticated:
        return redirect('/welcome/')
    message = ''
    if request.method == 'POST':
        form = UsernamesForm(request.POST)
        password_form = PasswordForm(request.POST)
        if form.is_valid() and password_form.is_valid():
            user = form.cleaned_data['usernames']
            password = password_form.cleaned_data['password'] 
            user = authenticate(username=user, password=password)
            if user:
                login(request, user)
                return redirect('/welcome/')
            else:
                message = 'Nom d’utilisateur ou mot de passe incorrect'
    else:
        form = UsernamesForm()
        password_form = PasswordForm()
    return render(request, 'index.html', {'form': form, 'password_form': password_form, 'message': message})

# View Register page : localhost:8000/register/
# This view displays a registration form
# If the form is valid, it creates a new user and logs them in
# If the user is already authenticated, it redirects to the welcome page

def register(request):
    if request.user.is_authenticated:
        return redirect('/welcome/')
    form = SignupForm()
    message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            login(request, user)
            return redirect('/welcome/')
        else:
            message = 'Votre formulaire contient des erreurs'
            return render(request, 'register.html', {'form': form, 'message': message})
    return render(request, 'register.html', {'form': form})

# View Welcome page : localhost:8000/welcome/
# This view displays the welcome page of the application
# It displays the user's profile picture, username, and a list of friends
# If the user is not authenticated, it redirects to the index page

@login_required
def welcome(request):
    my_friends = Friend.objects.filter(user1_uid_id=request.user.id)
    friends = []
    for friend in my_friends:
        friend_user = get_user_model().objects.get(id=friend.user2_uid.id)
        friend_is_online = friend_user.is_online
        friend_is_ongame = friend_user.in_game
        online_status = 'En ligne' if friend_is_online else 'Hors ligne'
        game_status = 'En jeu' if friend_is_ongame else 'Hors jeu'
        friends.append({
            'username': friend_user.username,
            'profile_image': request.build_absolute_uri(friend_user.profile_image.url),
            'id': friend_user.id,
            'is_online': online_status,
            'is_ongame': game_status,
        })
    if request.user.is_authenticated:
        return render(request, 'welcome.html', {'user': request.user, 'friends': friends})
    else:
        message = 'Vous devez être connecté pour accéder à cette page'
        return render(request, 'index.html', {'message': message, 'form': UsernamesForm(), 'password_form': PasswordForm()})

# View Settings page : localhost:8000/settings/
# This view displays the settings page of the application
# It allows the user to update their username, profile picture, and password
# If the form is valid, it updates the user's information and displays a success message
# If the user is not authenticated, it redirects to the index page

@login_required
def settings(request):
    picture_form = UpdatePictureForm(instance=request.user)
    form = UpdateUserNameForm(instance=request.user)
    password_form = UpdatePasswordForm(instance=request.user)
    message = ''
    if request.method == 'POST':
        picture_form = UpdatePictureForm(request.POST, request.FILES, instance=request.user)
        form = UpdateUserNameForm(request.POST, instance=request.user)
        password_form = UpdatePasswordForm(request.POST, instance=request.user)
        if form.is_valid() and picture_form.is_valid():
            user = form.save()
            picture_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès')
        if password_form.is_valid():
            new_password = password_form.cleaned_data['password']
            if new_password is not None and new_password != '':
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            else:
                message = 'Veuillez entrer un mot de passe valide'
                password_form = UpdatePasswordForm(instance=request.user)
        else:
            message = 'Votre formulaire contient des erreurs'
            picture_form = UpdatePictureForm(instance=request.user)
            form = UpdateUserNameForm(instance=request.user)
    return render(request, 'settings.html', {'form': form, 'picture_form': picture_form, 'password_form': password_form, 'message': message})

# View Profile page : localhost:8000/profile/
# This view displays the profile page of the application
# It displays the user's total matches, wins, losses, and win rate
# If the user is not authenticated, it redirects to the index page

@login_required
def profile(request):
    total_matches = request.user.total_matches
    win = request.user.win
    lose = request.user.lose
    
    matches = Game.objects.filter(ended=True).filter(player_uid=request.user.id)
    win_matches = matches.filter(winner_uid=request.user.id)
    lose_matches = matches.exclude(winner_uid=request.user.id)

    data = {
        'win_matches': win_matches.count(),
        'lose_matches': lose_matches.count()
    }
    return render(request, 'profile.html', {'total_matches': total_matches, 'win': win, 'lose': lose, 'data': data, 'matches': matches})

# View Match Infos page : localhost:8000/match_infos/
# This view displays the match infos page of the application
# It displays the match infos page with the user's profile picture, username, and a game

@login_required
def match_infos(request, match_id):
    match = Game.objects.get(id=match_id)
    match.score = Game.objects.get(id=match_id).score_player1
    match.score_player2 = Game.objects.get(id=match_id).score_player2
    match.winner = Game.objects.get(id=match_id).winner_uid
    if match.winner == request.user:
        match.winner = 'Vous'
    else:
        match.winner = 'Adversaire'
    match.time = Game.objects.get(id=match_id).time
    # Convert the time miliseconds to seconds
    match.time = match.time / 1000
    match.time = time.strftime('%M:%S', time.gmtime(match.time))
    return render(request, 'match_infos.html', {'match': match})

# Tournament page : localhost:8000/tournament/
# This view displays the tournament page of the application
# It displays the tournament page with the user's profile picture, username, and a game
# If the user is not authenticated, it redirects to the index page

@login_required
def tournaments(request):
    if request.user.is_authenticated:
        tournaments = Tournament.objects.filter(owner_uid_id=request.user.id)
        tournaments = tournaments.filter(state=False)
        # if user id have already created a tournament and it is not started yet return a message
        data = []
        for tournament in tournaments:
            data.append({
                'owner_name': request.user.username, 
                'tournament': tournament,
                'id': tournament.id,
                'number_of_players': tournament.number_of_players,
                'number_of_matchs': tournament.number_of_matchs,
                'number_of_rounds': tournament.number_of_rounds,
                'created_at': tournament.created_at,
                'state': tournament.state,
                'username_virtual_player': tournament.username_virtual_player,
            })
        return render(request, 'tournaments.html', {'tournaments': data})
    else:
        message = 'Vous devez être connecté pour accéder à cette page'
        return render(request, 'index.html', {'message': message, 'form': UsernamesForm(), 'password_form': PasswordForm()})

# Tournament Overview page : localhost:8000/tournament_overview/
# This view displays the overview of the actual Tournament
# It displays the tournament page with the user's profile picture, all the players and the actual round
# If the user is not authenticated, it redirects to the index page

@login_required
def tournaments_overview(request):
    if request.user.is_authenticated:
        tournaments_overview = Tournament.objects.filter(owner_uid_id=request.user.id).last()
        # if user id have already created a tournament and it is not started yet return a message
        data = []
        data.append({
            'owner_name': request.user.username,
            'tournament': tournaments_overview,
            'id': tournaments_overview.id,
            'number_of_players': tournaments_overview.number_of_players,
            'number_of_matchs': tournaments_overview.number_of_matchs,
            'number_of_rounds': tournaments_overview.number_of_rounds,
            'created_at': tournaments_overview.created_at,
            'state': tournaments_overview.state,
            'username_virtual_player': tournaments_overview.username_virtual_player,
            'winner_name': tournaments_overview.winner_name,
        })

        matchs_data = []
        matchs_list = Tournament_Match.objects.filter(tournament_id=tournaments_overview.id)
        for matchs in matchs_list:
            matchs_data.append({
                'tournament_id': tournaments_overview.id,
                'id': matchs.match_id,
                'round': matchs.round_id,
                'player1': matchs.player1,
                'player2': matchs.player2,
                'winner': matchs.winner,
            })

        return render(request, 'tournaments_overview.html', {'tournaments': data, 'matchs_list': matchs_data})
    else:
        message = 'Vous devez être connecté pour accéder à cette page'
        return render(request, 'index.html', {'message': message, 'form': UsernamesForm(), 'password_form': PasswordForm()})


# View Friends page : localhost:8000/friends/
# This view displays the friends page of the application
# It displays a list of all users in the database
# If the user is not authenticated, it redirects to the index page

@login_required
def friends(request):
    userList = User.objects.all()
    return render(request, 'friends.html', {'users': userList})

# View Game page : localhost:8000/gamepage/
# This view displays the game page of the application
# It displays the game page with the user's profile picture, username, and a game
# If the user is not authenticated, it redirects to the index page

@login_required
def gamepage(request):
    return render(request, 'gamepage.html', {'user': request.user})
# View Game page : localhost:8000/game/
# This view displays the game page of the application
# It displays the game page with the user's profile picture, username, and a game
# If the user is not authenticated, it redirects to the index page

@login_required
def game(request):
    if request.method == 'POST':
        request.user.total_matches += 1
        request.user.in_game = True
        request.user.save()

        game = Game.objects.create(local=True, tournament=False, ended=False, player_uid_id=request.user.id)
        game.save()
        return JsonResponse({'success': True})
    return render(request, 'game.html')

@login_required
def tournament_match(request):
    if request.method == 'POST':
        data_player = json.loads(request.body)
        player1 = data_player.get('player1')
        player2 = data_player.get('player2')
        match_id = data_player.get('match_id')
        tournament_id = data_player.get('tournament_id')
        data = {
            'player1': player1,
            'player2': player2,
            'match_id': match_id,
            'tournament_id': tournament_id
        }
        request.session['data'] = data
        return JsonResponse({'success': True})
    else:
        tournaments_overview = Tournament.objects.filter(owner_uid_id=request.user.id).last()
        match = Tournament_Match.objects.filter(tournament_id=tournaments_overview.id, winner='...').first()
        data =  {
            'player1': match.player1,
            'player2': match.player2,
            'match_id': match.match_id,
            'tournament_id': match.tournament_id
        }
    return render(request, 'tournament_match.html', {'tournament_match': data})

# View Game page : localhost:8000/game/ia
# This view displays the game page of the application
# It displays the game page with the user's profile picture, username, and a game
# If the user is not authenticated, it redirects to the index page

@login_required
def gameia(request):
    if request.method == 'POST':
        request.user.total_matches += 1
        request.user.in_game = True
        request.user.save()
        level = json.load(request)['level']
        request.session['level'] = level 
                
        game = Game.objects.create(local=True, tournament=False, ended=False, player_uid_id=request.user.id)
        game.save()
        return JsonResponse({'success': True})
    else:
        level = request.session.get('level', None)
    return render(request, 'ia.html', {'level': level})


############################################################################################################
# API endpoints
# Each endpoint is a function that takes a request as an argument and returns a JSON response
# The JSON response can contain data that is sent to the client
############################################################################################################

# API endpoint to update the user's score
# This endpoint is called when the game ends
# It increments the user's win count by 1

@login_required
def update_score(request):
    if request.method == 'POST':
        user = request.user
        user.win += 1
        user.in_game = False
        user.save()

        data = json.load(request)

        winner_uid = data['winner_uid']
        score_player1 = 5
        score_player2 = data['score']
        time = data['time']
        game = Game.objects.last()
        if game is not None:
            game.ended = True
            game.winner_uid_id = winner_uid
            game.score_player1 = score_player1
            game.score_player2 = score_player2
            game.time = time
            game.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

# API endpoint to update the user's loss count
# This endpoint is called when the game ends
# It increments the user's loss count by 1

@login_required
def update_loss(request):
    if request.method == 'POST':
        user = request.user
        user.lose += 1
        user.in_game = False
        user.save()

        game = Game.objects.last()
        data = json.load(request)
        score_player1 = data['score']
        time = data['time']
        score_player2 = 5
        if game is not None:
            game.ended = True
            game.score_player1 = score_player1
            game.score_player2 = score_player2
            game.time = time
            game.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

@login_required
def update_tournament_match(request):
    if request.method == 'POST':
        data = json.load(request)
        match_id = data['match_id']
        winner = data['winner']
        Tournament_up = Tournament.objects.filter(owner_uid_id=request.user.id).last()
        tournament_id = Tournament_up.id
        match = Tournament_Match.objects.get(match_id=match_id, tournament_id=tournament_id)
        match.winner = winner
        match.save()

        next_round = match.round_id + 1
        next_matchs = Tournament_Match.objects.filter(tournament_id=match.tournament_id, round_id=next_round)
        for next_match in next_matchs:
            if next_matchs:
                if next_match.player1 == "_":
                    next_match.player1 = winner
                    next_match.save()
                    break
                elif next_match.player2 == "_":
                    next_match.player2 = winner
                    next_match.save()
                    break

        # Check if the tournament is over
        tournament = Tournament.objects.get(id=tournament_id)
        matchs = Tournament_Match.objects.filter(tournament_id=tournament_id)
        matchs = matchs.filter(winner="...")
        if not matchs:
            tournament.winner_name = winner
            tournament.state = True
            tournament.save()

        return JsonResponse({'success': True})
    else:
        tournaments_overview = Tournament.objects.filter(owner_uid_id=request.user.id).last()
        match = Tournament_Match.objects.filter(tournament_id=tournaments_overview.id, winner='...').first()
        if not match:
            return JsonResponse({'success': False})
        data =  {
            'player1': match.player1,
            'player2': match.player2,
            'match_id': match.match_id,
        }
    return JsonResponse({'tournament_match': data})
# Handler for 404 errors
# This handler is called when a page is not found
# It renders the 404.html template

def handler404(request, exception):
    return render(request, 'base/404.html', status=404)

# Handler for 500 errors
# This handler is called when an internal server error occurs
# It renders the 500.html template

def handler500(request):
    return render(request, 'base/500.html', status=500)

# API endpoint to search for friends
# This endpoint is called when the user searches for friends
# It returns a list of users that match the search query

def search_friends(request):
    if request.method == 'POST':
        search = json.load(request)['search']
        userList = User.objects.filter(username__icontains=search)
        friends = Friend.objects.filter(user1_uid_id=request.user.id)
        userData = []
        for user in userList:
            userData.append({
                'username': user.username,
                'profile_image': request.build_absolute_uri(user.profile_image.url),
                'id': user.id,
                'is_friend': friends.filter(user2_uid_id=user.id).exists(),
                'is_self': user.id == request.user.id
            })

        return JsonResponse({'users': list(userData)})


# API endpoint to add friends
# This endpoint is called when the user sends a friend request
# It creates a new friend request in the database

def add_friends(request):
    if request.method == 'POST':
        id = json.load(request)['id']
        from_to = request.user.id
        to_id = id
        friend_request, created = Friend.objects.get_or_create(user1_uid_id=from_to, user2_uid_id=to_id)
        firend_request, created = Friend.objects.get_or_create(user1_uid_id=to_id, user2_uid_id=from_to)
        if created:
            return JsonResponse({'friend_request': True})
        else:
            return JsonResponse({'friend_request': False})
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


# API endpoint to create a tournament
# This endpoint is called when the user creates a tournament
# It creates a new tournament in the database

def create_tournament(request):
    if request.method == 'POST':
        playerList = json.load(request)['players']

        if Tournament.objects.filter(owner_uid_id=request.user.id).filter(state=False).exists():
            return JsonResponse({'success': False, 'message': 'Vous avez déjà créé un tournoi'})

        rounds = calculate_rounds(len(playerList))
        time = timezone.now()
        tournament = Tournament.objects.create(owner_uid_id=request.user.id, username_virtual_player=playerList, created_at=time, state=False, number_of_players=len(playerList), number_of_matchs=len(playerList) - 1, number_of_rounds=rounds)
        tournament.save()
        
        create_tournament_matchs(tournament)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Une erreur s’est produite'})

# API endpoint to log out the user
# This endpoint is called when the user logs out
# It logs out the user and redirects to the index page

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

# Utils for create_tournament
# This function define the number of rounds in function of the number of players

def calculate_rounds(num_players):
    if num_players == 2:
        return (1)
    elif num_players <= 4:
        return (2)
    elif num_players <= 8:
        return (3)
    elif num_players <= 16:
        return (4)
    else:
        return (0)

# Utils for create_tournament
# This function create every matchs of the tournament

def create_tournament_matchs(tournament):

    player = 0
    matchId = 1
    for i in range(tournament.number_of_rounds):

        j = 1
        while j*2 < tournament.number_of_players:
            j*= 2
        matchs_in_rounds = tournament.number_of_players - j
        for k in range(matchs_in_rounds):
            p1 = define_player(tournament.username_virtual_player, player)
            p2 = define_player(tournament.username_virtual_player, player + 1)
            match = Tournament_Match.objects.create(tournament_id=tournament, match_id=matchId, round_id=i + 1, player1=p1, player2=p2, winner="...")
            match.save()
            matchId+=1
            player+=2
        tournament.number_of_players -= matchs_in_rounds
    return


def define_player(PlayerList, num):
    if num < len(PlayerList):
        return PlayerList[num]
    else:
        return "_"