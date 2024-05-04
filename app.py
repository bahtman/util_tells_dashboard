import streamlit as st
from math import floor
from src.data import load_data, set_map
from src.scoring import cluster_scores
from src.filtering import select_team, tab_data


st.set_page_config(layout="wide")


def clear_map():
    del st.session_state.fig


def get_cluster_overview(df):
    score_df = cluster_scores(df, min_occurence = 2)
    grouped_df = score_df.groupby("cluster")
    group_list = [(cluster, group ,group.util_score.min()) for cluster, group in grouped_df]
    groups = [(sort[0], sort[1]) for sort in sorted(group_list, key = lambda tup: tup[2])]
    for cluster, group in groups[0:10]:
        n_row = len(group)
        score = int(group['util_score'].iloc[0])
        util_type = group['grenade_type'].iloc[0]

        

        with st.expander(f"Dissimilarity score: {score} - {n_row} occurences - {util_type}"):
            for idx, row in group.iterrows():
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
                cc[0].dataframe(row[["throwerName", "throwSeconds", "opponentTeam"]].to_frame().T, hide_index=True, use_container_width=True)
                #



                cc[-1].write("")
                cc[-1].button(":punch:", key = f"{cluster}:{idx}", on_click=set_map, args=(row['map_name'],row))



    
            



st.title('Utility tell tool')
df = load_data()
filter1, filter2 = st.columns(2)
buytypes = ["eco","force","full"]
with filter1:
    selected = st.selectbox("Select team",df.throwerTeam.unique())
    df = select_team(df, selected)
    map_pick = st.selectbox("Select map",df.map_name.unique(), on_change=clear_map)
with filter2:
    throwerBuy = st.multiselect(f"Select Buy Type of {selected}", buytypes, default = buytypes)
    opponentBuy = st.multiselect(f"Select Buy Type of opponent", buytypes, default = buytypes)

if 'fig' not in st.session_state:
    set_map(map_pick)

df_t, df_ct = tab_data(df, map_pick, throwerBuy, opponentBuy)

cluster_col, fig_col =st.columns(2)
with fig_col:
    st.image(st.session_state.fig)

with cluster_col:
    t_tab, ct_tab = st.tabs(["T side", "CT side"])
    with t_tab:
        get_cluster_overview(df_t)

    with ct_tab:
        get_cluster_overview(df_ct)



    
