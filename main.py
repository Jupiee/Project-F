from core.data_generator import Player_Gen

def main():
    generator = Player_Gen()
    team_players = [generator.generate_player() for _ in range(18)]

    for player in team_players:
        print(player)

if __name__ == "__main__":
    main()