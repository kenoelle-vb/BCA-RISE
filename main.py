# streamlit run "C:\Users\keno\OneDrive\Documents\Projects\BCA RISE\merchantview.py"

import streamlit as st
import pandas as pd
import numpy as np
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import altair as alt
from gtts import gTTS
import io
from PIL import Image
import base64

# ============================================== HTML AND CSS =========================================================================================

# This part assumes 'BCA Rise Logo.png' and 'Blue Wallpaper.png' exist in the same directory
# In a real deployed app, you might need to handle asset paths differently.
try:
    logo = Image.open("BCA RISE Logo.png")
except FileNotFoundError:
    st.warning("BCA Rise Logo.png not found. Using default Streamlit icon.")
    logo = None # Set logo to None if file not found

st.set_page_config(
    page_title="BCA RISE",
    page_icon=logo, # Use the loaded logo or None
    layout="wide",  # or "wide" if you prefer
    initial_sidebar_state="auto"
)

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.set_option('client.showErrorDetails', False)

st.markdown(
    """
    <style>
    section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {
        padding-top: 0px;  # Remove padding completely
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Hide Streamlit style elements


st.markdown("""
    <style>
    [data-testid="stTextArea"] {
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Set Montserrat font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Change color of specific Streamlit elements
st.markdown("""
    <style>
    .st-emotion-cache-1o6s5t7 {
        color: #ababab !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stExpander {
        background-color: #FFFFFF;
        border-radius: 10px;
    }
    
    .stExpander > details {
        background-color: #FFFFFF;
        border-radius: 10px;
    }
    
    .stExpander > details > summary {
        background-color: #FFFFFF;
        border-radius: 10px 10px 0 0;
        padding: 10px;
    }
    
    .stExpander > details > div {
        background-color: #FFFFFF;
        border-radius: 0 0 10px 10px;
        padding: 10px;
    }
    
    .stCheckbox {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton > button {
        color: #FFFFFF;
        background-color: #424040;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .streamlit-expanderHeader {
        font-size: 20px;
    }
    .streamlit-expanderContent {
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    try:
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
        }
        </style>
        ''' % bin_str
        
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Background image '{png_file}' not found. Using default background.")


# Set the background image
set_png_as_page_bg("Blue Wallpaper.png")

# ============================================== FUNCTIONS =========================================================================================

# Main title of the dashboard

# --- Data Generation (Now for a single merchant) ---
# Set a seed for reproducibility
np.random.seed(42)
random.seed(42)

# --- Define lists for realistic data generation ---
product_tags = [
    "fried_chicken", "milk_tea", "bakso", "coffee", "nasi_goreng",
    "sate", "martabak", "es_krim", "roti", "soto", "mie_ayam", "dimsum"
]

feedback_templates = [
    "{}nya enak tapi {} sulit ditemukan.",
    "Minumannya manis banget, pelayanan {}.",
    "Rasa biasa aja dan kurang {}.",
    "Cepat saji, tapi {} kurang.",
    "Porsi pas, tapi {} perlu ditingkatkan.",
    "Harga terjangkau, tapi {} kurang.",
    "Tempat nyaman, tapi {} kurang.",
    "Pelayanan ramah, tapi {} kurang.",
    "Produk segar, tapi {} kurang.",
    "Enak banget, sangat direkomendasikan!",
    "Kurang memuaskan, perlu banyak perbaikan.",
    "Standar, tidak ada yang spesial.",
    "Sangat baik, akan kembali lagi.",
    "Kecewa dengan {}."
]

common_issues = [
    "QR", "pelayanan", "kebersihan", "rasa", "kualitas", "parkir",
    "wifi", "tempat", "porsi", "harga", "promosi", "suasana"
]

sample_tips = [
    "Pindahkan QR ke meja kasir.",
    "Senyum saat melayani pelanggan.",
    "Bersihkan area dapur secara rutin.",
    "Tingkatkan kualitas bahan baku.",
    "Sediakan tempat parkir yang lebih luas.",
    "Perbaiki koneksi WiFi untuk pelanggan.",
    "Dekorasi ulang tempat agar lebih menarik.",
    "Berikan pelatihan tambahan untuk staf pelayanan.",
    "Tawarkan porsi yang lebih bervariasi.",
    "Adakan promosi menarik setiap bulan.",
    "Ciptakan suasana yang lebih nyaman.",
    "Pastikan ketersediaan stok produk.",
    "Periksa kebersihan toilet secara berkala.",
    "Gunakan bahan-bahan segar setiap hari."
]

# --- Generate 60 rows of data for a SINGLE merchant ---
num_rows = 60
data = []
# Fixed merchant_id for this personal dashboard
fixed_merchant_id = "M001"

for i in range(num_rows): # Loop 60 times for 60 data points for M001
    product_tag = random.choice(product_tags)

    # Generate feedback text based on templates and issues
    feedback_issue = random.choice(common_issues)
    feedback_text_template = random.choice(feedback_templates)
    if '{}' in feedback_text_template:
        if feedback_text_template.count('{}') == 2:
            feedback_text = feedback_text_template.format(product_tag.replace('_', ' ').title(), feedback_issue)
        else:
            feedback_text = feedback_text_template.format(feedback_issue)
    else:
        feedback_text = feedback_text_template # For templates without placeholders

    emoji_sentiment = random.randint(1, 5)
    avg_sentiment = round(np.random.uniform(1.0, 5.0), 1)
    sentiment_gap = round(5.0 - avg_sentiment, 1)
    impact_multiplier = round(np.random.uniform(0.05, 0.25), 2)
    potential_revenue_uplift = random.randint(50000, 500000)
    last_tip = random.choice(sample_tips)
    tip_feedback_score = random.randint(1, 5)
    mood_today = random.randint(1, 5) # This could be a single value for the merchant, but for simplicity, generated per row
    daily_revenue = random.randint(500000, 2500000) # This could be a single value for the merchant, but for simplicity, generated per row

    # Generate feedback topics (1 to 3 topics per entry)
    num_topics = random.randint(1, 3)
    feedback_topics = random.sample(common_issues, num_topics)

    # Generate recommended tips (2 to 3 tips per merchant for this specific interaction/row)
    num_recommended_tips = random.randint(2, 3)
    recommended_tips = random.sample(sample_tips, num_recommended_tips)

    data.append([
        fixed_merchant_id, product_tag, feedback_text, emoji_sentiment, avg_sentiment,
        sentiment_gap, impact_multiplier, potential_revenue_uplift, last_tip,
        tip_feedback_score, mood_today, daily_revenue, feedback_topics, recommended_tips
    ])

# Create the DataFrame for a single merchant
columns = [
    "merchant_id", "product_tag", "feedback_text", "emoji_sentiment", "avg_sentiment",
    "sentiment_gap", "impact_multiplier", "potential_revenue_uplift", "last_tip",
    "tip_feedback_score", "mood_today", "daily_revenue", "feedback_topics", "recommended_tips"
]
merchant_df = pd.DataFrame(data, columns=columns)

# --- Sample Flashcard Data (separate structure, remains the same) ---
flashcard_data = [
    {
        "flashcard_id": "FC001",
        "title": "Optimalkan Penempatan QR Code",
        "text_content": "QR code yang mudah diakses mempercepat transaksi. Coba letakkan di meja kasir atau dekat pintu masuk.",
        "image_url": "https://placehold.co/300x200/ADD8E6/000000?text=QR+Code+Tip",
        "product_relevance": ["all"],
        "topic_relevance": ["QR", "pelayanan"]
    },
    {
        "flashcard_id": "FC002",
        "title": "Senyum Pelayanan Prima",
        "text_content": "Senyum ramah menciptakan pengalaman positif bagi pelanggan. Latih staf untuk selalu tersenyum.",
        "image_url": "https://placehold.co/300x200/90EE90/000000?text=Customer+Service+Tip",
        "product_relevance": ["all"],
        "topic_relevance": ["pelayanan"]
    },
    {
        "flashcard_id": "FC003",
        "title": "Jaga Kebersihan Dapur",
        "text_content": "Dapur yang bersih menjamin kualitas dan keamanan makanan. Lakukan pembersihan rutin setiap hari.",
        "image_url": "https://placehold.co/300x200/FFB6C1/000000?text=Kitchen+Cleanliness",
        "product_relevance": ["fried_chicken", "bakso", "nasi_goreng", "soto", "mie_ayam"],
        "topic_relevance": ["kebersihan"]
    },
    {
        "flashcard_id": "FC004",
        "title": "Inovasi Rasa Produk",
        "text_content": "Jangan takut bereksperimen dengan rasa baru. Dengar masukan pelanggan untuk peningkatan.",
        "image_url": "https://placehold.co/300x200/DDA0DD/000000?text=Flavor+Innovation",
        "product_relevance": ["all"],
        "topic_relevance": ["rasa"]
    },
    {
        "flashcard_id": "FC005",
        "title": "Perluas Pilihan Menu",
        "text_content": "Tawarkan variasi menu untuk menarik lebih banyak pelanggan. Pertimbangkan tren makanan terkini.",
        "image_url": "https://placehold.co/300x200/87CEFA/000000?text=Menu+Expansion",
        "product_relevance": ["all"],
        "topic_relevance": ["porsi", "kualitas"]
    },
    {
        "flashcard_id": "FC006",
        "title": "Optimalkan Promosi Digital",
        "text_content": "Manfaatkan media sosial dan platform online untuk menjangkau lebih banyak pelanggan. Buat konten menarik!",
        "image_url": "https://placehold.co/300x200/FFD700/000000?text=Digital+Promo",
        "product_relevance": ["all"],
        "topic_relevance": ["promosi"]
    }
]

# --- Merchant Data for the Dashboard (now directly from the single-merchant DataFrame) ---
# Since merchant_df now only contains data for one merchant, we can use it directly.
current_merchant_products = merchant_df # All rows in merchant_df are for this single merchant
current_merchant_data = merchant_df.iloc[0] # Get the first row for general merchant info (e.g., a single recommended tip)

# --- Sidebar Navigation ---
st.sidebar.subheader("📈 BCA RISE Merchant Dashboard")
# st.sidebar.markdown(f"### Current Merchant: **{fixed_merchant_id}**") # Display the fixed merchant ID

# Define the sections for sidebar navigation
sections = {
    "📊 Customer Feedback Insights": "feedback",
    "🎯 Product Sentiment Gap": "sentiment_gap",
    "🧠 Coaching Corner": "coaching"
}

# Create selectbox for navigation
selected_section = st.sidebar.selectbox( # Changed from st.radio to st.selectbox
    "Go to section:",
    list(sections.keys())
)

# --- Main Content Area (Conditional Display based on Sidebar Selection) ---

if selected_section == "📊 Customer Feedback Insights":
    st.markdown(
        """
        <span style='color:white; font-size:36px; font-weight:bold; margin-top: 15px; display: block;'>📊 Customer Feedback Insights</span>
        """, 
        unsafe_allow_html=True
    )
    with st.expander("", expanded=True): # Changed to empty string
        st.markdown("#### Kata-kata terbanyak")
        # Combine feedback text ONLY for the current merchant for the WordCloud
        current_merchant_feedback_text = " ".join(current_merchant_products['feedback_text'].dropna().tolist())
        if current_merchant_feedback_text:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(current_merchant_feedback_text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("No feedback text available for WordCloud for this merchant.")
        
        st.title("")
        st.markdown("#### Peta Sentimen Emoji (Rata-rata sentimen per produk)")
        # Calculate average sentiment per product for the selected merchant, then get top 5
        product_sentiment_avg = current_merchant_products.groupby('product_tag')['avg_sentiment'].mean().reset_index()
        product_sentiment_avg = product_sentiment_avg.sort_values(by='avg_sentiment', ascending=False).head(5) # Top 5
        if not product_sentiment_avg.empty:
            chart = alt.Chart(product_sentiment_avg).mark_bar().encode(
                x=alt.X('product_tag:N', sort='-y', title="Product"),
                y=alt.Y('avg_sentiment:Q', title="Average Sentiment (1-5)"),
                tooltip=['product_tag', 'avg_sentiment']
            ).properties(
                title='Average Sentiment by Product (Top 5)' # Updated title
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No product sentiment data available for this merchant.")

        st.markdown("#### Isu-isu dan Topik Relevan")
        all_topics = [topic for sublist in current_merchant_products['feedback_topics'].dropna() for topic in sublist]
        unique_topics = sorted(list(set(all_topics)))
        if unique_topics:
            st.text_area(
                "Identified Top Issues:",
                value="\n".join([f"- {topic.replace('_', ' ').title()}" for topic in unique_topics]),
                height=350,
                disabled=False
            )
        else:
            st.info("No feedback topics identified for this merchant.")

elif selected_section == "🎯 Product Sentiment Gap":
    st.markdown(
        """
        <span style='color:white; font-size:36px; font-weight:bold; margin-top: 15px; display: block;'>🎯 Product Sentiment Gap</span>
        """, 
        unsafe_allow_html=True
    )
    with st.expander("", expanded=True): # Changed to empty string
        st.markdown("#### Sentimen vs Potensi Produk")
        if not current_merchant_products.empty:
            # Prepare data for the chart, sort by potential_revenue_uplift and get top 5
            chart_data = current_merchant_products.sort_values(by='potential_revenue_uplift', ascending=False).head(5)[['product_tag', 'sentiment_gap', 'potential_revenue_uplift']] # Top 5

            bar_sentiment_gap = alt.Chart(chart_data).mark_bar(color='#4CAF50').encode(
                x=alt.X('product_tag:N', sort='-y', title="Product"),
                y=alt.Y('sentiment_gap:Q', title="Sentiment Gap (5 - Avg Sentiment)"),
                tooltip=['product_tag', 'sentiment_gap', 'potential_revenue_uplift']
            ).properties(title='Gap Sentimen Per Produk (Top 5)') # Updated title

            bar_revenue_uplift = alt.Chart(chart_data).mark_bar(color='#2196F3').encode(
                x=alt.X('product_tag:N', sort='-y', title="Product"),
                y=alt.Y('potential_revenue_uplift:Q', title="Potential Revenue Uplift (IDR)"),
                tooltip=['product_tag', 'sentiment_gap', 'potential_revenue_uplift']
            ).properties(title='Potensi Pendapatan Per Produk (Top 5)') # Updated title

            st.altair_chart(bar_sentiment_gap, use_container_width=True)
            st.altair_chart(bar_revenue_uplift, use_container_width=True)
        else:
            st.info("No product sentiment gap data available for this merchant.")

        # st.markdown("#### Motivational Quote / Summary")
        top_products = current_merchant_products.sort_values(by='avg_sentiment', ascending=False).head(5)
        if not top_products.empty:
            st.markdown("---")
            st.markdown("##### 🏆 Produk-produk juaramu :")
            for idx, row in top_products.iterrows():
                st.markdown(f"**{row['product_tag'].replace('_', ' ').title()}** with a sentiment of **{row['avg_sentiment']}/5**!")
        else:
            st.info("No product data to generate motivational quotes for this merchant.")

elif selected_section == "🧠 Coaching Corner":
    st.markdown(
        """
        <span style='color:white; font-size:36px; font-weight:bold; margin-top: 15px; display: block;'>🧠 Coaching Corner</span>
        """, 
        unsafe_allow_html=True
    )
    with st.expander("", expanded=True): # Changed to empty string
        st.markdown("#### Flashcard Carousel")
        if flashcard_data:
            # Get current merchant's topics for relevance
            current_merchant_topics = [topic for sublist in current_merchant_products['feedback_topics'].dropna() for topic in sublist]
            current_merchant_topics_set = set(current_merchant_topics)

            ranked_flashcards = []
            general_flashcards = []

            for fc in flashcard_data:
                # Check for topic relevance
                if any(topic in current_merchant_topics_set for topic in fc.get("topic_relevance", [])):
                    ranked_flashcards.append(fc)
                else:
                    general_flashcards.append(fc)

            # Combine, prioritizing ranked flashcards
            display_flashcards = ranked_flashcards + general_flashcards
            # Ensure we only display up to 6 flashcards, or fewer if not enough are available
            display_flashcards = display_flashcards[:6]

            cols = st.columns(3) # Display in 3 columns
            for i, flashcard in enumerate(display_flashcards):
                with cols[i % 3]:
                    st.image(flashcard["image_url"], caption=flashcard["title"], use_container_width=True) # Changed to use_container_width
                    st.markdown(f"**{flashcard['title']}**")
                    st.write(flashcard["text_content"])
                    st.markdown("---")
        else:
            st.info("No flashcard data available.")

        # st.markdown("#### Audio Playback (Whisper-generated)")
        all_recommended_tips = [tip for sublist in current_merchant_products['recommended_tips'].dropna() for tip in sublist]

        # st.markdown("#### Customized NLP Coaching Tip")
        if all_recommended_tips:
            unique_recommended_tips = sorted(list(set(all_recommended_tips)))
            # st.markdown("---")
            st.markdown("##### 📌 Sekedar tips untuk kamu :")
            for tip in unique_recommended_tips[:5]: # Display only top 5
                st.markdown(f"- {tip}")
        else:
            st.info("No customized coaching tips available for this merchant.")
