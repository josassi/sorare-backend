def clubs_from_compet_query(competition: str) -> str:
    return f"""{{competition(slug:"{competition}")
            {{
                clubs
                {{
                    nodes
                        {{
                            slug
                            name
                        }}
                    }}
                }}
            }}"""


def players_from_club_query(club_slug: str) -> str:
    return f"""{{club(slug:"{club_slug}")
                {{
                    activePlayers
                    {{
                        nodes
                            {{
                                slug
                                position
                                activeClub{{
                                slug
                                country{{code}}
                                }}
                                country{{code}}
                                age
                                allSo5Scores(first:15){{
                                nodes{{score}}
                                }}
                                
                            }}
                        }}
                    }}
                }}"""


def cards_from_player_query(player_slug: str, rarity_list: str, end_cursor: str = None) -> str:
    if end_cursor is not None:
        return f"""
    {{
    player(slug:"{player_slug}"){{
    cards(rarities:{rarity_list}, after:"{end_cursor}"){{
    
    edges{{

    node{{
    
    slug

    liveSingleSaleOffer{{
      price
    }}

    latestEnglishAuction{{
        currentPrice
        cancelled
        open
        endDate
    }}
    
    }}
    }}
    }}
    }}
    }}
"""
    return f"""
    {{
    player(slug:"{player_slug}"){{
    cards(rarities:{rarity_list}){{
    
    edges{{

    node{{
    
    slug

    liveSingleSaleOffer{{
      price
    }}

    latestEnglishAuction{{
        currentPrice
        cancelled
        open
        endDate
    }}
    
    }}
    }}
    }}
    }}
    }}
"""


def cards_from_player_pagination_query(player_slug: str, rarity_list: str, end_cursor: str = "") -> str:
    return f"""
    {{
    player(slug:"{player_slug}"){{
    cards(rarities:{rarity_list}, after:"{end_cursor}"){{
    
    pageInfo{{
        hasNextPage
        endCursor
    }}
    
    }}
    }}
    }}
"""
