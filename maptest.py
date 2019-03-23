# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from os import listdir
from os import path

import pytmx
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame
import logging
from objects import Object
from actiontile import ActionTile
from player import Player
from enemy import Enemy

logger = logging.getLogger(__name__)
logger.info(pytmx.__version__)

class TiledRenderer(object):
    """
    Super simple way to render a tiled map
    """

    def __init__(self, screen, filename):
        tm = load_pygame(filename)

        # self.size will be the pixel size of the map
        # this value is used later to render the entire map to a pygame surface
        self.screen = screen
        self.pixel_size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.character_scale = 0.75
        self.tmx_data = tm
        self.spritelist = pygame.sprite.Group()
        self.walllist = []
        self.player = None
        self.enemygroup = pygame.sprite.Group()
        self.mygroup = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.finish = None

    def move_player(self, where):
        for player in self.mygroup:
            player.move(where)

    def render_map(self, surface):
        """ Render our map to a pygame surface

        Feel free to use this as a starting point for your pygame app.
        This method expects that the surface passed is the same pixel
        size as the map.

        Scrolling is a often requested feature, but pytmx is a map
        loader, not a renderer!  If you'd like to have a scrolling map
        renderer, please see my pyscroll project.
        """

        # fill the background color of our render surface
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        # iterate over all the visible layers, then draw them
        for layer in self.tmx_data.visible_layers:
            # each layer can be handled differently by checking their type
            if isinstance(layer, TiledTileLayer):
                self.render_tile_layer(surface, layer)
            elif isinstance(layer, TiledObjectGroup):
                self.render_object_layer(surface, layer)
            elif isinstance(layer, TiledImageLayer):
                self.render_image_layer(surface, layer)

    def render_tile_layer(self, surface, layer):
        """ Render all TiledTiles in this layer
        """
        # deref these heavily used references for speed
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit

        # iterate over the tiles in the layer, and blit them
        for x, y, image in layer.tiles():
            # surface_blit(image, (x * tw, y * th))
            if (layer.name== "nopass"):
                self.spritelist.add(Object(self.screen, path.join("levels", "blue.png"), (x * tw, y * th), 1))

    def render_object_layer(self, surface, layer):
        """ Render all TiledObjects contained in this layer
        """
        # deref these heavily used references for speed
        draw_rect = pygame.draw.rect
        draw_lines = pygame.draw.lines
        surface_blit = surface.blit

        # these colors are used to draw vector shapes,
        # like polygon and box shapes
        rect_color = (255, 0, 0)
        poly_color = (0, 255, 0)

        # iterate over all the objects in the layer
        # These may be Tiled shapes like circles or polygons, GID objects, or Tiled Objects
        for obj in layer:
            logger.info(obj)

            # objects with points are polygons or lines
            if hasattr(obj, 'points'):
                draw_lines(surface, poly_color, obj.closed, obj.points, 3)

            # some objects have an image
            # Tiled calls them "GID Objects"
            elif obj.image:
                surface_blit(obj.image, (obj.x, obj.y))
                # s = pygame.sprite.Sprite()
            elif (obj.name == "Enemy"):
                e = Enemy(self.screen, path.join("images", "enemy.png"), (obj.x, obj.y), self.character_scale)
                self.enemygroup.add(e)

            elif (obj.name == "Player"):
                self.mygroup.empty()
                self.player = Player(self.screen, path.join("images", "player.png"), (obj.x, obj.y + 33), self.character_scale)
                self.mygroup.add(self.player)

            elif (obj.name == "Finish"):
                self.finish = ActionTile(self.screen, path.join("levels", "green.png"), (obj.x, obj.y), 1)
                self.finish.image = pygame.transform.scale(self.finish.image, (int(obj.width), int(obj.height)))
                self.finish.rect = Rect(obj.x, obj.y, self.finish.image.get_width(), self.finish.image.get_height())
                self.waypoints.add(self.finish)

            # draw a rect for everything else
            # Mostly, I am lazy, but you could check if it is circle/oval
            # and use pygame to draw an oval here...I just do a rect.
            else:
                draw_rect(surface, rect_color,
                          (obj.x, obj.y, obj.width, obj.height), 3)


    def render_image_layer(self, surface, layer):
        if layer.image:
            surface.blit(layer.image, (0, 0))


