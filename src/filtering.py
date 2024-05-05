import streamlit as st
@st.cache_data
def select_team(df, selected):
    df = df[df.throwerTeam == selected].reset_index()
    df['throwSeconds'] = df['throwSeconds'].apply(int)
    return df

@st.cache_data
def tab_data(df, map, throwerBuy, opponentBuy, round_time):
    df = df[
        (df['map_name'] == map) & 
        df['throwerBuyType'].isin(throwerBuy) & 
        df['opponentBuyType'].isin(opponentBuy) &
        df['throwSeconds'].between(*round_time)].reset_index(drop=True)
    df_t = df.query('throwerSide=="TERRORIST"')
    df_ct = df.query('throwerSide=="CT"')
    return df_t, df_ct