'''
Update: 10/19/2023
App is operating with the synthetic data
    waiting for excel data of farms in DMV
Needs styling and modified UI
'''
from googlesearch import search
from flask import Flask, render_template, request
import pandas as pd

# Function to perform the search and return results
def search_agricultural_news_maryland():
    query = "Agricultural news Maryland"
    num_results = 10

    try:
        search_results = list(search(query, num=num_results, stop=num_results))
        results_list = []  # Create a list to store all the results

        for i, result in enumerate(search_results, start=1):
            result_string = result
            results_list.append(result_string)  # Append each result to the list
            print(result_string)  # Print the result in the loop

        return results_list  # Return the list of all results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def search_agricultural_facts_maryland(query):
        num_results = 10
        try:
            # Perform the Google search and return the results
            search_results = list(search(query, num=num_results, stop=num_results))
            results_list = search_results
            return results_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

farm_df = pd.read_excel("farm_data.xlsx")
farm_df['Zip Code'] = farm_df['Zip Code'].astype('Int64')
farm_df['Zip Code'] = farm_df['Zip Code'].astype(str)
farm_df = farm_df.drop(columns=['City'])
farm_df = farm_df.drop(columns=['State'])


crop_file = "agricultural_data.xlsx"
crop_df = pd.read_excel(crop_file)
# Reset the row indexes
crop_df = crop_df.reset_index(drop=True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/farm_locator1')
def farm_locator():
    return render_template('farm_locator1.html', farm_df=farm_df)

@app.route('/search_results', methods=['POST'])
def search_results():
    search_query = request.form.get('search')
    # Extract the city from the search query
    city = search_query.split(',')[0].strip()
    # Use pandas to filter the DataFrame based on the city
    results = farm_df[farm_df['City, State'].str.contains(city, case=False)]
    return render_template('search_results.html', results=results)

# New route for Crop Locator
# @app.route('/crop_locator', methods=['GET', 'POST'])
# def crop_locator():
#     # Get the list of unique counties from the DataFrame
#     counties = crop_df['County'].unique()

#     selected_county = request.form.get('county') if request.method == 'POST' else 'All Counties'

#     if selected_county == 'All Counties':
#         filtered_df = crop_df
#     else:
#         filtered_df = crop_df[crop_df['County'] == selected_county]

#     return render_template('crop_locator.html', crop_df=filtered_df, counties=counties, selected_county=selected_county)

# Define a route for the search news page
@app.route('/agricultural_news')
def agricultural_news():
    search_results = search_agricultural_news_maryland()
    return render_template('agricultural_news.html', search_results=search_results)

@app.route('/agricultural_facts', methods=['GET', 'POST'])
def agricultural_facts():
    questions = [
    "What are the current agricultural zoning regulations in Maryland?",
    "How can I obtain a farming permit in Maryland?",
    "Are there specific pesticide regulations for Maryland farmers?",
    "What are the water usage restrictions for farming in Maryland?",
    "What sustainable farming practices are recommended in Maryland?",
    "How can I implement eco-friendly agriculture in Maryland?",
    "Are there incentives for adopting sustainable farming methods in Maryland?",
    "Tell me about Maryland's initiatives for soil conservation in farming.",
    "Where can I learn about organic farming techniques in Maryland?",
    "What grants are available for Maryland farmers to improve their farms?",
    "How can I apply for agricultural subsidies in Maryland?",
    "Tell me about Maryland's programs to support small-scale farmers.",
    "What financial assistance is provided to promote farm sustainability in Maryland?",
    "Are there grants for Maryland farmers to invest in new technologies?",
    "Where can I find a list of Maryland farmers' markets and their hours of operation?",
    "Which restaurants in Maryland offer farm-to-table dining experiences?",
    "Tell me about the benefits of buying from local farms in Maryland.",
    "What are some popular seasonal products available at Maryland farmers' markets?",
    "Are there any food festivals or events showcasing local Maryland produce?",
    "What agricultural education programs are offered in Maryland?",
    "How can I access extension services for farm-related information in Maryland?",
    "Tell me about workshops and training opportunities for Maryland farmers.",
    "Where can I find resources for pest management in Maryland agriculture?",
    "Are there research centers that provide support to Maryland farmers?"
    ]

    if request.method == 'POST':
        selected_question = request.form.get('query')

        if selected_question:
            # Call the search_agricultural_facts_maryland function with the selected question
            search_results = search_agricultural_facts_maryland(selected_question)

            return render_template('agriculture_facts.html', search_results=search_results)

    return render_template('agriculture_facts.html', questions=questions)


if __name__ == '__main__':
    app.run()
