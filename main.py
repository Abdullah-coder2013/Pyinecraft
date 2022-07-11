from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import sys
import keyboard

app = Ursina()

dirt = load_texture("assets/dirtblock.png")
sand = load_texture("assets/sand.png")
stone = load_texture("assets/stone.png")
grassblock = load_texture("assets/grassblock.png")
log = load_texture("assets/log.png")
planks = load_texture("assets/planks.png")
arm = load_texture("assets/alt.png")
cobble = load_texture("assets/cobbler.png")
punch_sound   = Audio('assets/break.ogg',loop = False, autoplay = False)
bgm = Audio("assets/music.ogg", loop = True, autoplay = True)
block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False
window.fullscreen = True
window.color = color.inverse(color.brown)

def update():
	global block_pick

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4
	if held_keys['5']: block_pick = 5
	if held_keys['6']: block_pick = 6
	if held_keys['7']: block_pick = 7
	if held_keys['8']: block_pick = 8
	if held_keys['escape']: sys.exit()


class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grassblock):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5
   			)

	def input(self,key):
		if self.hovered:
			if key == 'right mouse down':
				punch_sound.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grassblock)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = dirt)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = stone)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = cobble)
				if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = sand)
				if block_pick == 6: voxel = Voxel(position = self.position + mouse.normal, texture = log)
				if block_pick == 7: voxel = Voxel(position = self.position + mouse.normal, texture = planks)

			if key == 'left mouse down':
				punch_sound.play()
				destroy(self)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.7,-0.6))

	def active(self):
		self.position = Vec2(0.5,-0.5)

	def passive(self):
		self.position = Vec2(0.7,-0.6)
  
class Inventory(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'quad',
			scale = (0.6,0.10,0),
			position =  Vec2(0, -0.4),
			texture = 'assets/inventory.png'
		)

noise = PerlinNoise(octaves=3,seed=random.randint(1,1000000))

for z in range(-30,30):
	for x in range(-30,30):
	    y = noise([x * .02,z * .02])
	    y = math.floor(y * 7.5)
	    voxel = Voxel(position=(x,y,z))

player = FirstPersonController()
player.gravity = 0.6
player.cursor = Entity(parent=camera.ui, model='quad', color=color.light_gray, scale=.008, rotation_z=45)
hand = Hand()
inventory = Inventory()

app.run()