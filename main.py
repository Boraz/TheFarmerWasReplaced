import tree_farm
import pumpkin_farm
import generic_farm
import maze_solver

# --- FARM SELECTOR ---
# Assign the farm you want to run. 

# active_farm = tree_farm.run
# active_farm = pumpkin_farm.run
# active_farm = generic_farm.run(Entities.Bush)

active_farm = maze_solver.run
# Execute the selected farm
active_farm()
