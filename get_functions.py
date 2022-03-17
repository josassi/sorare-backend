from requests import post as post
from requests_functions import *
from etl_functions import *
from datetime import datetime
from time import sleep

URL = 'https://api.sorare.com/graphql'
COMPETITIONS = ["bundesliga-de",
                "ligue-1-fr",
                "laliga-santander",
                "serie-a-it"]
PLAYER_SLUG_EXAMPLE = 'benjamin-pavard'
EXPORT_PATH = "~/Documents/Code/Sorare/"
CLUB_SLUG_EXAMPLE = "strasbourg-strasbourg"
SLEEP = 2


def get_clubs_from_compet(competition_slug: str, attributes_list: list = None) -> pd.DataFrame:
    """
    Function to get a dataframe with all the clubs in the given competition.
    :param competition_slug: competition slug, example: "ligue-1-fr"
    :param attributes_list: list of attributes in the GraphQL scheme.
    :return: Dataframe with all clubs slug and name
    """

    if attributes_list is None:
        attributes_list = ['data', 'competition', 'clubs', 'nodes']
    sleep(SLEEP)
    r = post(URL, json={'query': clubs_from_compet_query(competition=competition_slug)})
    return request_to_df(r, attributes_list=attributes_list)


def get_players_from_club(club_slug, attributes_list=None) -> pd.DataFrame:
    if attributes_list is None:
        attributes_list = ['data', 'club', 'activePlayers', 'nodes']
    sleep(SLEEP)
    r = post(URL, json={'query': players_from_club_query(club_slug=club_slug)})
    return request_to_df(r, attributes_list=attributes_list)


def get_cards_from_player(player_slug,
                          rarity_list: str = "[unique, super_rare, rare, limited]",
                          attributes_list=None,
                          end_cursor: str = None) -> pd.DataFrame:
    if attributes_list is None:
        attributes_list = ['data', 'player', 'cards', 'nodes']
    sleep(SLEEP)
    r = post(URL, json={
        'query': cards_from_player_query(player_slug=player_slug, rarity_list=rarity_list, end_cursor=end_cursor)})
    return request_to_df(r, attributes_list=attributes_list)


def get_all_cards_from_player(player_slug,
                              rarity_list: str = "[unique, super_rare, rare, limited]",
                              attributes_list=None) -> pd.DataFrame:
    if attributes_list is None:
        attributes_list = ['data', 'player', 'cards', 'edges']
    sleep(SLEEP)
    r_page = post(URL, json={
        'query': cards_from_player_pagination_query(player_slug=player_slug, rarity_list=rarity_list)}).json()
    df_total = get_cards_from_player(player_slug=player_slug, rarity_list=rarity_list, attributes_list=attributes_list)
    if len(df_total) == 0:
        return pd.DataFrame()
    has_next_page = r_page["data"]["player"]["cards"]["pageInfo"]["hasNextPage"]
    end_cursor = r_page["data"]["player"]["cards"]["pageInfo"]["endCursor"]
    while has_next_page:
        # GET THE DATA
        df_tmp = get_cards_from_player(player_slug=player_slug, rarity_list=rarity_list,
                                       attributes_list=attributes_list, end_cursor=end_cursor)
        df_total = pd.concat([df_total, df_tmp])

        # UPDATE THE PAGINATION DATA
        sleep(SLEEP)
        r_page = post(URL, json={
            'query': cards_from_player_pagination_query(player_slug=player_slug, rarity_list=rarity_list,
                                                        end_cursor=end_cursor)}).json()
        has_next_page = r_page["data"]["player"]["cards"]["pageInfo"]["hasNextPage"]
        end_cursor = r_page["data"]["player"]["cards"]["pageInfo"]["endCursor"]

    if "node.latestEnglishAuction.endDate" in df_total.columns:
        df_total.loc[:, "node.latestEnglishAuction.endDate"] = pd.to_datetime(
            df_total["node.latestEnglishAuction.endDate"])

    return df_total


def get_price_info_from_cards_df(df_cards: pd.DataFrame) -> (dict, pd.DataFrame):
    """
    Function scrapping relevqnt price information from a cards dataframe.
    :param df_cards: dataframe containing cards with liveSingleSaleOffer and latestEnglishAuction information
    :return: a dict with last_auction_price and lower_single_sale_offer, and the entry dataframe with an
    additional "%toLastAuctionPrice" column comparing the single sale offer to the latest auction price.
    """

    price_dict = {}
    price_dict["last_auction_price"] = None
    price_dict["max_auction_price"] = None
    price_dict["average_auction_price"] = None
    price_dict["lower_single_sale_offer"] = None

    now = pd.to_datetime(datetime.now().astimezone())

    if "node.liveSingleSaleOffer.price" in df_cards.columns:
        df_cards["node.liveSingleSaleOffer.price"] = df_cards["node.liveSingleSaleOffer.price"].fillna(0).apply(lambda x:float(x))
        price_dict["lower_single_sale_offer"] = df_cards["node.liveSingleSaleOffer.price"].min()

    if "node.latestEnglishAuction.endDate" in df_cards.columns:
        df_cards["node.latestEnglishAuction.currentPrice"] = df_cards["node.latestEnglishAuction.currentPrice"].fillna(
            0).apply(lambda x: int(x))
        df_cards["node.latestEnglishAuction.endDate"] = pd.to_datetime(df_cards["node.latestEnglishAuction.endDate"])

        mask_1 = (df_cards["node.latestEnglishAuction.open"]).fillna(True)
        mask_2 = (df_cards["node.latestEnglishAuction.cancelled"]).fillna(True)
        mask_3 = (df_cards["node.latestEnglishAuction.endDate"] <= now).fillna(True)

        df_auction = df_cards[(~mask_1) & mask_2 & (~mask_3)]
        df_auction = df_auction.sort_values(by="node.latestEnglishAuction.endDate", ascending=False)
        mask_4 = (df_auction["node.latestEnglishAuction.currentPrice"] > 0).fillna(True)

        if len(df_auction) > 0:
            price_dict["last_auction_price"] = df_auction[mask_4]["node.latestEnglishAuction.currentPrice"].iloc[0]
            price_dict["max_auction_price"] = df_auction["node.latestEnglishAuction.currentPrice"].max()
            price_dict["average_auction_price"] = df_auction["node.latestEnglishAuction.currentPrice"].mean()

    # df_cards.loc["%toLastAuctionPrice"] = (df_cards["node.liveSingleSaleOffer.price"]
    #                                        - price_dict["last_auction_price"]) / price_dict["last_auction_price"]

    return price_dict

