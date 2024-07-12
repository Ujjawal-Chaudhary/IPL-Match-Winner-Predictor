import streamlit as st
import pandas as pd
import pickle



teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings', 
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 
          'Durban', 'Centurion', 'East London', 'Johannesberg', 'Kimberley', 
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 
          'Visakhapatnam', 'Pune', 'Ranchi', 'Raipur', 'Abu Dhabi', 'Sharjah', 
          'Mohali', 'Bengaluru']

st.title("IPL Match Winner Predictor")
model = pickle.load(open('model.pkl', 'rb'))


col1, col2, col3 = st.columns(3)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

with col3:
    city = st.selectbox('Select Host City', sorted(cities))

target = st.number_input('Target')
score = st.number_input('Score')
overs = st.number_input('Over Completed')
wickets = st.number_input('Wicket out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    curr = score / overs
    rr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wicket': [wickets_left],
        'total_runs_x': [target],
        'curr': [curr],
        'rr': [rr]
    })

    result = model.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    
    st.subheader("Prediction Results:")
    st.write(f"{batting_team} Winning Probability: {round(win * 100)}%")
    st.write(f"{bowling_team} Winning Probability: {round(loss * 100)}%")

    st.subheader("Match Stats:")
    st.write(f"Required Run Rate: {round(rr, 2)}")
    st.write(f"Current Run Rate: {round(curr, 2)}")

