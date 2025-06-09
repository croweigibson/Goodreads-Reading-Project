import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set style for better looking plots
plt.style.use('default')
# Custom blue-grey palette
blue_grey_palette = ['#4472C4', '#70AD47', '#FFC000', '#C55A5A', '#264478', '#997300', '#843C0C', '#5B9BD5', '#A5A5A5', '#595959']
sns.set_palette(blue_grey_palette)

# Page config
st.set_page_config(
    page_title="📚 Goodreads Insights Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_data.csv')
    # Convert date_added column (yy-mm-dd format)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['month_name'] = df['date_added'].dt.strftime('%B')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Time period filter
time_filter = st.sidebar.radio(
    "📅 Time Period",
    ["All Time", "By Year", "By Month"],
    help="Filter data by time period"
)

year_filter = None
month_filter = None

if time_filter == "By Year":
    years = sorted(df['year_added'].dropna().unique())
    year_filter = st.sidebar.selectbox("Select Year", years)
    df_filtered = df[df['year_added'] == year_filter]
elif time_filter == "By Month":
    years = sorted(df['year_added'].dropna().unique())
    year_filter = st.sidebar.selectbox("Select Year", years)
    months = sorted(df[df['year_added'] == year_filter]['month_added'].dropna().unique())
    month_names = df[df['year_added'] == year_filter]['month_name'].dropna().unique()
    month_filter = st.sidebar.selectbox("Select Month", months)
    df_filtered = df[(df['year_added'] == year_filter) & (df['month_added'] == month_filter)]
else:
    df_filtered = df

# Additional filters
genres = ['All'] + list(df_filtered['genre'].unique())
selected_genre = st.sidebar.selectbox("📖 Genre Filter", genres)
if selected_genre != 'All':
    df_filtered = df_filtered[df_filtered['genre'] == selected_genre]

# Main dashboard
st.title("📚 Goodreads Insights Dashboard")
st.markdown("---")

# Enhanced KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_books = len(df_filtered)
    st.metric("📚 Total Books Read", total_books)

with col2:
    total_pages = df_filtered['num_of_pages'].sum()
    st.metric("📄 Total Pages Read", f"{total_pages:,}")

with col3:
    five_star_books = len(df_filtered[df_filtered['rating_num'] == 5])
    five_star_pct = (five_star_books / total_books * 100) if total_books > 0 else 0
    st.metric("🌟 5-Star Books", f"{five_star_books} ({five_star_pct:.1f}%)")

with col4:
    below_three_books = len(df_filtered[df_filtered['rating_num'] < 3])
    below_three_pct = (below_three_books / total_books * 100) if total_books > 0 else 0
    st.metric("📉 Books Below 3⭐", f"{below_three_books} ({below_three_pct:.1f}%)")

st.markdown("---")

# Interactive Analysis Section
st.subheader("🔍 Interactive Analysis")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    st.write("**📊 Quick Stats**")
    if st.button("🏆 Most Read Genre"):
        most_read = df_filtered['genre'].value_counts().head(1)
        st.success(f"Most Read: {most_read.index[0]} ({most_read.values[0]} books)")
    
    if st.button("📉 Least Read Genre"):
        least_read = df_filtered['genre'].value_counts().tail(1)
        st.info(f"Least Read: {least_read.index[0]} ({least_read.values[0]} books)")

with analysis_col2:
    st.write("**⭐ Rating Insights**")
    if st.button("🌟 Highest Rated Book (My Rating)"):
        highest = df_filtered.loc[df_filtered['rating_num'].idxmax()]
        st.success(f"📖 {highest['title']}")
        st.write(f"✍️ by {highest['author']}")
        st.write(f"⭐ My Rating: {highest['rating_num']} | Community: {highest['avg_rating']}")
    
    if st.button("📉 Lowest Rated Book (My Rating)"):
        lowest = df_filtered.loc[df_filtered['rating_num'].idxmin()]
        st.error(f"📖 {lowest['title']}")
        st.write(f"✍️ by {lowest['author']}")
        st.write(f"⭐ My Rating: {lowest['rating_num']} | Community: {lowest['avg_rating']}")

# Author Insights
author_col1, author_col2 = st.columns(2)

with author_col1:
    st.write("**✍️ Author Insights**")
    if st.button("📚 Most Read Author"):
        most_read_author = df_filtered['author'].value_counts().head(1)
        st.success(f"Most Read: {most_read_author.index[0]} ({most_read_author.values[0]} books)")
    
    if st.button("🏆 Author with Highest Avg Rating (2+ books)"):
        author_ratings = df_filtered.groupby('author').agg({
            'rating_num': ['mean', 'count']
        }).round(1)
        author_ratings.columns = ['avg_rating', 'book_count']
        qualified_authors = author_ratings[author_ratings['book_count'] >= 2]
        if not qualified_authors.empty:
            best_author = qualified_authors.loc[qualified_authors['avg_rating'].idxmax()]
            st.success(f"Best Author: {qualified_authors['avg_rating'].idxmax()}")
            st.write(f"⭐ Avg Rating: {best_author['avg_rating']:.1f} ({int(best_author['book_count'])} books)")
        else:
            st.info("No authors with 2+ books found")

with author_col2:
    st.write("**📖 Page Insights**")
    if st.button("📚 Longest Book"):
        longest = df_filtered.loc[df_filtered['num_of_pages'].idxmax()]
        st.success(f"📖 {longest['title']} ({longest['num_of_pages']} pages)")
        st.write(f"✍️ by {longest['author']}")

    if st.button("📖 Shortest Book"):
        shortest = df_filtered.loc[df_filtered['num_of_pages'].idxmin()]
        st.info(f"📖 {shortest['title']} ({shortest['num_of_pages']} pages)")
        st.write(f"✍️ by {shortest['author']}")

st.markdown("---")

# Genre Deep Dive Section
st.subheader("🎭 Genre Deep Dive")
selected_genre_analysis = st.selectbox("Select Genre for Detailed Analysis", 
                                     ['All'] + list(df_filtered['genre'].unique()))

if selected_genre_analysis != 'All':
    genre_data = df_filtered[df_filtered['genre'] == selected_genre_analysis]
    
    st.write(f"**Analysis for {selected_genre_analysis} ({len(genre_data)} books)**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not genre_data.empty and genre_data['num_of_pages'].notna().any():
            longest = genre_data.loc[genre_data['num_of_pages'].idxmax()]
            st.metric("📚 Longest", f"{longest['num_of_pages']:.0f} pages")
            st.caption(longest['title'])
        else:
            st.metric("📚 Longest", "No data")
    
    with col2:
        if not genre_data.empty and genre_data['num_of_pages'].notna().any():
            shortest = genre_data.loc[genre_data['num_of_pages'].idxmin()]
            st.metric("📖 Shortest", f"{shortest['num_of_pages']:.0f} pages")
            st.caption(shortest['title'])
        else:
            st.metric("📖 Shortest", "No data")
    
    with col3:
        if not genre_data.empty and genre_data['rating_num'].notna().any():
            highest_rated = genre_data.loc[genre_data['rating_num'].idxmax()]
            st.metric("🌟 Highest Rated", f"{highest_rated['rating_num']}⭐")
            st.caption(highest_rated['title'])
        else:
            st.metric("🌟 Highest Rated", "No ratings")
    
    with col4:
        if not genre_data.empty and genre_data['rating_num'].notna().any():
            avg_rating = genre_data['rating_num'].mean()
            st.metric("📊 Average Rating", f"{avg_rating:.1f}⭐")
            total_pages = genre_data['num_of_pages'].sum()
            st.caption(f"{total_pages:,} total pages")
        else:
            st.metric("📊 Average Rating", "No ratings")
            if not genre_data.empty:
                total_pages = genre_data['num_of_pages'].sum()
                st.caption(f"{total_pages:,} total pages")

st.markdown("---")

# Visualizations Row 1
vis_col1, vis_col2 = st.columns(2)

with vis_col1:
    st.subheader("⭐ Rating Comparison")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
    
    # My ratings histogram
    ax1.hist(df_filtered['rating_num'], bins=5, alpha=0.7, color='#4472C4', edgecolor='black')
    ax1.set_title('My Ratings', fontweight='bold')
    ax1.set_xlabel('Rating')
    ax1.set_ylabel('Number of Books')
    ax1.grid(True, alpha=0.3)
    
    # Community ratings histogram
    ax2.hist(df_filtered['avg_rating'], bins=5, alpha=0.7, color='#A5A5A5', edgecolor='black')
    ax2.set_title('Community Ratings', fontweight='bold')
    ax2.set_xlabel('Rating')
    ax2.set_ylabel('Number of Books')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

with vis_col2:
    st.subheader("📈 Books Read Per Year")
    yearly_counts = df_filtered['year_added'].value_counts().sort_index()
    avg_books_per_year = yearly_counts.mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(yearly_counts.index, yearly_counts.values, color='#4472C4', alpha=0.7, edgecolor='black')
    ax.axhline(y=avg_books_per_year, color='#264478', linestyle='--', linewidth=2, 
               label=f'Average: {avg_books_per_year:.1f} books/year')
    ax.set_title('Books Read Per Year', fontsize=16, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Books Read')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# Visualizations Row 2
vis_col3, vis_col4 = st.columns(2)

with vis_col4:
    st.subheader("📖 Page Count vs Rating Analysis")
    
    # Create page bins
    df_temp = df_filtered.copy()
    df_temp['page_bin'] = pd.cut(df_temp['num_of_pages'], 
                                bins=[0, 200, 300, 400, 500, float('inf')], 
                                labels=['0-200', '201-300', '301-400', '401-500', '500+'])
    
    # Calculate average rating per bin
    bin_ratings = df_temp.groupby('page_bin').agg({
        'rating_num': ['mean', 'count']
    }).round(2)
    bin_ratings.columns = ['avg_rating', 'book_count']
    bin_ratings = bin_ratings.reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart of average ratings by page range
    bars = ax.bar(bin_ratings['page_bin'], bin_ratings['avg_rating'], 
                  color='#70AD47', alpha=0.7, edgecolor='black')
    
    ax.set_title('Average Rating by Page Count Range', fontsize=16, fontweight='bold')
    ax.set_xlabel('Page Count Range')
    ax.set_ylabel('Average Rating')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 5)
    
    # Add value labels on bars and book counts
    for i, bar in enumerate(bars):
        height = bar.get_height()
        book_count = int(bin_ratings.iloc[i]['book_count'])
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'({book_count} books)', ha='center', va='center', fontsize=8)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

