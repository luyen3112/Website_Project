from sklearn.metrics import f1_score
from xgboost import XGBClassifier
import streamlit as st
import pandas as pd
from pickle import load

st.set_page_config(page_title="Customer Churn Prediction",
                page_icon = ":pig_nose:",
                layout="wide")

@st.cache
def get_weight():
    poly = load(open('EDA/poly.pkl', 'rb'))
    selector = load(open('EDA/selector.pkl', 'rb'))
    scale = load(open('EDA/scale.pkl', 'rb'))
    return poly, selector, scale

poly, selector, scale = get_weight()

#Loading up the model we created
model = XGBClassifier(random_state = 42)
model.load_model('EDA/xgb_model.json')

def predict(total_battle_time, total_bot, total_lose, total_win,
       total_afk, total_no_afk, total_find_match_failure,
       total_find_match_success, total_online_time, level, total_paid,
       total_frequency_paid, total_date, total_non_rank, total_rank):
    X_test = pd.DataFrame([[total_battle_time, total_bot, total_lose, total_win,
       total_afk, total_no_afk, total_find_match_failure,
       total_find_match_success, total_online_time, level, total_paid,
       total_frequency_paid, total_date, total_non_rank, total_rank]], columns=['total_battle_time', 'total_bot', 'total_lose', 'total_win',
       'total_afk', 'total_no_afk', 'total_find_match_failure',
       'total_find_match_success', 'total_online_time', 'level', 'total_paid',
       'total_frequency_paid', 'total_date', 'total_non_rank', 'total_rank'])
    X_new_test = poly.transform(X_test)
    X_new_test = pd.DataFrame(data = X_new_test, columns = poly.get_feature_names_out(X_test.columns))
    X_selector_test = selector.transform(X_new_test)
    X_test_res = scale.transform(X_selector_test)
    prediction = model.predict(X_test_res)
    return prediction

st.title(":runner: Customer Churn Prediction")
st.markdown("##")

st.image("""https://data-fun.com/wp-content/uploads/2019/11/customer-churn-analytics-1024x662.jpg""", width=620)
st.header('Enter the characteristics of the customer:')

total_battle_time = st.number_input('total_battle_time:', format="%.f")
total_bot  = st.number_input('total_bot:', format="%.f")
total_lose = st.number_input('total_lose:', format="%.f")
total_win = st.number_input('total_win:', format="%.f")
total_afk = st.number_input('total_afk:', format="%.f")
total_no_afk = st.number_input('total_no_afk:', format="%.f")
total_find_match_failure = st.number_input('total_find_match_failure:', format="%.f")
total_find_match_success = st.number_input('total_find_match_success:', format="%.f")
total_online_time = st.number_input('total_online_time:', format="%.f")
level = st.number_input('level:', format="%.f")
total_paid = st.number_input('total_paid:', format="%.f")
total_frequency_paid = st.number_input('total_frequency_paid:', format="%.f")
total_date = st.number_input('total_date:', format="%.f")
total_non_rank  = st.number_input('total_non_rank:', format="%.f")
total_rank  = st.number_input('total_rank:', format="%.f")

def churn(value):
    if value == 1:
        return "churn"
    else:
        return "Not churn"

if st.button('Predict Price'):
    price = predict(total_battle_time, total_bot, total_lose, total_win,
       total_afk, total_no_afk, total_find_match_failure,
       total_find_match_success, total_online_time, level, total_paid,
       total_frequency_paid, total_date, total_non_rank, total_rank)
    st.success(f'Predict customer is {churn(price[0])}')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)