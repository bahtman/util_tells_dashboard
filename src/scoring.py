import streamlit as st
from cs_bahtml.gospa import calculate_gospa_distance

@st.cache_data
def cluster_scores(df, min_occurence = 2):
    df_filtered = df.groupby('cluster').filter(lambda x: len(x) >= min_occurence)
    score = df_filtered.groupby("cluster")['alive_players'].apply(calculate_gospa_distance, c = 2000, p = 1, alpha = 2, map="..", euclidean_dist=True).reset_index()
    score.columns = ['cluster', 'util_score']
    score['cluster'] = score['cluster'].astype('int64')  # Convert dtype to int64
    out_df = df_filtered.merge(score, on='cluster', how='left')
    return out_df
    groups = out_df.groupby("cluster").groups
    group_list = [(out_df.loc[index,:],out_df.loc[index[0],"util_score"]) for index in groups.values()]
    return [sort[0] for sort in sorted(group_list, key = lambda tup: tup[1])]