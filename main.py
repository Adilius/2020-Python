import api
from game_layer import GameLayer

f=open("apikey.txt", "r")
api_key = f.read()
f.close()

map_name = "training1"  # TODO: You map choice here. If left empty, the map "training1" will be selected.

game_layer = GameLayer(api_key)


def main():
    game_layer.new_game(map_name)
    print("Starting game: " + game_layer.game_state.game_id)
    game_layer.start_game()
    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        take_turn()
    print("Done with game: " + game_layer.game_state.game_id)
    print("Final score was: " + str(game_layer.get_score()["finalScore"]))


def take_turn():
    # TODO Implement your artificial intelligence here.
    # TODO Take one action per turn until the game ends.
    # TODO The following is a short example of how to use the StarterKit

    state = game_layer.game_state

    #Update map with buildings
    for i in range(len(state.residences)):
        state.map[state.residences[i].X][state.residences[i].Y] = 2

    #Scan for broken stuff
    broken_stuff_list = []
    broken_stuff_health = []
    broken_stuff_residences = []
    for i in range(len(state.residences)):
        if state.residences[i].health < 40+(0.5*len(state.residences)):
            broken_stuff_list.append(i)
            broken_stuff_health.append(state.residences[i].health)
            broken_stuff_residences.append(state.residences[i])

    #Scan for too hot stuff
    cold_stuff_list = []
    cold_stuff_temperature = []
    cold_stuff_residences = []
    for i in range(len(state.residences)):
        if state.residences[i].temperature < 17:
            cold_stuff_list.append(i)
            cold_stuff_temperature.append(state.residences[i].temperature)
            cold_stuff_residences.append(state.residences[i])

    #Scan for too cold stuff
    hot_stuff_list = []
    hot_stuff_temperature = []
    hot_stuff_residences = []
    for i in range(len(state.residences)):
        if state.residences[i].temperature > 25:
            hot_stuff_list.append(i)
            hot_stuff_temperature.append(state.residences[i].temperature)
            hot_stuff_residences.append(state.residences[i])
    

    #If got broken stuff, fix it
    if len(broken_stuff_list) > 0:
        broken_stuff_value = min(broken_stuff_health)   #What is the lowest health value
        broken_stuff_index = broken_stuff_health.index(broken_stuff_value)  #What is it's index in our own list
        broken_stuff_building = broken_stuff_list[broken_stuff_index]   #Get corresponding index in actual list
        game_layer.maintenance((state.residences[broken_stuff_building].X, state.residences[broken_stuff_building].Y))
    #If got cold stuff, warm it
    elif len(cold_stuff_list) > 0:
        cold_stuff_value = min(cold_stuff_temperature)
        cold_stuff_index = cold_stuff_temperature.index(cold_stuff_value)
        cold_stuff_building = cold_stuff_list[cold_stuff_index]
        blueprint = game_layer.get_residence_blueprint(state.residences[cold_stuff_building].building_name)
        energy = blueprint.base_energy_need + 0.6 \
                    + (state.residences[cold_stuff_building].temperature - state.current_temp) * blueprint.emissivity / 1 \
                    - state.residences[cold_stuff_building].current_pop * 0.04
        game_layer.adjust_energy_level((state.residences[cold_stuff_building].X, state.residences[cold_stuff_building].Y), energy)
    elif len(hot_stuff_list) > 0:
        hot_stuff_value = min(hot_stuff_temperature)
        hot_stuff_index = hot_stuff_temperature.index(hot_stuff_value)
        hot_stuff_building = hot_stuff_list[hot_stuff_index]
        blueprint = game_layer.get_residence_blueprint(state.residences[hot_stuff_building].building_name)
        energy = blueprint.base_energy_need - 0.6 \
                    + (state.residences[hot_stuff_building].temperature - state.current_temp) * blueprint.emissivity / 1 \
                    - state.residences[hot_stuff_building].current_pop * 0.04
        game_layer.adjust_energy_level((state.residences[hot_stuff_building].X, state.residences[hot_stuff_building].Y), energy)



    if len(state.residences) < 1:
        for i in range(len(state.map)):
            for j in range(len(state.map)):
                if state.map[i][j] == 0:
                    x = i
                    y = j
                    break
        game_layer.place_foundation((x, y), game_layer.game_state.available_residence_buildings[0].building_name)
    else:
        the_only_residence = state.residences[0]
        if the_only_residence.build_progress < 100:
            game_layer.build((the_only_residence.X, the_only_residence.Y))
        #elif the_only_residence.health < 50:
        #    game_layer.maintenance((the_only_residence.X, the_only_residence.Y))
        #elif the_only_residence.temperature < 18:
        #    blueprint = game_layer.get_residence_blueprint(the_only_residence.building_name)
        #    energy = blueprint.base_energy_need + 0.5 \
        #             + (the_only_residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
        #             - the_only_residence.current_pop * 0.04
        #    game_layer.adjust_energy_level((the_only_residence.X, the_only_residence.Y), energy)
        #elif the_only_residence.temperature > 24:
        #    blueprint = game_layer.get_residence_blueprint(the_only_residence.building_name)
        #    energy = blueprint.base_energy_need - 0.5 \
        #             + (the_only_residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
        #             - the_only_residence.current_pop * 0.04
        #    game_layer.adjust_energy_level((the_only_residence.X, the_only_residence.Y), energy)
        elif state.available_upgrades[0].name not in the_only_residence.effects:
            game_layer.buy_upgrade((the_only_residence.X, the_only_residence.Y), state.available_upgrades[0].name)
        else:
            game_layer.wait()
    for message in game_layer.game_state.messages:
        print(message)
    for error in game_layer.game_state.errors:
        print("Error: " + error)


if __name__ == "__main__":
    main()