def farm_tile():
	is_tree_tile = (get_pos_x() + get_pos_y()) % 2 == 0
	
	if can_harvest():
		harvest()
		
	if get_ground_type() != Grounds.Soil:
		till()
		
	# Plant Tree on even tiles, Bushes on odd tiles
	if is_tree_tile:
		if get_entity_type() != Entities.Tree:
			plant(Entities.Tree)
	else:
		if get_entity_type() != Entities.Bush:
			plant(Entities.Bush)
			
	if not can_harvest() and get_water() < 0.2:
		use_item(Items.Water)
		
	# FERTILIZER COMPLETELY REMOVED!


def sector_worker():
	size = get_world_size()
	total_drones = 16
	
	# Calculate rows. If grid is smaller than 32, default to 1 row per drone.
	rows_to_cover = size // total_drones
	if rows_to_cover == 0:
		rows_to_cover = 1
	
	while True:
		for r in range(rows_to_cover):
			for c in range(size):
				farm_tile()
				move(East)
			
			# Step North to the next row in this drone's assigned sector
			if r < rows_to_cover - 1:
				move(North)
				
		# Sector finished! Reset by stepping South back to its starting row.
		for r in range(rows_to_cover - 1):
			move(South)


def run():
	clear()
	size = get_world_size()
	total_drones = 16
	
	rows_per_drone = size // total_drones
	if rows_per_drone == 0:
		rows_per_drone = 1
		
	# Cap the drone deployment if you have more drones than grid rows
	drones_to_deploy = total_drones
	if drones_to_deploy > size:
		drones_to_deploy = size
	
	for i in range(drones_to_deploy - 1):
		spawn_drone(sector_worker)
		
		# Move the main drone North to position the next clone
		for y in range(rows_per_drone):
			move(North)
			
	# The Main Drone handles the top sector
	sector_worker()
