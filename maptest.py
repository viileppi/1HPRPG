# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from os import listdir
from os import path
from vision import Screen
from colliders import *
from objects import Object
from actiontile import ActionTile
from player import Player
from enemy import Enemy
from wall import Wall


class LevelRenderer(object):
    """
    Super simple way to render a tiled map
    """

    def __init__(self, screen):

        # self.size will be the pixel size of the map
        # this value is used later to render the entire map to a pygame surface
        self.screen = screen.screen
        self.gamearea = screen.gamearea
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.character_scale = 1
        self.wall_list = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.mygroup = pygame.sprite.Group()
        self.enemyammo = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.mygroup.empty()
        self.player = Player(self.screen, path.join("images", "player.png"), (400, 300), self.character_scale, self.wall_list)
        self.mygroup.add(self.player)

        self.finish = None
        self.borders = [
                            # top row
                            [
                                (self.gamearea[0],self.gamearea[1]), 
                                (self.gamearea[2],self.gamearea[1])
                            ], 
                            # bottom row
                            [
                                (self.gamearea[0],self.gamearea[3]), 
                                (self.gamearea[2],self.gamearea[3])
                            ],
                            # left row
                            [
                                (self.gamearea[0],self.gamearea[1]), 
                                (self.gamearea[0],self.gamearea[3])
                            ], 
                            # right row
                            [
                                (self.gamearea[2],self.gamearea[1]), 
                                (self.gamearea[2],self.gamearea[3]), 
                            ] 
                        ]

        self.render_tile_layer(self.screen)
    def move_player(self, where):
        for player in self.mygroup:
            player.move(where)

    def render_map(self, surface):
        # fill the background color of our render surface
        surface.fill(pygame.Color("black"))

    def render_tile_layer(self, surface):
        surface_blit = surface.blit
        for line in self.borders:
            w = Wall(self.screen, line[0], line[1])
            self.wall_list.add(w)
        self.wall_list.draw(surface)
        self.player.wall_list = self.wall_list

    def render_object_layer(self, surface, layer):


        self.render_tile_layer(self.screen)
        e = Enemy(self.screen, path.join("images", "enemy.png"), (128, 128), self.character_scale, self.player, self.wall_list, self.enemyammo)
        self.enemygroup.add(e)

        self.mygroup.update()


    def render_image_layer(self, surface, layer):
        surface.blit(layer.image, (0, 0))

    def update_level(self):
        next_level = False
        self.enemygroup.update()
        self.wall_list.draw(self.screen)
        self.wall_list.update()
        self.mygroup.update()
        self.waypoints.draw(self.screen)
        self.player.ammogroup.update()
        self.player.ammogroup.draw(self.screen)
        self.enemyammo.update()
        self.enemyammo.draw(self.screen)
        chr_coll = pygame.sprite.groupcollide(self.mygroup, self.enemygroup, True, True, colli_kill_both)
        amm_coll = pygame.sprite.groupcollide(self.enemygroup, self.player.ammogroup, False, False, colli_kill_l)
        amm_enem = pygame.sprite.groupcollide(self.mygroup, self.enemyammo, False, False, colli_kill_l)
        amm_wall = pygame.sprite.groupcollide(self.player.ammogroup, self.wall_list, False, False, colli_kill_l)
        ea_wall = pygame.sprite.groupcollide(self.enemyammo, self.wall_list, False, False, colli_kill_l)
        enm_wall = pygame.sprite.groupcollide(self.enemygroup, self.wall_list, False, False, colli_bounce)
        enm_wal2 = pygame.sprite.groupcollide(self.enemygroup, self.waypoints, False, False, colli_bounce)
        pla_fin = pygame.sprite.groupcollide(self.mygroup, self.waypoints, False, False, colli_basic)
        #pla_wall = pygame.sprite.groupcollide(self.mygroup, self.wall_list, False, False, colli_bounce)
        for c in chr_coll:
            c.destroy()
            del c
            level.index = 0
            self = level.next()
            self.render_map(scr.bg)
            pygame.display.flip()
        for u in pla_fin:
            next_level = True
        return next_level


