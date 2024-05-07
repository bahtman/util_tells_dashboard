import streamlit as st
from cs_bahtml.plotting import add_smoke_wall, add_players
from cs_bahtml.radars import RADARS
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_json('./data/parsed_clusters.json')
    return df

def split_positions(coords, map):
    if map == 'de_vertigo':
        threshold = 11666
    elif map == 'de_nuke':
        threshold = -450
    else:
        raise ValueError("Map not supported")
    coords_lower = [(x,y,z) for (x,y,z) in coords if z<=threshold]
    coords = [(x,y,z) for (x,y,z) in coords if z>threshold]
    return coords, coords_lower


def set_map(map, row = None):
    fig = RADARS[map].copy()
    if map in ['de_vertigo', 'de_nuke']:
        map2 = map+"_lower"
        fig2 = RADARS[map2].copy()
        st.session_state.fig2 = fig2
    if not row is None:
        side = row['throwerSide']
        players = row['alive_players']
        util = [row['landCords']]
        thrower = [row['throwCords']]
        dead_players = row['dead_players']
        if dead_players is None:
            dead_players = []
        if map in ['de_vertigo', 'de_nuke']:
            players, players_lower = split_positions(players, map)
            dead_players, dead_players_lower = split_positions(dead_players, map)
            util, util_lower = split_positions(util, map)
            thrower, thrower_lower = split_positions(thrower, map)
            fig2 = add_players(fig2, players_lower, map, type = side)
            fig2 = add_players(fig2, dead_players_lower, map, type = 'dead_'+side)
            fig2 = add_smoke_wall(fig2, util_lower, map, type = row['grenade_type'])
            fig2 = add_players(fig2, thrower_lower, map, type = 'thrower')
            st.session_state.fig2 = fig2
        fig = add_players(fig, thrower, map, type = 'thrower')
        fig = add_smoke_wall(fig, util, map, type = row['grenade_type'])
        fig = add_players(fig, players, map, type = side)
        fig = add_players(fig, dead_players, map, type = 'dead_'+side)
    st.session_state.fig = fig
    