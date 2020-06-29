#!/usr/bin/python

from PIL import Image
from collections import deque
import math
import random

fractal = None
normal  = None
pal     = None
width   = None
height  = None

queue  = deque()

class Palette:
	a_r = 0.46
	a_g = 0.5
	a_b = 0.15
	b_r = 0.34
	b_g = 0.47
	b_b = 0.43
	c_r = 1.5
	c_g = 0.0
	c_b = 0.5
	d_r = 0.1
	d_g = 0.64
	d_b = 0.48

# returns RGB value (r,g,b) for value t (0.0 - 1.0)
def color_pixel(t, p):
	r = 255.* (p.a_r + p.b_r * math.cos(6.2832 * (p.c_r * t + p.d_r)))
	g = 255.* (p.a_g + p.b_g * math.cos(6.2832 * (p.c_g * t + p.d_g)))
	b = 255.* (p.a_b + p.b_b * math.cos(6.2832 * (p.c_b * t + p.d_b)))
	return (int(r), int(g), int(b))

def mid_pt(x,y):
	return ((x[0]+y[0]) // 2, (x[1]+y[1]) // 2)

# Complete a sub-square at corners a, b, c, d.
#
#   a---b
#   |   |
#   c...d
#
# factor 'r' dampens randomness at sub-steps
def popSquare(a, b, c, d, r):
	global fractal, normal, pal, width, height, queue

	average = 0
	for px in [a,b,c,d]:
		fractal[px[0],px[1]] = color_pixel(normal[px[0],px[1]], pal)
		average += normal[px[0],px[1]]
	average /= 4.0

	# fill the Center
	center = mid_pt(a,d)
	if a == center: # we have reached minimum spacing
		return
	normal[center[0],center[1]] = average + random.choice([-1.0,1.0]) * random.random() * 1.0 / r
	fractal[center[0],center[1]] = color_pixel(normal[center[0],center[1]], pal)

	# build the Diamond
	dist = abs(b[0] - a[0]) // 2
	dirs = [(dist,0),(-dist,0),(0,dist),(0,-dist)]
	for pt in [mid_pt(a,b),mid_pt(a,c),mid_pt(c,d),mid_pt(b,d)]:
		average = 0.0
		for dir in dirs:
			average += normal[(pt[0]+dir[0])%width, (pt[1]+dir[1])%height]
		average /= 4.0
		average += random.choice([-1.0,1.0]) * random.random() * 1.0 / r
		normal[pt[0],pt[1]] = average

	r += .8
	queue.append((a,mid_pt(a,b),mid_pt(a,c),center,r)) # a quad
	queue.append((mid_pt(a,b),b,center,mid_pt(b,d),r)) # b quad
	queue.append((mid_pt(a,c),center,c,mid_pt(c,d),r)) # c quad
	queue.append((center, mid_pt(b,d),mid_pt(c,d),d,r)) # d quad

if __name__ == "__main__":
	n = 10
	damp = 1.0

	fractal_img = Image.new('RGB', (2**n+1,2**n+1))
	width, height = fractal_img.size
	normal_img = Image.new('F',    (2**n+1,2**n+1))
	pal  = Palette()
	fractal  = fractal_img.load()
	normal   = normal_img.load()
	init_val = random.random()
	normal[0,0]       = init_val
	normal[0,2**n]    = init_val
	normal[2**n,0]    = init_val
	normal[2**n,2**n] = init_val
	popSquare((0,0),(2**n,0),(0,2**n),(2**n,2**n), damp)

	while len(queue) > 0:
		a, b, c, d, r = queue.popleft()
		popSquare(a,b,c,d,r)
	fractal_img.show()
	fractal_img.save("demo.png")

	#anim_steps = 10
	#for i in range(anim_steps):
	#	for x in range(width):
	#		for y in range(height):
	#			fractal[x,y] = color_pixel(normal[x,y] + i*(1.0 / anim_steps), pal)
	#	fractal_img.show()
