def run(crop_type):
	clear()
	size = get_world_size()
	total_drones = 16
	
	# Calculate how many rows each drone is responsible for
	rows_per_drone = size // total_drones
	if rows_per_drone == 0:
		rows_per_drone = 1
		
	def worker():
		while True:
			# Sweep the assigned rows
			for r in range(rows_per_drone):
				# Sweep the entire width of the board
				for c in range(size):
					if can_harvest():
						harvest()
					
					if get_entity_type() != crop_type:
						if crop_type != Entities.Grass and get_ground_type() != Grounds.Soil:
							till()
						plant(crop_type)
					
					if not can_harvest() and get_water() < 0.2:
						use_item(Items.Water)
						
					# Move forward safely (no collisions for Carrots/Grass)
					move(East)
				
				# If assigned multiple rows, step North to the next one
				if r < rows_per_drone - 1:
					move(North)
					
			# After finishing its sector, step South back to its starting row
			for r in range(rows_per_drone - 1):
				move(South)

	# DEPLOY THE SWARM
	# Cap the drone deployment if you have more drones than grid rows
	drones_to_deploy = total_drones
	if drones_to_deploy > size:
		drones_to_deploy = size
		
	for i in range(drones_to_deploy - 1):
		spawn_drone(worker)
		# Shift the main drone North to space out the next spawn
		for _ in range(rows_per_drone):
			move(North)
			
	# Put the Main Drone to work in the top sector
	worker()
