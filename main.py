from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader
import random
import sys
from numpy import floor

app = Ursina()
player = FirstPersonController()

blocks = [
    load_texture('asset/grassblock.png'),
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

block_id = 1


def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]


def update():
    global block_pick

    if held_keys['left mouse down'] or held_keys['right mouse down']:
        punch_sound.play()
        hand.active()
    else:
        hand.passive()

    if player.y < -6:
        player.y = 15
        player.x = 0
        player.z = 0

    if held_keys['escape']:
        sys.exit()

    genTerr()

    creeper.look_at(player, 'forward')
    creeper.rotation.x = 0


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


class Creeper(Entity):
    def __init__(self, position=(3, 1, 3), texture='assets/creeper.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/creeper.fbx',
            origin_y=1,
            texture=texture,
            shader=basic_lighting_shader,
            scale=0.08,
            double_sided=True,
            collider='mesh'
        )


#


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


noise = PerlinNoise(octaves=3, seed=123456)

freq = 24
amp = 6
shells = []
terrainWidth = 30

for i in range(terrainWidth*terrainWidth):
    ent = Voxel(texture=blocks[1])
    shells.append(ent)


def genTerr():
    for i in range(len(shells)):
        x = shells[i].x = floor((i/terrainWidth)+player.x-0.5*terrainWidth)
        z = shells[i].z = floor((i % terrainWidth)+player.z-0.5*terrainWidth)
        y = shells[i].y = floor((noise([x/freq, z/freq]))*amp)


player.gravity = 0.6
DirectionalLight(parent=Voxel, y=2, z=3, shadows=True)
player.jumping = True
player.cursor = Entity(parent=camera.ui, model='quad',
                       color=color.light_gray, scale=.008, rotation_z=45)
inventory = Inventory()
hand = Hand()
creeper = Creeper()

app.run()
