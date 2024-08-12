from django.shortcuts import render, redirect
from .models import Player, Game
import random

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        player, created = Player.objects.get_or_create(name=name, email=email)
        request.session['player_id'] = player.id
        return redirect('game')
    return render(request, 'index.html')

def game(request):
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('index')
    
    player = Player.objects.get(id=player_id)
    
    # Start a new game if requested
    if request.method == 'POST' and 'new_game' in request.POST:
        Game.objects.filter(player=player, result__isnull=True).delete()
        game = Game.objects.create(player=player, board=[['' for _ in range(3)] for _ in range(3)])
    else:
        game, created = Game.objects.get_or_create(player=player, result__isnull=True, defaults={'board': [['' for _ in range(3)] for _ in range(3)]})
    
    if request.method == 'POST' and 'x' in request.POST and 'y' in request.POST:
        x, y = int(request.POST.get('x')), int(request.POST.get('y'))
        board = game.board
        if board[x][y] == '':
            board[x][y] = 'X'
            if check_winner(board, 'X'):
                game.result = 'win'
                player.wins += 1
                game.save()
                player.save()
                return render(request, 'game.html', {'game': game, 'board': board, 'message': 'You win!'})
            
            if not any('' in row for row in board):
                game.result = 'draw'
                player.draws += 1
                game.save()
                player.save()
                return render(request, 'game.html', {'game': game, 'board': board, 'message': 'Draw!'})
            
            ai_move(board)
            if check_winner(board, 'O'):
                game.result = 'loss'
                player.losses += 1
                game.save()
                player.save()
                return render(request, 'game.html', {'game': game, 'board': board, 'message': 'You lose!'})
            
            game.board = board
            game.save()
    
    board_data = [[cell for cell in row] for row in game.board]
    return render(request, 'game.html', {'game': game, 'board': board_data})

def ai_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if empty_cells:
        x, y = random.choice(empty_cells)
        board[x][y] = 'O'

def check_winner(board, player):
    lines = [board[i] for i in range(3)] + \
            [[board[i][j] for i in range(3)] for j in range(3)] + \
            [[board[i][i] for i in range(3)]] + \
            [[board[i][2 - i] for i in range(3)]]
    return any(all(cell == player for cell in line) for line in lines)

def leaderboard(request):
    # Retrieve top 10 players by number of wins
    top_players = Player.objects.order_by('-wins')[:10]
    return render(request, 'leaderboard.html', {'players': top_players})