from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader
import random
import sys
from numpy import floor
from random import randrange

app = Ursina()
player = FirstPersonController()

blocks = [
    'hello',
    load_texture("assets/grassblock.png"),
    load_texture("assets/dirtblock.png"),
    load_texture("assets/stone.png"),
    load_texture("assets/cobbler.png"),
    load_texture("assets/sand.png"),
    load_texture("assets/log.png"),
    load_texture("assets/planks.png"),
    load_texture("assets/obsidian.png"),
    load_texture("assets/ice.png")
]
punch_sound = Audio('assets/break.ogg', loop=False, autoplay=False)
player_movement_sound = Audio('assets/move.mp3', loop=True, autoplay=False)
bgm = Audio("assets/music.ogg", loop=True, autoplay=True)
window.fps_counter.enabled = False
window.exit_button.visible = False
window.fullscreen = True
window.borderless = False
window.color = color.rgb(0, 181, 226)
window.show_ursina_splash = True
window.title = 'PyineCraft'
noise = PerlinNoise(octaves=2, seed=123456)
block_id = 1
pcs = 0


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='assets/grassblock.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5,
            shader=basic_lighting_shader
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                Voxel(position=self.position + mouse.normal,
                      texture=blocks[block_id])
            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)


def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]


def trunk(parent):
    for __z in range(1):
        for __x in range(1):
            for __y in range(3):
                voxel = Voxel(position=(__x, __y-3, __z), texture=blocks[6])
                voxel.parent = parent


def crown(parent):
    for ___z in range(3):
        for ___x in range(3):
            for ___y in range(3):
                voxel = Voxel(position=(___x-1, ___y, ___z-1),
                              texture='assets/leaves.png')
                voxel.parent = parent


def plantTree(_x, _y, _z):
    tree = Entity(model=None,
                  position=Vec3(_x, _y, _z))
    trunk(tree)
    crown(tree)
    tree.y = 3


def checkTree(_x, _y, _z):
    freq = 3
    amp = 100
    treeChance = ((noise([_x/freq, _z/freq]))*amp)
    if treeChance > 20:
        plantTree(_x, _y, _z)


def genTrees(_x, _z, plantTree=True):
    y = 1
    freq = 16
    amp = 21
    y += ((noise([_x/freq, _z/freq]))*amp)
    if plantTree == True:
        checkTree(_x, y, _z)


def update():

    if held_keys['left mouse down'] or held_keys['right mouse down']:
        punch_sound.play()
        hand.active()
    else:
        hand.passive()

    if held_keys['/']:
        pcs = 1

    if held_keys['control up']:
        player.speed = 5

    if held_keys['control']:
        player.speed = 10

    if player.y < -6:
        player.y = 15
        player.x = 0
        player.z = 0

    if held_keys['escape']:
        sys.exit()

    genTrees(randrange(-500, 500), randrange(-200, 200))
    genTerr()

    dragon.look_at(player, 'forward')
    dragon.rotation_x = 0


class Dragon(Button):
    def __init__(self, position=(3, 2, 3), texture='assets/ender_dragon.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/ender_dragon.fbx',
            origin_y=1,
            texture=texture,
            shader=basic_lighting_shader,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            y=3,
            scale=0.020,
            double_sided=True,
            collider='mesh'
        )


class Sun(Entity):
    def __init__(self, position=(1000, 700, 1000)):
        super().__init__(
            parent=scene,
            position=position,
            model='sphere',
            color=color.yellow,
            scale=150,
            collider='mesh'

        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/block',
            texture=blocks[block_id],
            scale=0.2,
            rotation=Vec3(-10, -10, 10),
            position=Vec2(0.6, -0.6)
        )

    def active(self):
        hand.position = Vec2(0.4, -0.5)

    def passive(self):
        hand.position = Vec2(0.6, -0.6)


class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(0.8, 0.10, 0),
            position=Vec2(0, -0.4),
            texture='assets/inventory.png'
        )


freq = 24
amp = 6
shells = []
terrainWidth = 20

for i in range(terrainWidth*terrainWidth):
    ent = Voxel(texture=blocks[1])
    shells.append(ent)


def genTerr():
    for i in range(len(shells)):
        x = shells[i].x = floor((i/terrainWidth)+player.x-0.5*terrainWidth)
        z = shells[i].z = floor((i % terrainWidth)+player.z-0.5*terrainWidth)
        y = shells[i].y = floor((noise([x/freq, z/freq]))*amp)


player.gravity = 0.6
sun = Sun()
DirectionalLight(parent=Voxel, y=2, z=3, shadows=True)
player.jumping = True
player.cursor = Entity(parent=camera.ui, model='quad',
                       color=color.light_gray, scale=.008, rotation_z=45)
inventory = Inventory()
hand = Hand()
dragon = Dragon()
player.y = 50
dragon.add_script(SmoothFollow(target=player, offset=[
    4, 1, 2], speed=0.5))
app.run()
