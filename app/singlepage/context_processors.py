def tournament_match(request):
    data = request.session.get('data', None)
    return {'tournament_match': data}
