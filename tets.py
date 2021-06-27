from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time

shape_model = input("What kind of model do you want to render? >> ")

app = Ursina()

from ursina.shaders import lit_with_shadows_shader # you have to apply this shader to enties for them to recieve shadows.

EditorCamera()
Entity(model='plane', scale=10, color=color.gray, shader=lit_with_shadows_shader)
cube = Entity(model=shape_model, color=color.cyan, y=1, shader=lit_with_shadows_shader)
pivot = Entity()


DirectionalLight(parent=pivot, y=2, z=3, shadows=True)

app.run()