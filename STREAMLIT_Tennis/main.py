import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import base64
import pandas_profiling
from io import BytesIO
from sklearn.linear_model import LinearRegression  # Import your model here

st.set_page_config(page_title="Epic Match Predictor", page_icon=":tennis:", layout="wide", initial_sidebar_state="expanded")

# Function to read and preprocess data
def preprocess_data():
    data = pd.read_csv("Ranking_stats_v2.csv")
    data.columns = data.columns.str.lower().str.replace(" ", "_")
    data = data.drop(columns=["unnamed:_0"])
    data["turned_pro"]= data["turned_pro"].apply(lambda x: str(x)[:4])
    data["year_price_money"] = data["year_price_money"].str.replace('$', '').str.replace(',', '')
    data["year_price_money"] = data["year_price_money"].fillna(0).astype(int)
    data["aces"] = data["aces"].str.replace(',', '').fillna(0).astype(int)
    data["career_price_money"] = data["career_price_money"].str.replace('$', '').str.replace(',', '').fillna(0).astype(int)
    data["double_faults"] = data["double_faults"].str.replace(',', '').fillna(0).astype(int)
    data["first_serves"] = data["first_serves"].str.replace('%', '').fillna(0).astype(int)
    data["first_serve_points_won"] = data["first_serve_points_won"].str.replace('%', '').fillna(0).astype(int)
    data["second_serve_points_won"] = data["second_serve_points_won"].str.replace('%', '').fillna(0).astype(int)
    data["break_points_faced"] = data["break_points_faced"].str.replace(',', '').fillna(0).astype(int)
    data["break_points_saved"] = data["break_points_saved"].str.replace('%', '').fillna(0).astype(int)
    data["service_games_played"] = data["service_games_played"].str.replace(',', '').fillna(0).astype(int)
    data["service_games_won"] = data["service_games_won"].str.replace('%', '').fillna(0).astype(int)
    data["total_service_points_won"] = data["total_service_points_won"].str.replace('%', '').fillna(0).astype(int)
    data["1st_serve_return_points_won"] = data["1st_serve_return_points_won"].str.replace('%', '').fillna(0).astype(int)
    data["2nd_serve_return_points_won"] = data["2nd_serve_return_points_won"].str.replace('%', '').fillna(0).astype(int)
    data["break_points_opportunities"] = data["break_points_opportunities"].str.replace(',', '').fillna(0).astype(int)
    data["break_points_converted"] = data["break_points_converted"].str.replace('%', '').fillna(0).astype(int)
    data["return_games_played"] = data["return_games_played"].str.replace(',', '').fillna(0).astype(int)
    data["return_games_won"] = data["return_games_won"].str.replace('%', '').fillna(0).astype(int)
    data["return_points_won"] = data["return_points_won"].str.replace('%', '').fillna(0).astype(int)
    data["total_points_won"] = data["total_points_won"].str.replace('%', '').fillna(0).astype(int)

    data[['w-year', 'l-year']] = data['w-l_year'].str.split('-', expand=True)
    data[['w-career', 'l-career']] = data['w-l_career'].str.split('-', expand=True)
    data["w-year"] = data["w-year"].fillna(0).astype(int)
    data["l-year"] = data["l-year"].fillna(0).astype(int)
    data["w-career"] = data["w-career"].fillna(0).astype(int)
    data["l-career"] = data["l-career"].fillna(0).astype(int)
    data['w/l_year_final'] = np.where(data['l-year'] != 0, data['w-year'] / data['l-year'], 0)
    data['w/l_career_final'] = np.where(data['l-career'] != 0, data['w-career'] / data['l-career'], 0)
    data['w/l_year_final']= data['w/l_year_final'].astype(int)
    data['w/l_career_final']= data['w/l_career_final'].astype(int)
    data["atp_points"] = data["atp_points"].str.replace(',', '').fillna(0).astype(int)
    data["w/l_year_final"]= data["w/l_year_final"].fillna(0)
    data["w/l_career_final"]= data["w/l_career_final"].fillna(0)
    return data

# Function to train your model
def train_model(data):
    X = data[['ages', 'title_year', 'title_career', 'year_price_money',
           'career_price_money', 'aces', 'double_faults', 'first_serves',
           'first_serve_points_won', 'second_serve_points_won',
           'break_points_faced', 'break_points_saved', 'service_games_played',
           'service_games_won', 'total_service_points_won',
           '1st_serve_return_points_won', '2nd_serve_return_points_won',
           'break_points_opportunities', 'break_points_converted',
           'return_games_played', 'return_games_won', 'return_points_won',
           'total_points_won', 'second_serve_points_won', 'w/l_year_final', 'w/l_career_final']]
    y = data["atp_points"]
    
    model = LinearRegression()  # Replace this with your model
    model.fit(X, y)
    return model

