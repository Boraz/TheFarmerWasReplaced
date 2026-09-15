# The Virtual Wall function prevents drones from escaping the bounding box
def safe_move(direction, maze_size):
	x = get_pos_x()
	y = get_pos_y()
	
	# Treat the coordinate limits as solid walls
	if direction == North and y >= maze_size - 1:
		return False
	if direction == East and x >= maze_size - 1:
		return False
	if direction == South and y <= 0:
		return False
	if direction == West and x <= 0:
		return False
		
	# If safe, execute the actual move
	return move(direction)

def spawn_maze(maze_size):
	# Anchor to (0,0) before spawning so the drones don't escape
	# Can remove this once 32 drones and just spawn the maze
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)
	if can_harvest():
		harvest()
		
	if get_ground_type() != Grounds.Soil:
		till()
		
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, maze_size)
	
def solve_maze(start_facing, base_prefer_right, maze_size):
	dirs = [North, East, South, West]
	facing = start_facing  
	
	while get_entity_type() != Entities.Treasure:
		current_prefer_right = base_prefer_right
		
		# The Slip Rule
		if random() < 0.05:
			if base_prefer_right:
				current_prefer_right = False
			else:
				current_prefer_right = True
				
		if current_prefer_right:
			preferred_turn = (facing + 1) % 4
			fallback_turn = (facing - 1) % 4
		else:
			preferred_turn = (facing - 1) % 4
			fallback_turn = (facing + 1) % 4
			
		# Swap out 'move' for our new 'safe_move' wrapper
		if safe_move(dirs[preferred_turn], maze_size):
			facing = preferred_turn
		elif safe_move(dirs[facing], maze_size):
			pass 
		else:
			facing = fallback_turn
			
	# The treasure is found, and walls drop!
	harvest()

def run():
	clear()
	
	total_drones = 16
	
	# Calculate the hard maze boundary here so we can pass it to the virtual walls
	maze_size = total_drones
	if maze_size > get_world_size():
		maze_size = get_world_size()
	
	spawn_maze(maze_size)
	
	configs = [
		(0, True),  
		(1, True),  
		(2, True),  
		(3, True),  
		(0, False), 
		(1, False), 
		(2, False), 
		(3, False), 
	]
	
	drones_per_faction = total_drones // 8
	
	for i in range(8):
		f_bias = configs[i][0]
		pr = configs[i][1]
		
		if i == 7:
			spawn_count = drones_per_faction - 1
		else:
			spawn_count = drones_per_faction
			
		for _ in range(spawn_count):
			def worker(facing=f_bias, prefer_right=pr):
				while True:
					solve_maze(facing, prefer_right, maze_size)
					spawn_maze(maze_size)
			
			spawn_drone(worker)
			
	while True:
		solve_maze(configs[7][0], configs[7][1], maze_size)
		spawn_maze(maze_size)
