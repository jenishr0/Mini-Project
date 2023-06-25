from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_input_data():
    brand = request.form.get('brand')
    price = float(request.form.get('price'))
    camera = float(request.form.get('camera'))
    battery = int(request.form.get('battery'))
    processor = request.form.get('processor')
    ram = int(request.form.get('ram'))
    ratings = float(request.form.get('ratings'))

    df = pd.read_csv("LT15K.csv")

    df.Prices = df.Prices.astype(float)
    df.Camera = df.Camera.astype(float)
    df.Battery = df.Battery.astype(int)
    df.RAM = df.RAM.astype(int)
    df.Ratings = df.Ratings.astype(float)

    df = df.loc[df['Brand'] == brand]
    df = df.loc[df['Prices'] <= price]
    df = df.loc[df['Ratings'] >= ratings]
    df = df.loc[df['RAM'] >= ram]
    df = df.loc[df['Battery'] >= battery]
    df = df.loc[df['Camera'] >= camera]
    df = df.loc[df["Processor"].str.contains(processor, case=False)]
    return df


def get_recommended_phones(df, input_data):
    phone_data = df['Brand'] + ' ' + df['Model']
    input_phone_data = input_data['Brand'].iloc[0] + ' ' + \
        input_data['Model'].iloc[0]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform([input_phone_data] + list(phone_data))
    print([input_phone_data] + list(phone_data))
    sim_scores = cosine_similarity(count_matrix)
    sim_scores = sim_scores[0][1:]
    df = df.copy()
    df['Score'] = sim_scores
    df = df.sort_values('Score', ascending=False)
    return df[['Brand', 'Model', 'Score']]


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    df = pd.read_csv("LT15K.csv")
    input_data = get_input_data()

    if input_data.empty:
        return "Empty"

    recommended_phones = get_recommended_phones(df, input_data)
    return render_template('Recommend.html', table=recommended_phones.to_html())


if __name__ == '__main__':
    app.run(debug=True)
