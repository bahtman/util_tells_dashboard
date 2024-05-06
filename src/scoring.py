import streamlit as st
from cs_bahtml.gospa import calculate_gospa_distance

@st.cache_data
def cluster_scores(df, min_occurence = 2):
    df_filtered = df.groupby('cluster').filter(lambda x: len(x) >= min_occurence)
    df_filtered = df_filtered.set_index('index', drop=True)
    score = df_filtered.groupby("cluster")['alive_players'].apply(calculate_gospa_distance, c = 2000, p = 1, alpha = 2, map="..", euclidean_dist=True).reset_index()
    score.columns = ['cluster', 'util_score']
    score['cluster'] = score['cluster'].astype('int64')  # Convert dtype to int64
    index_filtered = df_filtered.index
    out_df = df_filtered.merge(score, on='cluster', how='left')
    out_df.index = index_filtered
    return out_df