features=['ages', 'title_year', 'title_career', 'year_price_money',
       'career_price_money', 'aces', 'double_faults', 'first_serves',
       'first_serve_points_won', 'second_serve_points_won',
       'break_points_faced', 'break_points_saved', 'service_games_played',
       'service_games_won', 'total_service_points_won',
       '1st_serve_return_points_won', '2nd_serve_return_points_won',
       'break_points_opportunities', 'break_points_converted',
       'return_games_played', 'return_games_won', 'return_points_won',
       'total_points_won', 'second_serve_points_won', 'w/l_year_final', 'w/l_career_final']
# Function to predict the winner
def predict_winner(model, data, name1, name2):
    try:
        name1 = name1.strip().lower()
        name2 = name2.strip().lower()

        # Use case-insensitive matching and remove leading/trailing whitespaces
        player1_data = data[data['players'].str.strip().str.lower() == name1][features]
        player2_data = data[data['players'].str.strip().str.lower() == name2][features]

        if player1_data.empty or player2_data.empty:
            return "Invalid player names. Try again."

        points_player1 = model.predict(player1_data)
        points_player2 = model.predict(player2_data)

        if points_player1 > points_player2:
            result_message = f"The winner of this epic match is {name1}"
        elif points_player2 > points_player1:
            result_message = f"The winner of this epic match is {name2}"
        else:
            result_message = "It's a tie! Both players have equal chances."
        return result_message
    except:
        return "An error occurred. Please try again."



def get_player_data(data, name):
    name = name.strip().lower()
    player_data = data[data['players'].str.strip().str.lower() == name][["players", "w/l_year_final", "w/l_career_final", "aces", "w-year", "l-year", "year_price_money"]]
    return player_data

# Streamlit app code
def main():
    data = preprocess_data()
    model = train_model(data)

    # Load and display the background image
    background_image = Image.open("court.jpeg")
    st.image(background_image, use_column_width=True)

    # Emoji and titles
    emoji_player1 = Image.open("player1_emoji.png").resize((300, 300))
    emoji_player2 = Image.open("player2_emoji.png").resize((300, 300))
    vs_image = Image.open("vs_image.png").resize((100, 100))

    # Convert images to data URLs
    def img_to_data_url(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    emoji_player1_data_url = img_to_data_url(emoji_player1)
    emoji_player2_data_url = img_to_data_url(emoji_player2)
    vs_image_data_url = img_to_data_url(vs_image)

    # Container for the text and images
    st.markdown(
    """
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -125%); text-align: center;">
        <h1 style="color: white; font-size: 70px; font-weight: bold;">EPIC MATCH PREDICTOR</h1>
        <p style="color: white; font-size: 50px;">CHOOSE YOUR PLAYERS</p>
        <div style="display: flex; align-items: center; justify-content: center;">
            <div style="margin-right: 30px;">
                <img src="{emoji_player1_data_url}" alt="Player 1" style="width: 400px; height: 400px;">
                <p style="color: white; font-size: 20px;">Player 1</p>
            </div>
            <div>
                <img src="{vs_image_data_url}" alt="VS" style="width: 200px; height: 100px;">
            </div>
            <div style="margin-left: 30px;">
                <img src="{emoji_player2_data_url}" alt="Player 2" style="width: 400px; height: 400px;">
                <p style="color: white; font-size: 20px;">Player 2</p>
            </div>
        </div>
    </div>
    """.format(
        emoji_player1_data_url=emoji_player1_data_url,
        emoji_player2_data_url=emoji_player2_data_url,
        vs_image_data_url=vs_image_data_url,
    ),
    unsafe_allow_html=True,)
 

    # Data input
    st.title("Enter Player Names")
    name1 = st.text_input("Player 1")
    name2 = st.text_input("Player 2")

    # Prediction button
    if st.button("Predict Winner"):
        if name1 and name2:
            result = predict_winner(model, data, name1, name2)
            st.write(result)
        else:
            st.write("Please enter both player names to predict the winner.")
    
    if name1 and name2:
        st.title("Player Stat Comparisons")
        player1_data = get_player_data(data, name1)
        player2_data = get_player_data(data, name2)

        st.write(f"Comparing stats for \033[1m{name1}\033[0m and \033[1m{name2}\033[0m:")
        st.dataframe(player1_data)
        st.dataframe(player2_data)

    # Display five random samples of the table
    st.title("Random Samples from the Table")
    random_samples = data.sample(5)
    st.dataframe(random_samples)

    

if __name__ == "__main__":
    main()
# ... (previous code remains unchanged)






