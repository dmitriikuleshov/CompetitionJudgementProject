from math import ceil
from typing import NamedTuple, List, Tuple

Place = float


class Player:
    """
    Player objects are used for collecting information
    about player in competition:
        places given by judges
        player's id
    """

    def __init__(self, id: int):
        self.id = id
        self.places: List[float] = []
        self.rating: List[int] = []

    def get_id(self):
        return self.id

    def add_place(self, new_place: Place):
        self.places.append(new_place)

    def set_rating(self, rating: List[int]):
        self.rating = rating

    def __repr__(self):
        return str(self.id)


class Judge:
    """
    Judge objects are used to give places to players.
    Every judge in competition gives every player a place.
    One judge can't give two or more players one place.
    """

    def __init__(self, id: int):
        self.id = id
        self.used_places: list[Place] = []

    def use_place(self, place: Place) -> None:
        self.used_places.append(place)

    def __repr__(self):
        return f"judge(id={self.id})"


class RatingInformation(NamedTuple):
    """
    RatingInformation are used to contain data
    about players, who have the same rating
    Example: players = [1, 2], rating = [1, 2, 3]
    Example: players = [5], rating = [0, 2, 3]
    """
    players: List[Player]
    rating: List[int]


class PrintInformation(NamedTuple):
    player: Player
    place: Place


def generate_players() -> list[Player]:
    try:
        number_of_players = int(input("Enter the number of "
                                      "participants in the competition: "))
    except ValueError:
        print("Invalid input, please try again")
        return generate_players()
    players = [Player(id) for id in range(1, number_of_players + 1)]
    return players


def generate_judges() -> list[Judge]:
    try:
        number_of_judges = int(input("Enter the number of "
                                     "judges in the competition: "))
    except ValueError:
        print("Invalid input, please try again")
        return generate_judges()
    judges = [Judge(id) for id in range(1, number_of_judges + 1)]
    return judges


def input_place(player: Player) -> Place:
    while True:
        try:
            place = int(input(f"\tenter the place for participant {player.get_id()}: "))
            break
        except ValueError:
            print("\tInvalid input, please try again")
    return place


def give_place(player: Player, judge: Judge, number_of_players: int) -> None:
    place = input_place(player)
    if not (0 < place < number_of_players + 1):
        print("\tThe place is out of range, please try again")
        return give_place(player, judge, number_of_players)
    if place in judge.used_places:
        print("\tThis rating has already been set, try another one")
        return give_place(player, judge, number_of_players)
    judge.use_place(place)
    player.add_place(place)


def give_places(players: list[Player], judges: list[Judge]) -> None:
    for judge in judges:
        print(f"Judge {judge.id} places: ")
        for player in players:
            give_place(player, judge, len(players))


def get_correct_place(place_counter: Place, num_of_players: int) -> float:
    if num_of_players == 1:
        return place_counter
    return (place_counter * num_of_players +
            sum(x for x in range(1, num_of_players))) / num_of_players


def make_ratings(players: list[Player], judges: list[Judge]) -> list[RatingInformation]:
    # для каждого игрока: список из чисел, обозначающих количество мест
    # [1,   2,   3]
    #  1,  1-2,  1-3
    players_data: {Player: list[int]} = {player: [0 for _ in range(len(players))]
                                         for player in players}
    for player in players:
        for ind in range(len(players)):
            players_data[player][ind] = len([place for place in
                                             player.places if place <= ind + 1])
        player.set_rating(players_data[player])

    players_ratings: list[RatingInformation] = []
    for player in players:
        the_same_flag = False
        for ind, rating_info in enumerate(players_ratings):
            if players_data[player] == rating_info.rating:
                players_ratings[ind].players.append(player)
                the_same_flag = True
                break

        if not the_same_flag:
            players_ratings.append(RatingInformation(players=[player],
                                                     rating=players_data[player]))
    return players_ratings


def print_players_place_info(players_place_info: List[Tuple[RatingInformation, Place]]) -> None:
    print_data = [PrintInformation(place=rating_info_place_tup[1], player=player)
                  for rating_info_place_tup in players_place_info
                  for player in rating_info_place_tup[0].players]
    # sort information by players' id
    print_data.sort(key=lambda print_info: print_info.player.id)

    for print_info in print_data:
        print(f"participant №{print_info.player}"
              f" -- marks {print_info.player.places}"
              f" -- rating {print_info.player.rating}"
              f" -- PLACE {print_info.place}")


def compare_players(players: list[Player],
                    judges: list[Judge],
                    players_ratings: list[RatingInformation]
                    ) -> List[Tuple[RatingInformation, Place]]:
    result_players_place_info: List[Tuple[RatingInformation, Place]] = []

    place_counter: Place = 1
    ratings_num = len(players_ratings[0].rating)
    judges_majority = ceil(len(judges) / 2)
    for ind in range(ratings_num):
        if not players_ratings:
            break
        # сортировка по оценкам судей
        players_ratings.sort(key=lambda top_player: sum(sorted(top_player.players[0].places)[0:ind + 1]))
        players_ratings.reverse()
        # cортировка по рейтингу
        for recurse_win_ind in range(len(players) - 1, -1, -1):
            players_ratings.sort(key=lambda rate_info: rate_info.rating[recurse_win_ind])

        players_ratings.sort(key=lambda rate_info: rate_info.rating[ind])

        # определение места по большинству
        win_rate = players_ratings[-1].rating[ind]
        if not (win_rate < judges_majority):
            current_best = players_ratings[-1]
            correct_place = get_correct_place(place_counter=place_counter,
                                              num_of_players=len(current_best.players))
            result_players_place_info.append((current_best, correct_place))
            place_counter += len(current_best.players)

            rating_indexes_to_delete: [int] = [-1]
            for check_for_next_best_ind in range(len(players_ratings) - 2, -1, -1):
                next_best = players_ratings[check_for_next_best_ind]
                next_best_rate = next_best.rating[ind]
                if next_best_rate == win_rate:
                    correct_place = get_correct_place(place_counter=place_counter,
                                                      num_of_players=len(next_best.players))
                    result_players_place_info.append((next_best, correct_place))
                    rating_indexes_to_delete.append(check_for_next_best_ind)
                    place_counter += len(next_best.players)

            for index in rating_indexes_to_delete:
                players_ratings.pop(index)
    return result_players_place_info


def main():
    players = generate_players()
    judges = generate_judges()
    give_places(players, judges)
    players_ratings = make_ratings(players, judges)
    result_players_place_info = compare_players(players, judges, players_ratings)
    print_players_place_info(result_players_place_info)


if __name__ == "__main__":
    main()
