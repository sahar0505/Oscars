import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv('oscars_df.csv')

# Generate word cloud for directors
director_text = ' '.join(data['Directors'].dropna())  # Assuming 'Directors' contains director names

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(director_text)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for Directors in Oscar-nominated Movies')
plt.show()

# Split genres and create a new DataFrame
genre_counts = data['Genres'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
genre_counts.name = 'Genre'
genre_counts = genre_counts.reset_index()

# Merge with original data to consider awards
merged_data = pd.merge(genre_counts, data, left_index=True, right_index=True)

# Filter data for Best Picture nominations and wins
best_picture_data = merged_data[merged_data['Award'].isin(['Winner', 'Nominee'])]

# Count the occurrences of each genre for nominations and wins separately
genre_counts = best_picture_data.groupby(['Genre', 'Award']).size().unstack().reset_index()
genre_counts = genre_counts.fillna(0)  # Fill NaN values with 0

# Create an interactive bar chart using Plotly Express
fig = px.bar(genre_counts, x='Genre', y=['Winner', 'Nominee'],
             labels={'Genre': 'Movie Genre', 'value': 'Count'},
             barmode='group')  # Group bars for Winner and Nominee counts

# Customize layout
fig.update_xaxes(categoryorder='total descending')  # Order bars by total count
fig.update_layout(xaxis_title='Movie Genre', yaxis_title='Count', legend_title='Award')

# Group by Directors and Genres to count occurrences
director_genre_counts = merged_data.groupby(['Directors', 'Genre']).size().reset_index(name='Count')

# Create a Sunburst chart using Plotly Express
sunburst_fig = px.sunburst(director_genre_counts, path=['Directors', 'Genre'], values='Count')

# Update layout
sunburst_fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))

# Save the figures as HTML files
fig.write_html("interactive_chart.html", full_html=False)
sunburst_fig.write_html("directors_genres_tree.html", full_html=False)

# Show the figures
fig.show()
sunburst_fig.show()
