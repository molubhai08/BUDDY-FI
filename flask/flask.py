from flask import Flask, render_template, request
import pandas as pd
import pymongo

class BuddyFinder:
    def fit(self, df):
        self.df = df

    def finder(self, preference):
        if self.df is None:
            raise ValueError("DataFrame is not provided. Please call `fit()` with a DataFrame first.")

        # Filter by gender
        if preference[0] == 'F':
            filtered_df = self.df[self.df['Gender'] == 'F']
        elif preference[0] == 'M':
            filtered_df = self.df[self.df['Gender'] == 'M']
        else:
            filtered_df = self.df

        # Process hobbies
        similar_people_data = []
        user_hobbies = set(preference[1])  # Convert to set for better matching

        for _, row in filtered_df.iterrows():
            row_hobbies = set(row['Hobbies'])  # Convert to set for better matching
            if user_hobbies.intersection(row_hobbies):  # Check for intersection
                similar_people_data.append({
                    'Name': row['Name'],
                    'Age': row['Age'],  # Include Age in the output
                    'Hobbies': ', '.join(row['Hobbies'])  # Join hobbies as string
                })

        similar_people_df = pd.DataFrame(similar_people_data).drop_duplicates()
        return similar_people_df

# MongoDB connection and Flask app initialization (same as before)
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client['Buddyfi']
# collection = db['people']
# data = list(collection.find())

# # Convert the data to a DataFrame
# df = pd.DataFrame(data)
# if '_id' in df.columns:
#     df.drop('_id', axis=1, inplace=True)

# # Initialize the BuddyFinder and fit the DataFrame
# buddy_finder = BuddyFinder()
# buddy_finder.fit(df)

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         gender = request.form['gender']
#         movie = request.form['movie']
#         weekend = request.form['weekend']
#         music = request.form['music']
#         tough_day = request.form['tough_day']
#         communication = request.form['communication']
#         vacation = request.form['vacation']
#         social_setting = request.form['social_setting']

#         preference = [gender, [movie, weekend, music, tough_day, communication, vacation, social_setting]]
#         similar_people = buddy_finder.finder(preference)
#         return render_template('home.html', tables=[similar_people.to_html(classes='data')], titles=similar_people.columns.values)

#     return render_template('home.html', tables=[], titles=[])

if __name__ == '__main__':
    app.run(debug=True)
