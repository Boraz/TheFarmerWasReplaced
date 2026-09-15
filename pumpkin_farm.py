def goto(tx, ty):
	while get_pos_x() != tx:
		move(East)
	while get_pos_y() != ty:
		move(North)

def run():
	clear()
	
	# --- DYNAMIC GRID MATH ---
	size = get_world_size()
	q = size // 2       # Quadrant size (16 for a 32x32 grid)
	m = q - 1           # Max local coordinate (15 for a 32x32 grid)
	
	def maintain():
		if get_entity_type() == Entities.Dead_Pumpkin:
			harvest()
		if get_entity_type() != Entities.Pumpkin:
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
		if not can_harvest():
			if get_water() < 0.2:
				use_item(Items.Water)

	# --- THE FOUR DIRECTIONAL SNAKES ---
	# They now use 'q' for the modulo and 'm' for the boundaries
	
	def snake_W_to_E():
		lx = get_pos_x() % q
		ly = get_pos_y() % q
		if lx % 2 == 0:
			if ly < m:
				move(North)
			else:
				move(East)
		else:
			if ly > 0:
				move(South)
			else:
				if lx < m:
					move(East)
				else:
					for _ in range(m):
						move(West)

	def snake_E_to_W():
		lx = get_pos_x() % q
		ly = get_pos_y() % q
		if lx % 2 == 1:
			if ly < m:
				move(North)
			else:
				move(West)
		else:
			if ly > 0:
				move(South)
			else:
				if lx > 0:
					move(West)
				else:
					for _ in range(m):
						move(East)

	def snake_S_to_N():
		lx = get_pos_x() % q
		ly = get_pos_y() % q
		if ly % 2 == 0:
			if lx < m:
				move(East)
			else:
				move(North)
		else:
			if lx > 0:
				move(West)
			else:
				if ly < m:
					move(North)
				else:
					for _ in range(m):
						move(South)

	def snake_N_to_S():
		lx = get_pos_x() % q
		ly = get_pos_y() % q
		if ly % 2 == 1:
			if lx < m:
				move(East)
			else:
				move(South)
		else:
			if lx > 0:
				move(West)
			else:
				if ly > 0:
					move(South)
				else:
					for _ in range(m):
						move(North)

	# --- THE SQUAD ROLES ---
	
	def worker_N_to_S():
		while True:
			maintain()
			snake_N_to_S()
			
	def worker_E_to_W():
		while True:
			maintain()
			snake_E_to_W()
			
	def worker_S_to_N():
		while True:
			maintain()
			snake_S_to_N()
			
	def checker_W_to_E():
		change_hat(Hats.Purple_Hat)
		mature_count = 0
		while True:
			lx = get_pos_x() % q
			ly = get_pos_y() % q
			
			if lx == 0 and ly == 0:
				mature_count = 0
				
			maintain()
			
			if can_harvest():
				mature_count += 1
				
			# Triggers harvest when all 256 tiles in the 16x16 quadrant are mature
			if mature_count == q * q:
				harvest()
				
			snake_W_to_E()

	# --- DEPLOY THE MESH NETWORK ---
	
	# Base corners dynamically adapt to the board size
	corners_x = [q, q, 0, 0]
	corners_y = [0, q, q, 0]
	
	for i in range(4):
		bx = corners_x[i]
		by = corners_y[i]
		
		# Deploy N_to_S Worker (Starts Top-Left of quadrant)
		goto(bx, by + m)
		spawn_drone(worker_N_to_S)
		
		# Deploy E_to_W Worker (Starts Bottom-Right of quadrant)
		goto(bx + m, by)
		spawn_drone(worker_E_to_W)
		
		# Deploy S_to_N Worker (Starts Bottom-Left of quadrant)
		goto(bx, by)
		spawn_drone(worker_S_to_N)
		
		# Deploy W_to_E Checker (Starts Bottom-Left of quadrant)
		goto(bx, by)
		
		if i < 3:
			spawn_drone(checker_W_to_E)
		else:
			checker_W_to_E()
