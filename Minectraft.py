from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from ursina.shaders import lit_with_shadows_shader


World_X = 20
World_Y = 20
World_Z = 5

list = ['x', 'y']

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop = False, autoplay = False)
block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False
window.title = 'Minectraft'

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


class Voxel(Button):
	def __init__(self, position = (0, 0, 0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0, 0, random.uniform(0.9, 1)),
			scale = 0.5)

	def input(self, key):
		if self.hovered:

			if key == 'right mouse down':
				punch_sound.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

				print ("block placed at " + str(self.position + mouse.normal))

			if key == 'left mouse down':
				punch_sound.play()
				destroy(self)

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150, -10, 0),
			position = Vec2(0.4, -0.6))

	def active(self):
			self.position = Vec2(0.3, -0.5)

	def passive(self):
		self.position = Vec2(0.4, -0.6)

def more_blocks(x, z, y):

	is_there_another_block = random.randint(1, 5)
	if is_there_another_block == 1 or is_there_another_block == 2 or is_there_another_block == 3 :
		which_one = random.choice(list)
		if which_one == 'x':
			voxel = Voxel(position = (x + 1, 1, y))
			more_blocks(x + 1, 1, y)
		else:
			voxel = Voxel(position = (x, 1, y + 1))
			more_blocks(x, 1, y + 1)

def put_a_tree(x, y):
	for i in range(random.randint(4, 9)):
		voxel = Voxel(position = (x, i, y), texture = dirt_texture)
	print (i)

	voxel = Voxel(position = (x, i, y + 1), texture = stone_texture)
	voxel = Voxel(position = (x + 1, i, y), texture = stone_texture)
	voxel = Voxel(position = (x - 1, i, y), texture = stone_texture)
	voxel = Voxel(position = (x, i, y - 1), texture = stone_texture)

	voxel = Voxel(position = (x, i + 1, y), texture = stone_texture)
	voxel = Voxel(position = (x + 1, i, y + 1), texture = stone_texture)
	voxel = Voxel(position = (x + 1, i, y + 1), texture = stone_texture)
	voxel = Voxel(position = (x - 1, i, y + 1), texture = stone_texture)
	voxel = Voxel(position = (x + 1, i, y - 1), texture = stone_texture)
e = Entity(model='quad')

# initial World Gen

for z in range(World_Y):
	for x in range(World_X):
		for i in range(World_Z):
			i = -i
			if i < 0:
				dirt_or_stone = random.randint(1, 4)
				if dirt_or_stone == 1 or dirt_or_stone == 2 or dirt_or_stone == 3:
					voxel = Voxel(position = (x, i, z), texture = dirt_texture)
				else:
					voxel = Voxel(position = (x, i, z), texture = stone_texture)
			else:
				voxel = Voxel(position = (x, i, z))

for i in range(random.randint(2, 10)):
	put_a_tree(random.randint(1, World_X), random.randint(1, World_Y))

amount_of_anomolies = random.randint(2, 10)

for i in range(amount_of_anomolies):
	x = random.randint(1, World_X)
	y = random.randint(1, World_Y)
	voxel = Voxel(position = (x, 1, y))

	more_blocks(x, 1, y)


player = FirstPersonController(speed=6.5, jump_height=1, jump_duration=.3)
sky = Sky()
hand = Hand()

app.run()