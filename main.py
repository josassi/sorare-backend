from query_functions.get_functions import *


def get_all_players_price_info(competition_slug: str,
                               rarity_list: str = "[unique, super_rare, rare, limited]",
                               verbose: bool = False
                               ) -> pd.DataFrame:
    """

    :param competition_slug:
    :param rarity_list:
    :param verbose:
    :return:
    """
    list_players_price_info = []
    clubs = set(get_clubs_from_compet(competition_slug=competition_slug)["slug"])
    k = 0
    for i, club in enumerate(clubs):
        # club = "reims-reims"
        players = set(get_players_from_club(club)["slug"])
        for j, player in enumerate(players):
            k += 1
            df_cards = get_all_cards_from_player(player_slug=player, rarity_list=rarity_list)
            if verbose:
                print(k, i, j, club, player, len(df_cards))
            if len(df_cards) > 0:
                price_dict = get_price_info_from_cards_df(df_cards=df_cards)
                price_dict["player.slug"] = player
                list_players_price_info.append(price_dict)
            if j == 100:
                break
        if i == 10:
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

    df = get_all_players_price_info(competition_slug=COMPETITIONS[1], rarity_list="[limited]", verbose=True)
    df.to_csv(EXPORT_PATH + "results_all_limited.csv")
