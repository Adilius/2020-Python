import api
from game_layer import GameLayer

f=open("apikey.txt", "r")
api_key = f.read()
f.close()

map_name = "training1"  # TODO: You map choice here. If left empty, the map "training1" will be selected.

game_layer = GameLayer(api_key)



def main():
    game_layer.game_state.game_id = "25310ab5-c420-451f-b51d-edb56796c929"
    game_layer.end_game()
    print("Done with game: " + game_layer.game_state.game_id)
    print("Final score was: " + str(game_layer.get_score()["finalScore"]))

if __name__ == "__main__":
    main()