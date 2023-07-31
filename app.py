import streamlit as st
import pandas as pd
from cs_bahtml.plotting import add_smoke_wall, load_map, add_players
from math import floor


st.set_page_config(layout="wide")

DATA_PATH = './data/'
MAP_PATH = './media/maps'
PAGINATION_SIZE = 5

def set_map(map, row = None):
    fig = load_map(MAP_PATH, map)
    if not row is None:
        side = row['throwerSide']

        fig = add_players(fig, [row['throwCords']], map, type = 'thrower')
        fig = add_smoke_wall(fig, [row['landCords']], map, type = row['grenadeType'])
        fig = add_players(fig, row['players'], map, type = side)
        fig = add_players(fig, row['dead_players'], map, type = 'dead_'+side)
    st.session_state.fig = fig
    
@st.cache_data
def load_data(selected):
    df = pd.read_json('./data/parsed_util.json')
    df = df[df.throwerTeam == selected].reset_index()
    df['throwSeconds'] = df['throwSeconds'].apply(int)
    return df

@st.cache_data
def tab_data(df, map):
    df = df[df.mapName == map].reset_index()
    df_t = df.query('throwerSide=="t"')
    df_ct = df.query('throwerSide=="ct"')
    return df_t, df_ct

@st.cache_data
def split_df(df, rows):
    df = [df.iloc[i:i+rows-1,:] for i in range(0,len(df),rows)]
    return df

@st.cache_data
def grouped_list(df):
    groups = df.groupby(["mapName","throwerSide","throwArea","landArea","grenadeType"]).groups
    group_list = [(df.loc[index,:],df.loc[index[0],"util_score"]) for index in groups.values()]
    return [sort[0] for sort in sorted(group_list, key = lambda tup: tup[1])]

def paginator_cb(key, change):
    st.session_state[key] += change

def get_cluster_overview(df, type):
    groups = grouped_list(df)
    for df_group in groups[0:10]:
        n_row = len(df_group)
        score = int(df_group['util_score'].min())
        util_type = df_group['grenadeType'].iloc[0]
        if score >900:
            continue

        

        with st.expander(f"Dissimilarity score: {score} - {n_row} occurences - {util_type}"):
            for idx, row in df_group.iterrows():
                st.divider()
                cc = st.columns([5,1])

                # cc[0].text('Opponent')
                # cc[0].text(row['ctTeam'])

                # cc[1].text('Round time')
                # cc[1].text(int(row['throwSeconds']))

                # cc[2].text('Secret')
                # cc[2].text(1.5)

                # cc[3].text('Yard')
                # cc[3].text(0)

                # cc[4].text('Ramp')
                # cc[4].text(0.5)

                # cc[5].text('Lobby/A')
                # cc[5].text(2)
                cc[0].dataframe(row[["throwerName", "throwSeconds", "opponentName"]].to_frame().T, hide_index=True, use_container_width=True)
                #



                cc[-1].write("")
                cc[-1].button(":punch:", key = idx, on_click=set_map, args=(row['mapName'],row))



def get_figure_col():
    st.image(st.session_state.fig)

def fill_tab(df, type):
    get_cluster_overview(df,type)
            
def clear_map():
    del st.session_state.fig


st.title('Utility tell tool')
selected = st.selectbox("Select team",["MOUZ","FaZe Clan"] )
df = load_data(selected)
map_pick = st.selectbox("Select map",df.mapName.unique(), on_change=clear_map)

if 'fig' not in st.session_state:
    set_map(map_pick)
df_t, df_ct = tab_data(df, map_pick)

cluster_col, fig_col =st.columns(2)

with cluster_col:
    t_tab, ct_tab = st.tabs(["T side", "CT side"])
    with t_tab:
        fill_tab(df_t,"t")

    with ct_tab:
        fill_tab(df_ct,"ct")



    
with fig_col:
    get_figure_col()


