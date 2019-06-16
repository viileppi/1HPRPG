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

def player_died():
    return pygame.event.Event(pygame.USEREVENT + 5)

def player_ran():
    return pygame.event.Event(pygame.USEREVENT + 6)

def player_blast():
    return pygame.event.Event(pygame.USEREVENT + 7)

def player_gun():
    return pygame.event.Event(pygame.USEREVENT + 8)

def music_stop():
    return pygame.event.Event(pygame.USEREVENT + 9)



