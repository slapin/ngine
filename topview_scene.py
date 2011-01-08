# -*- coding: utf-8 -*-

#================================================
#
# Dummy Scene for the Top-View Example (please execute topview_example.py)
#
# Copyright (C) 2010  Wil Alvarez <wil.alejandro@gmail.com>
#
#===================================================

import pygame
import random

from ngine import scene
from ngine import collisions
from ngine import particles

from dummy_keys import *
from topview_objects import *

class DummyScene(scene.Scene):
    def __init__(self, director, _input, gamedata):
        scene.Scene.__init__(self, director, _input, gamedata)
        
    def __load_map(self, filename):
        self.maploader.load(filename)
        
        for row in self.maploader.layers['unwalkable']:
            for block in row:
                tb, bb, lb, rb = self.maploader.get_collide_bounds(block.x, block.y)
                if block.t_id == '01':
                    Block((block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '65':
                    Tree(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '09':
                    WaterWell(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '66':
                    Gravestone(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id == '67':
                    CrossGravestone(self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                elif block.t_id in ['17', '18', '19', '33', '34', '35', '25']:
                    Fence(block.t_id, self.res, (block.real_x, block.real_y), tb, bb, lb, rb)
                
        for row in self.maploader.layers['characters']:
            for char in row:
                if char.t_id == '01':
                    self.box = ArchMage(self.res, (char.real_x, char.real_y), self.gblocks)
                elif char.t_id == '02':
                    DeadBox((char.real_x, char.real_y))
        
        for row in self.maploader.layers['items']:
            for item in row:
                if item.t_id == '01':
                    ItemBox((item.real_x, item.real_y))
        
    def on_load(self):
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.gblocks = pygame.sprite.Group()
        self.all = pygame.sprite.Group()
        
        ArchMage.containers = self.all, self.layer1
        DeadBox.containers = self.all, self.layer2
        ItemBox.containers = self.all, self.layer2
        particles.Particle.containers = self.all, self.layer2
        Block.containers = self.all, self.layer2, self.gblocks
        Tree.containers = self.all, self.layer2, self.gblocks
        WaterWell.containers = self.all, self.layer2, self.gblocks
        Gravestone.containers = self.all, self.layer2, self.gblocks
        CrossGravestone.containers = self.all, self.layer2, self.gblocks
        Fence.containers = self.all, self.layer2, self.gblocks
        
        self.res.font.load_default('__default__', 16, (255,255,255))
        self.res.image.load(['archmage.png'])
        self.res.image.load(['map.bmp'])
        
        self.__load_map('02.map')
        
        self.effect = 0
        self.on_loaded_map()
        self.append_to_draw(self.layer2)
        self.append_to_draw(self.layer1)
        self.set_camera_target(self.box)
        self.set_backgrounds(bg2=self.maploader.layers['background'])
        
    def handle_events(self):
        self._input.handle_input()
        
        if self._input.lookup(LEFT): 
            self.box.move(-1, 0)
        elif self._input.lookup(RIGHT): 
            self.box.move(1, 0)
        elif self._input.lookup(UP): 
            self.box.move(0, -1)
        elif self._input.lookup(DOWN): 
            self.box.move(0, 1)
        if self._input.lookup(BUTTON1):
            if pygame.mouse.get_pos()[0] > 640/2: 
                dir = 270
            else: 
                dir = 90
            if self.effect == 0:
                particles.ParticlesExplosion(pygame.mouse.get_pos(), 2)
            elif self.effect == 1:
                particles.ParticlesFirework(pygame.mouse.get_pos(), 2)
            elif self.effect == 2:
                particles.ParticlesShock(pygame.mouse.get_pos(), 1, dir, (0,255,0))
        if self._input.lookup(BUTTON3): 
            self.effect += 1
            if self.effect > 4:
                self.effect = 0
        if self._input.lookup(EXIT): 
            return True
        
        return False
    
    def check_collisions(self):
        return
                
    def on_update(self):
        self.all.update()
        
    def on_draw(self):
        if self.effect == 3:
            ang = random.randint(-25, 25)
            particles.Particle(pos=pygame.mouse.get_pos(), angle=ang, 
                               size=1.8, color_type='random', duration=1500, 
                               vx=0.5, vy=1, ax=0, ay=0)
        elif self.effect == 4:
            particles.ParticlesBoost(pygame.mouse.get_pos(), 180, 2, 
                                     particles=50)
        self.__text_on_screen()
    
    def __text_on_screen(self):
        fps = str(int(self.director.clock.get_fps ()))
        obj_count = str(len(self.all))
        info1 = self.res.font.render('__default__', 'FPS: ' + fps)
        info2 = self.res.font.render('__default__', 'Objects: ' + obj_count)
        self.screen.blit(info1, (10, 10))
        self.screen.blit(info2, (10, 20))
        
        if self.effect == 0: 
            text = self.res.font.render('__default__', 'Effect: Explosion')
        elif self.effect == 1: 
            text = self.res.font.render('__default__', 'Effect: Fireworks')
        elif self.effect == 2: 
            text = self.res.font.render('__default__', 'Effect: Shock')
        elif self.effect == 3: 
            text = self.res.font.render('__default__', 'Effect: Trace')
        elif self.effect == 4: 
            text = self.res.font.render('__default__', 'Effect: Boost')
        inst = self.res.font.render('__default__', 'Click on the screen to see the effect. Right click to change it')
        self.screen.blit(inst, (150,440))
        self.screen.blit(text, (250,460))
