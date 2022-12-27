import streamlit as st
import pandas as pd
import datetime
import altair as alt
import numpy as np
import dask.dataframe as dd
from google.cloud import storage

st.set_page_config(page_title="Home Page",
                page_icon = ":pig_nose:",
                layout="wide",
                initial_sidebar_state='expanded')


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title(":bar_chart: Company Dashboard")
st.markdown("##")

@st.cache
def get_data():
    game = pd.read_parquet("EDA/game.parquet",engine = 'fastparquet')
    info = pd.read_parquet("EDA/info.parquet", engine = 'fastparquet')
    match = pd.read_parquet("EDA/match.parquet", engine = 'fastparquet')
    data_loc = pd.read_parquet("EDA/a.parquet",engine = 'fastparquet')
    data_loc_1 = pd.read_parquet("EDA/c.parquet",engine = 'fastparquet')
    return game, info, match, data_loc, data_loc_1

game, info, match, data_loc, data_loc_1 = get_data()

game['order_time'] =  pd.to_datetime(game['order_time'] , format='%Y-%m-%d')
info['date'] =  pd.to_datetime(info['date'] , format='%Y-%m-%d')
match['date'] =  pd.to_datetime(match['date'] , format='%Y-%m-%d')


#number of user_info in this month
st.sidebar.header("Please Filter Here:")

st.sidebar.subheader('Show in Number or Percentage')
per = st.sidebar.selectbox("Number or Percentage",
    ('Number', 'Percentage'))
st.sidebar.subheader('Filter for Count number of User, Match, Game')
date_select = st.sidebar.date_input("When\'s your birthday",
    datetime.date(2022, 8, 7))
st.sidebar.subheader('Filter for Count number of Churn')
option = st.sidebar.selectbox(
    'Select by Day or Month',
    ('All Time', 'Week'))

# info['date'].dt.day == int(str(date_select).split("-")[2]) = info['date'].dt.day == int(str(date_select).split("-")[2])
# info.loc[info['date'].dt.day == int(str(date_select).split("-")[2])].account_id.nunique() = info.loc[info['date'].dt.day == int(str(date_select).split("-")[2])].account_id.nunique()
# game['order_time'].dt.day == int(str(date_select).split("-")[2]) = game['order_time'].dt.day == int(str(date_select).split("-")[2])
# match['date'].dt.day == int(str(date_select).split("-")[2])  = match['date'].dt.day == int(str(date_select).split("-")[2]) 


b1, b2, b3= st.columns(3)
if per == "Number":
    b1.metric("Number of User this day", info.loc[info['date'].dt.day == int(str(date_select).split("-")[2])].account_id.nunique(), 
    str(info.loc[info['date'].dt.day == int(str(date_select).split("-")[2])].account_id.nunique()- info.loc[info['date'].dt.day == int(str(date_select).split("-")[2]) - 1].account_id.nunique()) + " than the day before")
    b2.metric("Number of Match this day", len(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]),
    str(len(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) ]) - len(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])-1])) + " than the day before")
    b3.metric("Number of Finding Match this day", len(match.loc[match['date'].dt.day == int(str(date_select).split("-")[2]) ]),
    str(len(match.loc[match['date'].dt.day == int(str(date_select).split("-")[2])  ]) - len(match.loc[match['date'].dt.day == int(str(date_select).split("-")[2])-1])) + " than the day before")
if per == "Percentage":
    b1.metric("Number of User this day", info.loc[info['date'].dt.day == int(str(date_select).split("-")[2])].account_id.nunique(), 
    str(round(np.float64(info.loc[info['date'].dt.day == int(str(date_select).split("-")[2])].account_id.nunique()- info.loc[info['date'].dt.day == int(str(date_select).split("-")[2]) - 1].account_id.nunique())/info.loc[info['date'].dt.day == int(str(date_select).split("-")[2]) - 1].account_id.nunique(),2)*100) + "% than the day before")
    b2.metric("Number of Match this day", len(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]),
    str(round(np.float64(len(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) ]) - len(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])-1]))/info.loc[info['date'].dt.day == int(str(date_select).split("-")[2]) - 1].account_id.nunique(),2)*100) + "% than the day before")
    b3.metric("Number of Finding Match this day", len(match.loc[match['date'].dt.day == int(str(date_select).split("-")[2]) ]),
    str(round(np.float64(len(match.loc[match['date'].dt.day == int(str(date_select).split("-")[2])  ]) - len(match.loc[match['date'].dt.day == int(str(date_select).split("-")[2]) -1]))/info.loc[info['date'].dt.day == int(str(date_select).split("-")[2]) - 1].account_id.nunique(),2)*100) + "% than the day before")


