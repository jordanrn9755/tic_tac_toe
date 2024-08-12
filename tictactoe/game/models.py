from django.db import models
import json



# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    opponent = models.CharField(max_length=100, default="AI")
    board = models.JSONField(default=list)
    result = models.CharField(max_length=10, choices=[('win', 'Win'), ('loss', 'Loss'), ('draw', 'Draw')], null=True, blank=True)

    def __str__(self):
        return f"{self.player} vs {self.opponent}"