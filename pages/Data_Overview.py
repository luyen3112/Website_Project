import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit


st.set_page_config(page_title="Game Analytics",
                page_icon = ":pig:",
                layout="wide")
                
st.title(":mag: Company Data")
st.markdown("##")

@st.cache
def get_data():
    game = pd.read_parquet("EDA/game.parquet",engine = 'fastparquet')
    info = pd.read_parquet("EDA/info.parquet", engine = 'fastparquet')
    match = pd.read_parquet("EDA/match.parquet", engine = 'fastparquet')
    return game, info, match
User_Game, user_info, User_Match = get_data()

option = option_menu(None, ['User_Info', 'User_Game', 'User_Match'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
 


st.text_input("Find Account_id: ",  key = "account", value="xxxxxxxxxxxxxxxx0e3536")


if "account" not in st.session_state:
    st.session_state.key = "account"

if option == "User_Info":
    st.dataframe(user_info.loc[user_info['account_id'] == st.session_state.account], use_container_width=True)
    st.write('Totally {} of {} rows and {} columns'.format(len(user_info.loc[user_info['account_id'] == st.session_state.account]), user_info.shape[0], user_info.shape[1]))

elif option == "User_Game":
    st.dataframe(User_Game.loc[User_Game['account_id'] == st.session_state.account], use_container_width=True)
    st.write('Totally {} of {} rows and {} columns'.format(len(User_Game.loc[User_Game['account_id'] == st.session_state.account]),User_Game.shape[0], User_Game.shape[1]))

elif option == "User_Match":
    st.dataframe(User_Match.loc[User_Match['account_id'] == st.session_state.account], use_container_width=True)
    st.write('Totally {} of {} rows and {} columns'.format(len(User_Match.loc[User_Match['account_id'] == st.session_state.account]), User_Match.shape[0], User_Match.shape[1]))


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
