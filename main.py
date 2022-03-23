from query_functions.get_functions import *


def append_all_players_price_info_from_club(club_slug: str,
                                            list_players_price_info: list,
                                            rarity_list: str = "[unique, super_rare, rare, limited]",
                                            total_player_iteration: int = 0,
                                            club_iteration: int = None,
                                            limit_players: int = None,
                                            verbose: bool = False,
                                            ) -> (int, int, int):
    """

    :param club_slug:
    :param rarity_list:
    :param list_players_price_info:
    :param total_player_iteration:
    :param club_iteration:
    :param limit_players:
    :param verbose:
    :return:
    """
    if list_players_price_info is None:
        list_players_price_info = []
    players = set(get_players_from_club(club_slug=club_slug)["slug"])
    club_player_iteration = 0
    for club_player_iteration, player in enumerate(players):
        club_player_iteration += 1
        total_player_iteration += 1
        df_cards = get_all_cards_from_player(player_slug=player, rarity_list=rarity_list)
        if verbose:
            print(total_player_iteration, club_iteration, club_player_iteration, player, len(df_cards))
        if len(df_cards) > 0:
            price_dict = get_price_info_from_cards_df(df_cards=df_cards)
            price_dict["player.slug"] = player
            list_players_price_info.append(price_dict)
        if limit_players is not None and club_player_iteration == limit_players:
            break
    return total_player_iteration, club_iteration, club_player_iteration


def append_all_players_price_and_score_info_from_club(club_slug: str,
                                                      list_players_price_info: list,
                                                      rarity_list: str = "[unique, super_rare, rare, limited]",
                                                      total_player_iteration: int = 0,
                                                      club_iteration: int = None,
                                                      limit_players: int = None,
                                                      verbose: bool = False,
                                                      ) -> (int, int, int):
    """

    :param club_slug:
    :param rarity_list:
    :param list_players_price_info:
    :param total_player_iteration:
    :param club_iteration:
    :param limit_players:
    :param verbose:
    :return:
    """
    if list_players_price_info is None:
        list_players_price_info = []
    df_players = get_players_from_club(club_slug=club_slug)
    club_player_iteration = 0
    for club_player_iteration, row_player in df_players.iterrows():
        club_player_iteration += 1
        total_player_iteration += 1
        player = row_player["slug"]
        df_cards = get_all_cards_from_player(player_slug=player, rarity_list=rarity_list)
        df_cards.to_csv(EXPORT_PATH + f"{player}_cards.csv")
        if verbose:
            print(total_player_iteration, club_iteration, club_player_iteration, player, len(df_cards))
        if len(df_cards) > 0:
            price_dict = get_price_info_from_cards_df(df_cards=df_cards)
            for column in row_player.index.drop("allSo5Scores.nodes"):
                price_dict[f"player.{column}"] = row_player[column]
            for n, score in enumerate(row_player["allSo5Scores.nodes"]):
                price_dict[f"player.score.{n}"] = score["score"]
            list_players_price_info.append(price_dict)
        if limit_players is not None and club_player_iteration == limit_players:
            break
    return total_player_iteration, club_iteration, club_player_iteration


def get_df_all_players_price_info_from_competition(competition_slug: str,
                                                   rarity_list: str = "[unique, super_rare, rare, limited]",
                                                   verbose: bool = False,
                                                   limit_players: int = None,
                                                   limit_club: int = None
                                                   ) -> pd.DataFrame:
    """

    :param competition_slug:
    :param rarity_list:
    :param verbose:
    :param limit_players:
    :param limit_club:
    :return:
    """
    list_players_price_info = []
    clubs = set(get_clubs_from_compet(competition_slug=competition_slug)["slug"])
    total_player_iteration = 0
    for club_iteration, club in enumerate(clubs):
        total_player_iteration, club_iteration, club_player_iteration = append_all_players_price_and_score_info_from_club(
            club_slug=club,
            list_players_price_info=list_players_price_info,
            rarity_list=rarity_list,
            verbose=verbose,
            limit_players=limit_players,
            club_iteration=club_iteration,
            total_player_iteration=total_player_iteration)
        if club_iteration is not None and club_iteration == limit_club - 1:
            break
    df_final = pd.DataFrame(list_players_price_info)
    return df_final


if __name__ == "__main__":
    COMPETITIONS = ["bundesliga-de",
                    "ligue-1-fr",
                    "laliga-santander",
                    "serie-a-it"]
    EXPORT_PATH = "~/Documents/Code/Sorare/"
    df = get_df_all_players_price_info_from_competition(competition_slug=COMPETITIONS[1], rarity_list="[limited]",
                                                        verbose=True, limit_club=10, limit_players=15)
    df.to_csv(EXPORT_PATH + "results_all_limited_score.csv")
