from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name or "No name"

class Baralho(models.Model):
    id = models.AutoField(primary_key=True)  # ID único para o deck
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Relacionamento com Customer
    title = models.CharField(max_length=200, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Card(models.Model):
    id = models.AutoField(primary_key=True)  # ID único para o card
    baralho = models.ForeignKey(Baralho, on_delete=models.CASCADE, related_name='cards')  # Relacionamento com Deck
    frente = models.CharField(max_length=200, null=False)  # Frente do card (título)
    resposta = models.TextField(null=False)  # Resposta/explicação
    ESCOLHAS_DE_DIFICULDADE = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
        ('impossivel', 'Impossível')
    ]
    dificuldade = models.CharField(max_length=20, choices=ESCOLHAS_DE_DIFICULDADE, default='facil')  # Nível de dificuldade
    
    def __str__(self):
        return f"{self.front} - {self.difficulty}"
