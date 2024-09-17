import pyglet

def soundTest():

	X = pyglet.resource.media('Sounds/bruh.mp3', streaming=False)
	player = pyglet.media.Player()
	player.queue(X)
	player.volume = 1
	player.play()
	print(pyglet.options['audio'])
	print("did you hear")