ct = game.mode_game.value_counts()
b1, b2, b3, b4 = st.columns(4)
if per == "Number":
    b1.metric("Dau Xep Hang", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0],
    str(int(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0]))+ " than the day before")
    b2.metric("Dau Thuong 5v5", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0],
    str(int(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0]))+ " than the day before")
    b3.metric("Dau Giai Tri", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0],
    str(int(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0]))+ " than the day before")
    b4.metric("Cac Che Do Choi Khac", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0],
    str(int(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0]))+ " than the day before")
if per == "Percentage":
    b1.metric("Dau Xep Hang", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0],
    str(round(np.float64(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0])/game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_xep_hang']][0] *100,2)) + " % than the day before")
    b2.metric("Dau Thuong 5v5", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0],
    str(round(np.float64(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0])/game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_thuong_5v5']][0] *100,2)) + " % than the day before")
    b3.metric("Dau Giai Tri", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0],
    str(round(np.float64(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0])/game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['dau_giai_tri']][0] *100,2)) + " % than the day before")
    b4.metric("Cac Che Do Choi Khac", game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0],
    str(round(np.float64(game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2])]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0]- game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0])/game.loc[game['order_time'].dt.day == int(str(date_select).split("-")[2]) - 1]['mode_game'].value_counts().reindex(
    game.mode_game.unique(), fill_value=0).loc[['cac_che_do_choi_khac']][0] *100,2)) + " % than the day before")



colors = ['#7fc97f','#beaed4']


c1, c2 = st.columns((7,3))
with c1:
    # input_dat = st.date_input(
    # "Select your day or month you want to find: ",
    # datetime.date(2022, 8, 11))
    if option == 'All Time':
        df = game.groupby(['order_time', 'churn_flag']).size().reset_index(name="Count")
        p = alt.Chart(df,title='Trending of Churn OverTime').mark_area(opacity=0.5).encode(
        x=alt.X('order_time', axis=alt.Axis(title='')),
        y=alt.Y('Count', axis=alt.Axis(), stack=None),
        color='churn_flag').properties(
        height=355
        ).configure_range(
    category=alt.RangeScheme(colors))
        st.altair_chart(p, use_container_width=True)

    if option == 'Week':
        info['day'] = info['date'].dt.day_name()
        df = info.groupby(['day', 'churn_flag']).size().reset_index(name="Count")
        p = alt.Chart(df,title='Trending of Churn OverWeek').mark_area(opacity=0.5).encode(
        x=alt.X('day', axis=alt.Axis(title='')),
        y=alt.Y('Count', axis=alt.Axis(), stack=None),
        color='churn_flag').properties(
        height=355
        ).configure_range(
    category=alt.RangeScheme(colors)
)
        st.altair_chart(p, use_container_width=True)
#The fake nonsens table:

domain = ['dau_thuong', 'cac_che_do_choi_khac', 'dau_xep_hang', 'dau_giai_tri'] 
range_ = ['#405069',  '#213d69', '#4477c7', '#1d4c96']

domain = [ 'Not Churn', 'Churn'] 
range_ = [ '#4477c7', '#1d4c96']
with c2:
    pert = pd.DataFrame(info['churn_flag'].value_counts())
    pert = pert.reset_index()
    pert['pere'] = round(pert['churn_flag']/sum(pert['churn_flag']) * 100,2)
    pert = pert.rename(columns={'index': 'churn_flag', 'churn_flag': 'count', 'pere': 'percentage'})
    base = alt.Chart(pert, title='Percentage of Churn Flag').mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="percentage", type="quantitative", stack=True),
    color=alt.Color(field="churn_flag",scale=alt.Scale(scheme='purples'), type="nominal", legend=alt.Legend(title="Churn Flag"))).mark_arc(innerRadius=50)
    pie = base.mark_arc(innerRadius=50)
    # text = base.mark_text(radius=165, size=13).encode(text="percentage:N")
    st.altair_chart(pie, use_container_width=True)

    # pert = pd.DataFrame(game['mode_game'].value_counts())
    # pert = pert.reset_index()
    # pert['pere'] = round(pert['mode_game']/sum(pert['mode_game']) * 100,2)
    # pert = pert.rename(columns={'index': 'mode_game', 'mode_game': 'count', 'pere': 'percentage'})
    # base = alt.Chart(pert, title='Percentage of Mode Game').mark_arc(innerRadius=50).encode(
    # theta=alt.Theta(field="percentage", type="quantitative", stack=True),
    # color=alt.Color(field="mode_game",scale=alt.Scale(scheme='purples'), type="nominal", legend=alt.Legend(title="Game Mode",orient="bottom"))).mark_arc(innerRadius=50)
    # pie = base.mark_arc(innerRadius=30)
    # text = base.mark_text(radius=147, size=13).encode(text="percentage:N")
    # st.altair_chart(pie + text, use_container_width=True)

