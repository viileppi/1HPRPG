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
from wall import Finish
from menu import Menu
import random

class LevelRenderer(object):
    """
    Super simple way to render a tiled map
    """

    def __init__(self, screen, xy, player_pos):

        # self.size will be the pixel size of the map
        # this value is used later to render the entire map to a pygame surface
        self.screen = screen.gamearea
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.fifth = int(self.width/5)
        self.third = int(self.height/3)
        self.offset = 16
        self.keypoints = []
        for y in range(2,3):
            for x in range(2,5):
                self.keypoints.append((int(self.fifth*x), int(self.third*y)))
        self.character_scale = 1
        self.wall_list = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.mygroup = pygame.sprite.Group()
        self.enemyammo = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.mygroup.empty()
        self.player = Player(self.screen, path.join("images", "player.png"), player_pos, self.character_scale, self.wall_list)
        self.mygroup.add(self.player)
        self.xy = xy
        self.spawn_points = [
                            (self.width/6, self.height/6),
                            (self.width/2, self.height/2)
                            ]
        self.finish = None
        self.borders = [
                            # top row
                            [
                                (0,0), 
                                (self.fifth*2,0)
                            ], 
                            [
                                (self.fifth*3,0), 
                                (self.width,0)
                            ], 
                            # bottom row
                            [
                                (0,self.height - self.offset), 
                                (self.fifth*2, self.height - self.offset)
                            ],
                            [
                                (self.fifth*3,self.height-self.offset), 
                                (self.width,self.height-self.offset)
                            ], 
                            # left column
                            [
                                (0,0), 
                                (0,self.third)
                            ], 
                            [
                                (0,self.third*2), 
                                (0,self.height)
                            ], 
                            # right column
                            [
                                (self.width - self.offset,0), 
                                (self.width - self.offset,self.third), 
                            ], 
                            [
                                (self.width - self.offset,self.third*2), 
                                (self.width - self.offset,self.height), 
                            ] 
                        ]

        self.render_tile_layer(self.screen)
        self.generate_maze(self.screen)
        self.render_object_layer(self.screen)
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
        # manually add exits
        w = Finish(self.screen, (self.fifth*2, 0), (self.fifth*3, 0))
        self.waypoints.add(w)
        w = Finish(self.screen, (self.fifth*2, self.height - self.offset), (self.fifth*3, self.height - self.offset))
        self.waypoints.add(w)
        w = Finish(self.screen, (0, self.third), (0, self.third*2))
        self.waypoints.add(w)
        w = Finish(self.screen, (self.width - self.offset, self.third), (self.width - self.offset, self.third*2))
        self.waypoints.add(w)
        self.wall_list.draw(surface)
        self.waypoints.draw(surface)
        self.player.wall_list = self.wall_list

    def generate_maze(self, surface):
        i = 0
        end = (0,0)
        xy = (self.xy[1]<<8)|self.xy[0]
        for i in range(2):
            xy = xy*7
            xy += 12627
        print(xy)
        for item in self.keypoints:
            # north
            if (xy>>i)&3 == 0:
                end = (item[0],item[1] - self.third)
            # south
            if (xy>>i)&3 == 1:
                end = (item[0],item[1] + self.third)
            # east
            if (xy>>i)&3 == 2:
                end = (item[0] - self.fifth,item[1])
            # west
            if (xy>>i)&3 == 3:
                end = (item[0] + self.fifth,item[1])
            w = Wall(self.screen, item, end)
            i += 2
            self.wall_list.add(w)
        self.wall_list.draw(surface)

    def render_object_layer(self, surface):

        for coord in self.spawn_points:
            e = Enemy(self.screen, path.join("images", "enemy.png"), coord, self.character_scale, self.player, self.wall_list, self.enemyammo)
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
        for death in amm_enem:
            M = Menu(self.screen)
            M.menuitems = {"continue": 0,
                            "quit": 1
                            }
            mr = M.menuloop()
            if (mr == 0):
                next_level = True
            if (mr == 1):
                pygame.quit()
        return next_level


