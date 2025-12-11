import streamlit as st
from ultralytics import YOLO
from PIL import Image, ImageDraw
import requests
import numpy as np
import wikipedia

# Set the API key and CSE ID directly in the code
API_KEY = 'your_google_api_key'  # Replace with your actual API key
SEARCH_ENGINE_ID = 'your_custom_search_engine_id'  # Replace with your actual CSE ID

# Check if API keys are configured
API_KEYS_CONFIGURED = API_KEY != 'your_google_api_key' and SEARCH_ENGINE_ID != 'your_custom_search_engine_id'

# Page configuration
st.set_page_config(
    page_title="🌿 CropGuard AI | Intelligent Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "🌿 CropGuard AI - Advanced Plant Disease Detection System powered by YOLOv8"
    }
)

# Premium Website-Style CSS with Better Colors, Floating Icons, and Enhanced Typography
st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Floating Icons Animation */
    @keyframes float {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }
        50% {
            transform: translateY(-20px) rotate(5deg);
        }
    }
    
    @keyframes floatReverse {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }
        50% {
            transform: translateY(-15px) rotate(-5deg);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.1);
            opacity: 0.8;
        }
    }
    
    .floating-icon {
        animation: float 3s ease-in-out infinite;
        display: inline-block;
        font-size: 3rem;
    }
    
    .floating-icon-reverse {
        animation: floatReverse 3s ease-in-out infinite;
        display: inline-block;
        font-size: 3rem;
    }
    
    .pulse-icon {
        animation: pulse 2s ease-in-out infinite;
        display: inline-block;
    }
    
    /* Hero Section with Premium Colors */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        color: rgba(255,255,255,0.95);
        font-weight: 400;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
        line-height: 1.6;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-feature {
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(15px);
        padding: 1.2rem 2rem;
        border-radius: 15px;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border: 2px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .hero-feature:hover {
        background: rgba(255,255,255,0.35);
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.15);
        margin-bottom: 2rem;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        box-shadow: 0 20px 45px rgba(102, 126, 234, 0.25);
        transform: translateY(-2px);
    }
    
    /* Disease Card with Premium Design */
    .disease-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .disease-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .disease-card:hover::before {
        left: 100%;
    }
    
    .disease-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.25);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Enhanced Info Boxes with Better Colors */
    .info-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.2);
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
        color: #2e7d32;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.2);
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
        color: #e65100;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.8rem;
        border-radius: 15px;
        border-left: 5px solid #2196f3;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.2);
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
        color: #1565c0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #a5d6a7 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #4caf50;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
        text-align: center;
        color: #1b5e20;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.25);
    }
    
    /* Enhanced Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Enhanced Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9ff 0%, #e8ebff 100%);
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%);
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Image Container */
    .image-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        margin: 1.5rem 0;
        border: 3px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .image-container:hover {
        box-shadow: 0 20px 45px rgba(102, 126, 234, 0.25);
        transform: translateY(-5px);
    }
    
    /* Welcome Section */
    .welcome-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 4rem 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.15);
        margin: 2rem 0;
        border: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-item {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
        transition: all 0.4s ease;
        border: 2px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-item:hover::before {
        transform: scaleX(1);
    }
    
    .feature-item:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    /* Premium Footer */
    .footer {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 4rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    /* Typography Enhancements */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    p {
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .feature-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Loading Animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    </style>
""", unsafe_allow_html=True)

# Load YOLOv8 model
@st.cache_resource
def load_model():
    try:
        return YOLO("model/last (2).pt")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model = load_model()

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h2 style="color: #667eea; margin: 0; font-family: 'Poppins', sans-serif;">⚙️ Control Panel</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    confidence_threshold = st.slider(
        "Detection Sensitivity",
        min_value=0.01,
        max_value=1.0,
        value=0.25,
        step=0.01,
        help="Adjust the confidence threshold for disease detection. Higher values require more certainty before reporting a disease."
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success(f"**AI Model**: YOLOv8\n\n**Status**: ✅ Operational\n\n**Version**: 8.0")
    
    st.markdown("---")
    st.markdown("### ℹ️ About CropGuard AI")
    st.markdown("""
    **Intelligent Plant Health Analysis**
    
    Leveraging cutting-edge deep learning technology to provide accurate, real-time plant disease detection and comprehensive treatment recommendations.
    
    **Core Capabilities:**
    - 🖼️ Advanced image analysis
    - 🔍 Real-time disease detection
    - 📚 Comprehensive information database
    - 💊 Expert treatment guidance
    """)

# Function to search the web using Google Custom Search API
def search_web(query, num_results=3):
    if not API_KEYS_CONFIGURED:
        return []
    
    try:
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={num_results}"
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            if 'items' in data:
                for item in data['items']:
                    title = item.get('title', 'No title')
                    snippet = item.get('snippet', 'No description available')
                    link = item.get('link', '')
                    if 'site:.in' in query and 'amazon.in' in link:
                        results.append({'title': title, 'snippet': snippet, 'link': link})
                    elif 'site:.in' not in query:
                        results.append({'title': title, 'snippet': snippet, 'link': link})
            return results
        return []
    except requests.exceptions.Timeout:
        return []
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []

# Function to get comprehensive disease information from Wikipedia
def get_disease_info_from_wikipedia(disease_name):
    try:
        page = wikipedia.page(disease_name, auto_suggest=False)
        summary = page.summary
        return summary, page.url
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            summary = page.summary
            return summary, page.url
        except:
            try:
                summary = wikipedia.summary(disease_name, sentences=5)
                return summary, None
            except:
                return f"Comprehensive information about {disease_name} is available but requires refinement for accurate display.", None
    except wikipedia.exceptions.PageError:
        try:
            modified_name = f"{disease_name} plant disease"
            page = wikipedia.page(modified_name, auto_suggest=False)
            summary = page.summary
            return summary, page.url
        except:
            return f"{disease_name} represents a significant plant disease that can substantially impact crop health and agricultural yield. Early identification and prompt treatment are essential to prevent widespread damage and ensure optimal plant growth.", None
    except Exception:
        return f"Retrieving detailed information about {disease_name}. This condition requires immediate attention and appropriate agricultural intervention.", None

# Function to get general prevention and treatment advice
def get_general_prevention_advice(disease_name):
    general_advice = {
        "Leaf Spot": [
            "Immediately remove and properly dispose of all infected leaves to prevent disease spread",
            "Maintain adequate spacing between plants to ensure optimal air circulation",
            "Implement proper watering techniques by targeting the base of plants, avoiding leaf contact",
            "Apply recommended fungicides containing copper or sulfur compounds",
            "Establish a crop rotation schedule to minimize disease recurrence"
        ],
        "Blossom Blight": [
            "Prune and remove all infected blossoms and affected branches promptly",
            "Apply appropriate fungicidal treatments during the critical flowering period",
            "Ensure excellent air circulation throughout the growing area",
            "Maintain garden cleanliness by removing all plant debris regularly",
            "Select and cultivate disease-resistant plant varieties when available"
        ],
        "default": [
            "Immediately remove and destroy all infected plant parts to contain the disease",
            "Maintain optimal plant spacing to promote healthy air circulation",
            "Implement proper irrigation practices, watering at plant base only",
            "Apply suitable fungicides or pesticides following manufacturer guidelines",
            "Practice excellent garden hygiene by regularly removing debris",
            "Consider utilizing disease-resistant plant varieties",
            "Establish a regular monitoring schedule for early disease detection",
            "Consult with local agricultural extension services for region-specific solutions"
        ]
    }
    
    return general_advice.get(disease_name, general_advice["default"])

# Function to draw bounding boxes on image
def draw_boxes(image, boxes, labels, scores, model_names):
    try:
        draw = ImageDraw.Draw(image)
        colors = {
            0: (255, 0, 0),    # Red
            1: (0, 255, 0),    # Green
            2: (0, 0, 255),    # Blue
            3: (255, 255, 0),  # Yellow
            4: (255, 0, 255),  # Magenta
            5: (0, 255, 255),   # Cyan
        }
        
        for i, (box, label, score) in enumerate(zip(boxes, labels, scores)):
            x1, y1, x2, y2 = box
            color = colors.get(int(label) % len(colors), (255, 255, 255))
            
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(image.width, int(x2)), min(image.height, int(y2))
            
            draw.rectangle([x1, y1, x2, y2], outline=color, width=4)
            
            label_text = f"{model_names[int(label)]} ({score:.2f})"
            text_y = y1 - 25 if y1 - 25 > 0 else y1 + 5
            draw.text((x1, text_y), label_text, fill=color)
        
        return image
    except Exception:
        return image

# Function to display disease information
def display_disease_info(disease_name, confidence_score):
    tab1, tab2, tab3 = st.tabs(["📖 Disease Information", "🛡️ Prevention & Treatment", "🛒 Product Recommendations"])
    
    with tab1:
        st.markdown(f"### 🔬 {disease_name}")
        disease_info, wiki_url = get_disease_info_from_wikipedia(disease_name)
        st.markdown(f'<div class="info-box">{disease_info}</div>', unsafe_allow_html=True)
        
        if wiki_url:
            st.markdown(f"📚 [Explore comprehensive information on Wikipedia]({wiki_url})")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Detection Confidence", f"{confidence_score:.1%}")
        with col2:
            st.metric("Detection Status", "⚠️ Disease Identified")
    
    with tab2:
        prevention_query = f"{disease_name} prevention and cure site:.in"
        prevention_results = search_web(prevention_query)

        if prevention_results:
            st.markdown("### 🛡️ Expert Prevention & Treatment Methods")
            for idx, result in enumerate(prevention_results, 1):
                with st.expander(f"📄 {result['title']}", expanded=(idx == 1)):
                    st.write(result['snippet'])
                    st.markdown(f"[🔗 Access full article]({result['link']})")
        else:
            st.markdown("### 🛡️ Comprehensive Prevention & Treatment Guidelines")
            st.markdown('<div class="tip-box">', unsafe_allow_html=True)
            st.markdown("**Recommended Action Plan:**")
            advice_list = get_general_prevention_advice(disease_name)
            for advice in advice_list:
                st.markdown(f"• {advice}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### 📚 Additional Professional Resources")
            st.info("""
            **For specialized treatment recommendations:**
            - Consult with certified agricultural extension services
            - Visit your local agricultural department for expert guidance
            - Contact plant pathology specialists
            - Engage with local nurseries for region-specific solutions
            """)
            
            if not API_KEYS_CONFIGURED:
                st.markdown("""
                <div style="background-color: #F5F5F5; padding: 1rem; border-radius: 10px; margin-top: 1rem; font-size: 0.9em; color: #666;">
                    💡 <strong>Enhancement Tip:</strong> Configure Google Custom Search API keys (lines 9-10) to access web-based prevention information and expert resources.
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        product_query = f"{disease_name} pesticides fertilizers site:amazon.in"
        product_results = search_web(product_query)

        if product_results:
            st.markdown("### 🛒 Recommended Treatment Products")
            cols = st.columns(min(len(product_results), 3))
            for idx, result in enumerate(product_results):
                col = cols[idx % len(cols)]
                with col:
                    st.markdown(f"""
                    <div class="disease-card">
                        <h4 style="color: #667eea; margin-bottom: 0.5rem;">{result['title'][:50]}...</h4>
                        <p style="font-size: 0.95em; color: #666; line-height: 1.6;">{result['snippet'][:120]}...</p>
                        <a href="{result['link']}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600; display: inline-block; margin-top: 0.5rem;">🛒 View Product Details →</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("### 🛒 Treatment Product Resources")
            st.markdown('<div class="tip-box">', unsafe_allow_html=True)
            st.markdown(f"""
            **Where to Source Treatment Products:**
            
            • **Agricultural Supply Stores**: Visit specialized agricultural supply stores for professional-grade fungicides and pesticides
            • **E-commerce Platforms**: Search for "{disease_name} treatment solutions" on major online marketplaces
            • **Agricultural Cooperatives**: Connect with local farming cooperatives for bulk purchasing options
            • **Specialized Garden Centers**: Explore garden centers for both organic and conventional treatment options
            
            **Treatment Categories Available:**
            - **Fungicides**: Specifically designed for fungal disease management
            - **Bactericides**: Effective against bacterial plant diseases
            - **Organic Solutions**: Natural treatments including neem oil and copper-based formulations
            - **Systemic Treatments**: Advanced solutions that are absorbed by the plant for comprehensive protection
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if not API_KEYS_CONFIGURED:
                st.markdown("""
                <div style="background-color: #F5F5F5; padding: 1rem; border-radius: 10px; margin-top: 1rem; font-size: 0.9em; color: #666;">
                    💡 <strong>Enhancement Tip:</strong> Configure Google Custom Search API keys (lines 9-10) to receive direct product links from Amazon India and other trusted suppliers.
                </div>
                """, unsafe_allow_html=True)

# Main App - Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="floating-icon">🌿</div>
        <h1 class="hero-title">CropGuard AI</h1>
        <p class="hero-subtitle">Intelligent Plant Disease Detection System<br>Powered by Advanced Deep Learning Technology</p>
        <div class="hero-features">
            <div class="hero-feature">⚡ Instant Analysis</div>
            <div class="hero-feature">🎯 High Accuracy</div>
            <div class="hero-feature">📚 Expert Guidance</div>
            <div class="hero-feature">💊 Treatment Solutions</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Image upload section
st.markdown("""
    <div class="upload-section">
        <h2 style="text-align: center; color: #333; margin-bottom: 1rem; font-family: 'Poppins', sans-serif;">
            <span class="floating-icon-reverse">📤</span> Upload Your Plant Image
        </h2>
        <p style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.1rem;">
            Experience cutting-edge AI-powered disease detection with comprehensive treatment recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Select an image file to analyze",
    type=["jpg", "jpeg", "png"],
    help="For optimal results, upload a clear, well-lit image focusing on the affected plant area"
)

if uploaded_file:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📷 Original Image")
        try:
            image = Image.open(uploaded_file)
            
            if image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(image, use_container_width=True, caption="Original Plant Image")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            st.stop()
    
    with col2:
        st.markdown("### 🔍 Analysis Results")
        with st.spinner("🔍 Analyzing image with AI technology..."):
            try:
                results = model.predict(np.array(image), conf=confidence_threshold, verbose=False)
                
                boxes = results[0].boxes.xyxy.cpu().numpy() if len(results[0].boxes) > 0 else []
                labels = results[0].boxes.cls.cpu().numpy() if len(results[0].boxes) > 0 else []
                scores = results[0].boxes.conf.cpu().numpy() if len(results[0].boxes) > 0 else []

                if len(boxes) > 0:
                    annotated_image = image.copy()
                    annotated_image = draw_boxes(annotated_image, boxes, labels, scores, model.names)
                    
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(annotated_image, use_container_width=True, caption="AI Detection Results with Annotations")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("### 📊 Detection Summary")
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        st.metric("Diseases Identified", len(boxes))
                    with metric_col2:
                        avg_confidence = np.mean(scores) * 100
                        st.metric("Average Confidence", f"{avg_confidence:.1f}%")
                    
                    st.markdown("---")
                    
                    for i, (label, score) in enumerate(zip(labels, scores)):
                        disease_name = model.names[int(label)]
                        st.markdown(f'<div class="disease-card">', unsafe_allow_html=True)
                        display_disease_info(disease_name, score)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if i < len(labels) - 1:
                            st.markdown("---")
                else:
                    st.markdown("""
                    <div class="success-box">
                        <div class="pulse-icon" style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                        <h2 style="color: #1b5e20; margin: 0.5rem 0;">No Diseases Detected!</h2>
                        <p style="font-size: 1.1rem; margin: 0;">Your plant appears to be in excellent health. Continue regular monitoring to maintain optimal plant condition.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.image(image, use_container_width=True, caption="Healthy Plant - No Issues Detected")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.info("Please try uploading a different image or adjust the detection sensitivity threshold.")
else:
    # Welcome screen
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #333; margin-bottom: 1rem; font-family: 'Poppins', sans-serif;">
            <span class="floating-icon">👋</span> Welcome to CropGuard AI
        </h2>
        <p style="text-align: center; font-size: 1.2em; color: #666; margin-bottom: 2rem; line-height: 1.8;">
            Upload an image of your plant to receive instant AI-powered disease detection<br>
            along with comprehensive treatment recommendations and expert guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-icon floating-icon">📤</div>
            <h3 style="color: #667eea; margin: 1rem 0;">Simple Upload</h3>
            <p style="color: #666; line-height: 1.6;">Select a clear, high-quality image of the plant leaf or affected area for analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-icon floating-icon-reverse">🔍</div>
            <h3 style="color: #667eea; margin: 1rem 0;">AI Analysis</h3>
            <p style="color: #666; line-height: 1.6;">Our advanced YOLOv8 deep learning model performs real-time disease detection with exceptional accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-icon pulse-icon">💊</div>
            <h3 style="color: #667eea; margin: 1rem 0;">Expert Solutions</h3>
            <p style="color: #666; line-height: 1.6;">Receive comprehensive prevention methods, treatment recommendations, and product suggestions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Best Practices for Optimal Results")
    st.markdown("""
    <div class="tip-box">
        <ul style="margin: 0; padding-left: 1.5rem; line-height: 2;">
            <li>Utilize clear, well-lit images with good contrast</li>
            <li>Focus the camera on the affected area for maximum detail</li>
            <li>Ensure image quality meets minimum resolution of 500x500 pixels</li>
            <li>Capture images in natural lighting conditions when possible</li>
            <li>Remove any obstructions that may interfere with disease visibility</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Premium Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0; font-size: 1.3em; font-weight: 600; font-family: 'Poppins', sans-serif;">
        <span class="floating-icon">🌿</span> CropGuard AI
    </p>
    <p style="margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1rem;">
        Intelligent Plant Disease Detection System | Powered by YOLOv8 & Streamlit
    </p>
    <p style="margin: 1rem 0 0 0; opacity: 0.7; font-size: 0.9rem;">
        Advanced Deep Learning Technology for Agricultural Excellence
    </p>
</div>
""", unsafe_allow_html=True)
