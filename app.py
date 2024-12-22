import streamlit as st
import joblib
import numpy as np

# Load data using joblib
popular_df = joblib.load('popular.pkl')
pt = joblib.load('pt.pkl')
books = joblib.load('books.pkl')
similarity_scores = joblib.load('similarity_scores.pkl')

# Streamlit application
st.set_page_config(page_title="Book Recommender System", layout="wide")


# Function to recommend books
def recommend_books(user_input):
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        recommendations = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            book_title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            book_author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            book_image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
            recommendations.append((book_title, book_author, book_image))

        return recommendations
    except IndexError:
        return None


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Recommend"])

# Home page
if page == "Home":
    st.title("Top 50 Books")
    st.markdown("### Explore the most popular books")
    cols = st.columns(4)

    for i in range(len(popular_df)):
        with cols[i % 4]:
            st.image(popular_df['Image-URL-M'].values[i], width=150)
            st.markdown(f"**{popular_df['Book-Title'].values[i]}**")
            st.markdown(f"Author: {popular_df['Book-Author'].values[i]}")
            st.markdown(f"Votes: {popular_df['Book-Rating'].values[i]}")
            st.markdown(f"Rating: {popular_df['avg_Rating'].values[i]} ⭐")

# Recommend page
elif page == "Recommend":
    st.title("Book Recommender System")
    st.markdown("### Find books similar to your favorite ones")

    user_input = st.text_input("Enter the name of a book:")
    if st.button("Recommend"):
        if user_input.strip():
            recommendations = recommend_books(user_input)
            if recommendations:
                st.markdown("### Recommended Books")
                rec_cols = st.columns(4)
                for idx, rec in enumerate(recommendations):
                    with rec_cols[idx % 4]:
                        st.image(rec[2], width=150)
                        st.markdown(f"**{rec[0]}**")
                        st.markdown(f"Author: {rec[1]}")
            else:
                st.error("No recommendations found. Please check the book name.")
        else:
            st.warning("Please enter a book name.")
