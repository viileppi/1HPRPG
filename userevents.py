# -*- coding: UTF-8 -*-     
import pygame

def player_shot_event():
    return pygame.event.Event(pygame.USEREVENT + 1)

def player_blast_event():
    return pygame.event.Event(pygame.USEREVENT + 2)

def death_event():
    return pygame.event.Event(pygame.USEREVENT + 3)

def enemy_shot_event():
    return pygame.event.Event(pygame.USEREVENT + 4)