d1, d2 = st.columns(2)
with d1:
    if option == 'All Time':
        base = alt.Chart(data_loc, title='A mount of Payment and Online Time').encode(
            alt.X('date', axis=alt.Axis(title='', titleFontSize = 15)))
        area = base.mark_area(opacity=0.3, color='#4c77a4').encode(alt.Y('online_time:Q',
                    axis=alt.Axis(title='Amout of Online Time', titleColor='#4c77a4',titleFontSize = 20)))
        line = base.mark_line(stroke='#cccfc8', interpolate='monotone').encode(
            alt.Y('paid_amount:Q',
                axis=alt.Axis(title='Amount of Paying', titleColor='#cccfc8',titleFontSize = 20)))
        st.altair_chart((area + line).resolve_scale(
            y = 'independent'), use_container_width=True)

    if option == 'Week':
        data_loc = data_loc.groupby(['Day'])[['paid_amount', 'online_time']].apply('sum').reset_index()
        base = alt.Chart(data_loc, title='A mount of Payment and Online Time').encode(
            alt.X('Day', axis=alt.Axis(title='', titleFontSize = 15)))
        area = base.mark_area(opacity=0.3, color='#4c77a4').encode(alt.Y('online_time',
                    axis=alt.Axis(title='Amout of Online Time', titleColor='#4c77a4',titleFontSize = 20)))
        line = base.mark_line(stroke='#cccfc8', interpolate='monotone').encode(
            alt.Y('paid_amount',
                axis=alt.Axis(title='Amount of Paying', titleColor='#cccfc8',titleFontSize = 20)))
        st.altair_chart((area + line).resolve_scale(
            y = 'independent'), use_container_width=True)
with d2:
    if option == 'All Time':
        base = alt.Chart(data_loc_1,title='A mount of Time').encode(
        alt.X('date', axis=alt.Axis(title='', titleFontSize = 15)))
        area = base.mark_area(opacity=0.3, color='#783d76').encode(alt.Y('Total_Finding_Match_Time',
            axis=alt.Axis(title='Amout of Finding Match Time', titleColor='#783d76',titleFontSize = 20)))
        line = base.mark_line(stroke='#e3c5e2', interpolate='monotone').encode(alt.Y('Total_Battle_Time',
            axis=alt.Axis(title='Amount of Battle Time', titleColor='#e3c5e2',titleFontSize = 20)))
        st.altair_chart((area + line).resolve_scale(
            y = 'independent'), use_container_width=True)
    if option == 'Week':
        data_loc_1 = data_loc_1.groupby(['Day'])[['Total_Battle_Time', 'Total_Finding_Match_Time']].apply('sum').reset_index()
        base = alt.Chart(data_loc_1,title='A mount of Time').encode(
        alt.X('Day', axis=alt.Axis(title='', titleFontSize = 15)))
        area = base.mark_area(opacity=0.3, color='#783d76').encode(alt.Y('Total_Finding_Match_Time',
            axis=alt.Axis(title='Amout of Finding Match Time', titleColor='#783d76',titleFontSize = 20)))
        line = base.mark_line(stroke='#e3c5e2', interpolate='monotone').encode(alt.Y('Total_Battle_Time',
            axis=alt.Axis(title='Amount of Battle Time', titleColor='#e3c5e2',titleFontSize = 20)))
        st.altair_chart((area + line).resolve_scale(
            y = 'independent'), use_container_width=True)

e1,e2 = st.columns((7,3))
pert = pd.DataFrame(game['mode_game'].value_counts())
pert = pert.reset_index()
pert['pere'] = round(pert['mode_game']/sum(pert['mode_game']),2)
with e1:
    base = alt.Chart(pert, title = 'Percentage of Mode Game').mark_bar().encode(
    alt.X('pere:Q', axis=alt.Axis(format='.0%'), title = ''),
    alt.Y('index:N', title = ''),
    color = alt.Color(field="index",scale=alt.Scale(scheme='purples'))).properties(
    height=300)
    bar = base.mark_bar()
    st.altair_chart(bar, use_container_width=True)

with e2:
    pert = pd.DataFrame(match['status'].value_counts())
    pert = pert.reset_index()
    pert['pere'] = round(pert['status']/sum(pert['status']) * 100,2)
    pert = pert.rename(columns={'index': 'status', 'status': 'count', 'pere': 'percentage'})
    base = alt.Chart(pert, title='Percentage of Status').mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="percentage", type="quantitative", stack=True),
    color=alt.Color(field="status",scale=alt.Scale(scheme='purples'), type="nominal", legend=alt.Legend(title="Churn Flag",orient="bottom"))).mark_arc(innerRadius=50)
    pie = base.mark_arc(innerRadius=100)
    # text = base.mark_text(radius=165, size=13).encode(text="percentage:N")
    st.altair_chart(pie, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)