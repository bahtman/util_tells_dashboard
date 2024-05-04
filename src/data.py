import streamlit as st
from cs_bahtml.plotting import add_smoke_wall, add_players
from cs_bahtml.radars import RADARS
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_json('./data/parsed_clusters.json')
    return df


def set_map(map, row = None):
    fig = RADARS[map].copy()
    if not row is None:
        side = row['throwerSide']

        fig = add_players(fig, [row['throwCords']], map, type = 'thrower')
        fig = add_smoke_wall(fig, [row['landCords']], map, type = row['grenade_type'])
        fig = add_players(fig, row['alive_players'], map, type = side)
        if row['dead_players']:
            fig = add_players(fig, row['dead_players'], map, type = 'dead_'+side)
    st.session_state.fig = fig