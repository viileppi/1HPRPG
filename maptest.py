# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from os import path
from colliders import *
from player import Player
from enemy import Enemy
from enemy import Roomba
from wall import Wall
from wall import Finish
import random
import item
from item import Item

class LevelRenderer(object):
    """
    Super simple way to render a tiled map
    """

    def __init__(self, screen, xy, player_pos, difficulty):

        # self.size will be the pixel size of the map
        # this value is used later to render the entire map to a pygame surface
        self.difficulty = difficulty
        print("difficulty: " + str(self.difficulty))
        self.pew_playing = 0
        self.robot_image = path.join("images", "robot.png") 
        self.screen = screen.gamearea
        self.menuscreen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.fifth = int(self.width/5)
        self.third = int(self.height/3)
        self.offset = 16
        self.keypoints = []
        for y in range(1,3):
            for x in range(1,5):
                self.keypoints.append((int(self.fifth*x), int(self.third*y)))
        self.wallgroup = pygame.sprite.Group()
        self.itemgroup = pygame.sprite.Group()
        self.enemy_walls = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.snakegroup = pygame.sprite.Group()
        self.mygroup = pygame.sprite.Group()
        self.enemyammo = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.corpsegroup = pygame.sprite.Group()
        self.mygroup.empty()
        self.player = Player(self, path.join("images", "player_noblur.png"), player_pos)
        self.player_items = {"speed": self.player.speed, "blast_radius": self.player.blast_radius, "shots_n": self.player.ammo_spawner.shots_n }
        self.mygroup.add(self.player)
        self.gave_item = False
        self.xy = xy
        self.spawn_points = []
        for item in self.keypoints:
            self.spawn_points.append((item[0] + 64, item[1] + 64))
            self.spawn_points.append((item[0] - 64, item[1] - 64))
        self.gived_items = False
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
        self.player.wallgroup = self.wallgroup
        self.player.updateWallgroup()
        #self.render_object_layer(self.screen)

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
            self.wallgroup.add(w)
            self.enemy_walls.add(w)
        # manually add exits
        w = Finish(self.screen, (self.fifth*2, 0), (self.fifth*3, 0))
        if (w.too_close(self.player)):
            w = Wall(self.screen, w.start, w.end)
            self.wallgroup.add(w)
        else:
            self.waypoints.add(w)
        self.enemy_walls.add(w)
        w = Finish(self.screen, (self.fifth*2, self.height - self.offset), (self.fifth*3, self.height - self.offset))
        if (w.too_close(self.player)):
            w = Wall(self.screen, w.start, w.end)
            self.wallgroup.add(w)
        else:
            self.waypoints.add(w)
        self.enemy_walls.add(w)
        w = Finish(self.screen, (0, self.third), (0, self.third*2))
        if (w.too_close(self.player)):
            w = Wall(self.screen, w.start, w.end)
            self.wallgroup.add(w)
        else:
            self.waypoints.add(w)
        self.enemy_walls.add(w)
        w = Finish(self.screen, (self.width - self.offset, self.third), (self.width - self.offset, self.third*2))
        if (w.too_close(self.player)):
            w = Wall(self.screen, w.start, w.end)
            self.wallgroup.add(w)
        else:
            self.waypoints.add(w)
        self.enemy_walls.add(w)
        self.wallgroup.draw(surface)
        self.waypoints.draw(surface)

    def generate_maze(self, surface):
        self.itemgroup.empty()
        i = 0
        end = (0,0)
        xy = (self.xy[1]<<8)|self.xy[0]
        for i in range(2):
            xy = xy*7
            xy += 12627
        for item in self.keypoints:
            post = (xy>>i)&3
            # north
            if post == 0:
                end = (item[0],item[1] - self.third)
            # south
            if post == 1:
                end = (item[0],item[1] + self.third)
            # east
            if post == 2:
                end = (item[0] - self.fifth,item[1])
            # west
            if post == 3:
                end = (item[0] + self.fifth,item[1])
            w = Wall(self.screen, item, end)
            i += 2
            self.wallgroup.add(w)
            self.enemy_walls.add(w)
        self.wallgroup.draw(surface)
        i = 0
        enemies = int(3 + self.difficulty)
        mask = xy&3
        for coord in self.spawn_points:
            point = (xy>>i)&3
            if (point == mask):
                ### ROOMBA TEST ### 
                e = Enemy(self, self.robot_image, coord, self.difficulty)
                ### e = Roomba(self, self.robot_image, coord, self.difficulty)
                if (e.playerCheck(200)) or (enemies < 0):
                    e.kill()
                    del e
                else:
                    self.enemygroup.add(e)
                    self.mygroup.update()
                    enemies -= 1
            i += 2


    def render_object_layer(self, surface):
        enemies_n = random.randint(1, self.difficulty)
        for coord in self.spawn_points:
            if (random.randint(0,10) == enemies_n):
                e = Enemy(self.screen, path.join("images", "robot.png"), coord, self.player, self.wallgroup, self.enemyammo, self.difficulty)
                if e.playerCheck(100):
                    e.kill()
                    del e
                else:
                    self.enemygroup.add(e)
                    self.mygroup.update()
                    enemies_n -= 1
            #elif (random.randint(1,4) == enemies_n):
            #    e = Snake(self.screen, path.join("images", "snake.png"), coord, self.player, self.wallgroup, self.enemyammo)
            #    if e.playerCheck(100):
            #        e.kill()
            #        del e
            #    else:
            #        self.snakegroup.add(e)
            #        self.enemygroup.add(e)
            #        self.mygroup.update()
            #        enemies_n -= 1


    def render_image_layer(self, surface, layer):
        surface.blit(layer.image, (0, 0))

    def update_level(self):
        shots_fired = len(self.enemyammo.sprites())
        player_fired = len(self.player.ammogroup.sprites())
        next_level = False
        self.enemygroup.update()
        self.wallgroup.update()
        self.corpsegroup.update()
        self.mygroup.update()
        self.player.ammogroup.update()
        self.player.blastgroup.update()
        self.player.bombgroup.update()
        self.enemyammo.update()
        self.itemgroup.update()
        self.itemgroup.draw(self.screen)
        self.wallgroup.draw(self.screen)
        self.waypoints.draw(self.screen)
        self.player.ammogroup.draw(self.screen)
        #self.player.blastgroup.draw(self.screen)
        self.enemyammo.draw(self.screen)
        chr_coll = pygame.sprite.groupcollide(self.mygroup, self.enemygroup, True, True, colli_kill_both)
        #amm_coll = pygame.sprite.groupcollide(self.enemygroup, self.player.ammogroup, True, True, colli_kill_both)
        amm_coll = pygame.sprite.groupcollide(self.enemygroup, self.player.ammogroup, True, True, colli_kill_both)
        amm_enem = pygame.sprite.groupcollide(self.mygroup, self.enemyammo, True, True, colli_kill_both)
        amm_wall = pygame.sprite.groupcollide(self.player.ammogroup, self.wallgroup, False, False, colli_kill_l)
        ea_wall = pygame.sprite.groupcollide(self.enemyammo, self.wallgroup, False, False, colli_kill_l)
        #enm_wall = pygame.sprite.groupcollide(self.enemygroup, self.wallgroup, False, False, colli_bounce)
        #enm_wal2 = pygame.sprite.groupcollide(self.enemygroup, self.waypoints, False, False, colli_bounce)
        pla_fin = pygame.sprite.groupcollide(self.mygroup, self.waypoints, False, False, colli_basic)
        amm_amm = pygame.sprite.groupcollide(self.enemyammo, self.player.ammogroup, True, True)
        blast_amm = pygame.sprite.groupcollide(self.enemyammo, self.player.blastgroup, False, False, colli_kill_l)
        bomb_amm = pygame.sprite.groupcollide(self.enemyammo, self.player.bombgroup, False, False, colli_kill_l)
        blast_enm = pygame.sprite.groupcollide(self.enemygroup, self.player.blastgroup, False, False, colli_kill_l)
        bomb_enm = pygame.sprite.groupcollide(self.enemygroup, self.player.bombgroup, False, False, colli_kill_l)
        blast_wall = pygame.sprite.groupcollide(self.player.blastgroup, self.wallgroup, False, False, colli_clip)
        bomb_wall = pygame.sprite.groupcollide(self.player.bombgroup, self.wallgroup, False, False, colli_clip)
        pla_item = pygame.sprite.groupcollide(self.itemgroup, self.mygroup, False, False, colli_kill_l)
        enmenm = pygame.sprite.groupcollide(self.enemygroup, self.enemygroup, False, False, colli_bounce)
        #snake_wall = pygame.sprite.groupcollide(self.snakegroup, self.wallgroup, False, False, colli_kill_l)
        #pla_wall = pygame.sprite.groupcollide(self.mygroup, self.wallgroup, False, False, colli_bounce)
        #for c in chr_coll:
        #    c.destroy()
        #    del c
        #    ##  self.render_map(scr.bg)
        #    pygame.display.flip()
        if (len(self.enemygroup.sprites()) <= 0) and (not self.gived_items):
            self.gived_items = True
            for point in self.spawn_points:
                if (random.randint(0,4)>2):
                    i = Item(self, point)
                    self.itemgroup.add(i)
        for item in pla_item:
            self.player_items = item.levelUp(self.player)
        for u in pla_fin:
            next_level = True
            self.player_items = {"speed": self.player.speed, "blast_radius": self.player.blast_radius, "shots_n": self.player.ammo_spawner.shots_n, "blasts_n": self.player.blast_spawner.shots_n }
        return next_level


