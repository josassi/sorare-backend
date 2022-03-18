from query_functions.get_functions import *


def append_all_players_price_info_from_club(club_slug: str,
                                            list_players_price_info: list,
                                            rarity_list: str = "[unique, super_rare, rare, limited]",
                                            total_player_iteration: int = None,
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
        df_cards = get_all_cards_from_player(player_slug=player, rarity_list=rarity_list)
        if verbose:
            print(total_player_iteration, club_iteration, club_player_iteration, player, len(df_cards))
        if len(df_cards) > 0:
            price_dict = get_price_info_from_cards_df(df_cards=df_cards)
            price_dict["player.slug"] = player
            list_players_price_info.append(price_dict)
        if limit_players is not None and j == limit_players:
            break
    return total_player_iteration, club_iteration, club_player_iteration


def get_df_all_players_price_info_from_competition(competition_slug: str,
                                                   rarity_list: str = "[unique, super_rare, rare, limited]",
                                                   verbose: bool = False,
                                                   limit_players: int = None,
                                                   limit_club:int = None
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
        total_player_iteration, club_iteration, club_player_iteration = append_all_players_price_info_from_club(
            club_slug=club,
            list_players_price_info=list_players_price_info,
            rarity_list=rarity_list,
            verbose=verbose,
            limit_players=limit_players,
            club_iteration=club_iteration,
            total_player_iteration=total_player_iteration)
        if club_iteration is not None and club_iteration == limit_club:
            break
    df_final = pd.DataFrame(list_players_price_info)
    return df_final


# def get_cards_dataframe(competition_slug: str,
#                         verbose: bool = False,
#                         export_path: str = None) -> pd.DataFrame:
#     """
#
#     :param competition_slug:
#     :param verbose:
#     :param export_path:
#     :return:
#     """
#     df = pd.DataFrame()
#     df_clubs = get_clubs_from_compet(competition_slug=competition_slug)
#     for i, club in enumerate(df_clubs["slug"]):
#         df_players = get_players_from_club(club)
#         for j, player in enumerate(df_players["slug"]):
#             if verbose:
#                 print(player)
#                 print(i, j)
#             df_tmp = get_cards_from_player(player)
#             if len(df_tmp) != 0:
#                 df_tmp["Club Slug"] = club
#                 df_tmp["Player Slug"] = player
#                 df = pd.concat([df, df_tmp])
#             if j == 100:
#                 break
#         if i == 10:
#             break
#     if verbose:
#         print(df)
#
#     if export_path is not None:
#         df.to_csv(export_path)
#
#     return df


if __name__ == "__main__":
    # df_cards = get_all_cards_from_player(player_slug=PLAYER_SLUG_EXAMPLE, rarity_list="[limited]")
    # df.to_csv(EXPORT_PATH+"results_bp_limited.csv")

    # df = pd.read_csv(EXPORT_PATH + "results_bp_limited.csv")
    # a, b = get_price_info_from_cards_df(df)
    # print(a)
    df = get_df_all_players_price_info_from_competition(competition_slug=COMPETITIONS[1], rarity_list="[limited]",
                                                        verbose=True, limit_club=1)
    df.to_csv(EXPORT_PATH + "results_all_limited.csv")
