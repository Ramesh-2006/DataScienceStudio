import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import warnings
import re
from datetime import datetime
import io

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Data Science Playground | Complete EDA Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Professional CSS for frontend design
st.markdown("""
<style>
    /* Root styling */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #4caf50;
        --warning-color: #ff9800;
        --danger-color: #f44336;
        --info-color: #2196f3;
    }

    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .main-header p {
        margin: 0.8rem 0 0;
        opacity: 0.95;
        font-size: 1.1rem;
    }

    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
        border-color: #e0e0e0;
    }

    /* Comparison container */
    .comparison-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    /* Before/After cards */
    .before-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 5px solid #ff9800;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 10px rgba(255, 152, 0, 0.15);
    }

    .after-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 10px rgba(76, 175, 80, 0.15);
    }

    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        color: #666;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #2196f3;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
    }

    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
    }

    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 5px solid #ff9800;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.1);
    }

    /* Stat card */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2.5rem;
        margin-top: 3rem;
        border-top: 2px solid #f0f0f0;
        color: #666;
        background: #fafafa;
        border-radius: 12px;
    }

    /* Cleaning step */
    .cleaning-step {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .badge-success {
        background-color: #4caf50;
        color: white;
    }

    .badge-warning {
        background-color: #ff9800;
        color: white;
    }

    .badge-info {
        background-color: #2196f3;
        color: white;
    }

    /* Section title */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem;
        color: #333;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    /* Placeholder styling */
    .placeholder-container {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        border: 2px dashed #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []

# ============== Helper Functions ==============

def clean_column_names(df):
    """Clean column names: remove spaces, special chars, make lowercase"""
    original_names = df.columns.tolist()
    df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', col.strip().lower()) for col in df.columns]
    changes = []
    for old, new in zip(original_names, df.columns):
        if old != new:
            changes.append(f"'{old}' → '{new}'")
    return df, changes

def remove_duplicates(df):
    """Remove duplicate rows"""
    initial_count = len(df)
    df = df.drop_duplicates()
    removed = initial_count - len(df)
    return df, removed

def handle_missing_values(df, strategy):
    """Handle missing values based on strategy"""
    missing_before = df.isnull().sum().sum()
    
    if strategy == 'Drop rows with missing values':
        df = df.dropna()
        method = "Dropped rows with any missing values"
    elif strategy == 'Fill with mean (numeric)':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].mean())
        method = "Filled numeric columns with mean"
    elif strategy == 'Fill with median (numeric)':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())
        method = "Filled numeric columns with median"
    elif strategy == 'Fill with mode (categorical)':
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
        method = "Filled categorical columns with mode"
    else:
        method = "No action taken"
    
    missing_after = df.isnull().sum().sum()
    return df, missing_before, missing_after, method

def remove_outliers(df, column, method='IQR'):
    """Remove outliers from specified column"""
    if column not in df.columns:
        return df, 0
    
    initial_count = len(df)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    if method == 'IQR':
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    elif method == 'Z-Score':
        mean = df[column].mean()
        std = df[column].std()
        df = df[abs(df[column] - mean) <= 3 * std]
    
    removed = initial_count - len(df)
    return df, removed

def standardize_text(df, column):
    """Standardize text column (lowercase, strip whitespace)"""
    if column in df.columns and df[column].dtype == 'object':
        df[column] = df[column].str.lower().str.strip()
        return df, True
    return df, False

def convert_data_types(df):
    """Automatically convert columns to appropriate data types"""
    changes = []
    for col in df.columns:
        original_type = df[col].dtype
        try:
            df[col] = pd.to_numeric(df[col])
            if original_type != df[col].dtype:
                changes.append(f"{col}: {original_type} → {df[col].dtype}")
        except:
            try:
                df[col] = pd.to_datetime(df[col])
                if original_type != df[col].dtype:
                    changes.append(f"{col}: {original_type} → datetime")
            except:
                pass
    return df, changes

def trim_whitespace(df):
    """Trim whitespace from string columns"""
    changes = []
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
        changes.append(col)
    return df, changes

def detect_and_fix_inconsistent_categories(df, column):
    """Detect and fix inconsistent categorical values"""
    if column in df.columns:
        unique_values = df[column].nunique()
        df[column] = df[column].str.title()
        return df, unique_values - df[column].nunique()
    return df, 0

def generate_all_plots(df, numeric_cols, categorical_cols):
    """Generate all possible EDA plots using plotly"""
    plots = []
    
    # Distribution plots
    for col in numeric_cols[:5]:
        fig = px.histogram(df, x=col, marginal='box', 
                          title=f'📊 Distribution of {col}', 
                          color_discrete_sequence=['#667eea'])
        fig.update_layout(bargap=0.1, template='plotly_white', height=500)
        plots.append(('Histogram', col, fig))
    
    # Box plots
    for col in numeric_cols[:5]:
        fig = px.box(df, y=col, title=f'📦 Box Plot of {col}', 
                     color_discrete_sequence=['#764ba2'])
        fig.update_layout(template='plotly_white', height=500)
        plots.append(('Box Plot', col, fig))
    
    # Correlation heatmap
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect='auto', 
                        title='🔥 Correlation Heatmap', 
                        color_continuous_scale='RdBu_r',
                        width=600, height=500)
        fig.update_layout(template='plotly_white')
        plots.append(('Correlation', 'Heatmap', fig))
    
    # Bar plots
    for col in categorical_cols[:3]:
        value_counts = df[col].value_counts().head(10)
        fig = px.bar(x=value_counts.index, y=value_counts.values, 
                     title=f'📈 Count Plot of {col}',
                     color_discrete_sequence=['#667eea'],
                     labels={'x': col, 'y': 'Count'})
        fig.update_layout(template='plotly_white', height=500)
        plots.append(('Bar Plot', col, fig))
    
    # Scatter plots
    if len(numeric_cols) >= 2:
        for i in range(min(3, len(numeric_cols)-1)):
            for j in range(i+1, min(i+3, len(numeric_cols))):
                fig = px.scatter(df, x=numeric_cols[i], y=numeric_cols[j], 
                                 title=f'🎯 {numeric_cols[i]} vs {numeric_cols[j]}',
                                 trendline='ols', 
                                 color_discrete_sequence=['#667eea'])
                fig.update_layout(template='plotly_white', height=500)
                plots.append(('Scatter Plot', f'{numeric_cols[i]} vs {numeric_cols[j]}', fig))
    
    return plots

def show_data_comparison(original_df, cleaned_df, title="Data Cleaning Comparison"):
    """Display before and after comparison of dataframes"""
    st.markdown(f"<h3 style='color: #333; margin-top: 2rem;'>{title}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="before-card">', unsafe_allow_html=True)
        st.markdown("#### 🔴 Before Cleaning")
        col_bf1, col_bf2 = st.columns(2)
        with col_bf1:
            st.metric("Rows", f"{original_df.shape[0]:,}")
            st.metric("Missing Values", f"{original_df.isnull().sum().sum():,}")
        with col_bf2:
            st.metric("Columns", f"{original_df.shape[1]:,}")
            st.metric("Duplicates", f"{original_df.duplicated().sum():,}")
        with st.expander("📋 View Sample Data"):
            st.dataframe(original_df.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="after-card">', unsafe_allow_html=True)
        st.markdown("#### 🟢 After Cleaning")
        col_af1, col_af2 = st.columns(2)
        with col_af1:
            st.metric("Rows", f"{cleaned_df.shape[0]:,}", 
                     delta=f"{cleaned_df.shape[0] - original_df.shape[0]}")
            st.metric("Missing Values", f"{cleaned_df.isnull().sum().sum():,}", 
                     delta=f"{cleaned_df.isnull().sum().sum() - original_df.isnull().sum().sum()}")
        with col_af2:
            st.metric("Columns", f"{cleaned_df.shape[1]:,}", 
                     delta=f"{cleaned_df.shape[1] - original_df.shape[1]}")
            st.metric("Duplicates", f"{cleaned_df.duplicated().sum():,}", 
                     delta=f"{cleaned_df.duplicated().sum() - original_df.duplicated().sum()}")
        with st.expander("📋 View Sample Data"):
            st.dataframe(cleaned_df.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def get_theory_content(topic):
    """Get theory content for each topic with unique images"""
    theory_data = {
        'Need for Data Science': {
            'content': """
### Why Data Science?

Data Science has become essential in today's data-driven world. Here's why:

- **Data Explosion**: 2.5 quintillion bytes of data are created every day
- **Competitive Advantage**: Organizations use data to gain insights and make better decisions
- **Automation**: Machine learning enables automation of complex tasks
- **Personalization**: From Netflix recommendations to personalized healthcare
- **Predictive Analytics**: Forecasting trends, customer behavior, and risks

### Key Drivers

📈 **Volume**: Massive amounts of data being generated
🚀 **Velocity**: Real-time data streaming and processing
🎯 **Variety**: Different types of data (structured, unstructured, semi-structured)
✅ **Veracity**: Data quality and trustworthiness
💡 **Value**: Extracting meaningful insights from data
            """,
            'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop',
        },
        'Benefits & Uses': {
            'content': """
### Benefits of Data Science

🚀 **Business Benefits**:
- Better decision making through data-driven insights
- Improved operational efficiency
- Enhanced customer experience
- New revenue streams and business models
- Risk mitigation and fraud detection

### Real-World Applications

🏥 **Healthcare**: Disease prediction, Drug discovery, Personalized treatment
💰 **Finance**: Algorithmic trading, Credit scoring, Fraud detection
🛒 **Retail**: Recommendation systems, Inventory management, Price optimization
🚗 **Transportation**: Route optimization, Autonomous vehicles, Traffic management
            """,
            'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop',
        },
        'Facets of Data': {
            'content': """
### Understanding Data Facets

📊 **By Structure**:
- **Structured**: Tabular data (CSV, Excel, SQL databases)
- **Unstructured**: Text, images, audio, video
- **Semi-structured**: JSON, XML, log files

📈 **By Measurement Scale**:
- **Nominal**: Categories without order (colors, names)
- **Ordinal**: Categories with order (ratings, education levels)
- **Interval**: Numeric without true zero (temperature in Celsius)
- **Ratio**: Numeric with true zero (height, weight, age)
            """,
            'image': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=400&fit=crop',
        },
        'Data Science Process': {
            'content': """
### The Data Science Lifecycle

**Step-by-Step Process**:

1. **Business Understanding** 📋 - Define project objectives
2. **Data Acquisition** 📥 - Collect relevant data
3. **Data Preparation** 🧹 - Clean and transform data
4. **Exploratory Data Analysis** 🔍 - Visualize patterns
5. **Modeling** 🤖 - Select and train algorithms
6. **Evaluation** 📊 - Assess model performance
7. **Deployment** 🚀 - Put models into production
            """,
            'image': 'https://source.unsplash.com/600x400/?workflow,process,flowchart',
        },
        'Setting Research Goal': {
            'content': """
### Setting the Research Goal

🎯 **SMART Goals Framework**:

- **S**pecific: Clearly define what needs to be achieved
- **M**easurable: Define quantifiable success metrics
- **A**chievable: Ensure goals are realistic
- **R**elevant: Align with business objectives
- **T**ime-bound: Set clear deadlines

💡 **Example Goals**:
- Reduce customer churn by 15% in the next quarter
- Build a recommendation engine to increase sales by 20%
- Predict equipment failure 24 hours in advance
            """,
            'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop',
        },
        'Retrieving Data': {
            'content': """
### Data Retrieval Methods

📁 **Common Data Sources**:

**Files**: CSV, Excel, JSON, Parquet, Images, Audio, Video

**Databases**: SQL (MySQL, PostgreSQL), NoSQL (MongoDB), Data Warehouses

**APIs**: REST APIs, GraphQL, Web Scraping

**Streaming**: Kafka, IoT sensors, Real-time logs

🔧 **Popular Tools**:
- Pandas for CSV/Excel
- SQLAlchemy for databases
- Requests for API calls
- BeautifulSoup for web scraping
            """,
            'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&h=400&fit=crop',
        },
        'Significance of EDA': {
            'content': """
### Why Exploratory Data Analysis Matters

🔍 **Key Benefits**:

- Understand Data Structure and patterns
- Detect Anomalies and data quality issues
- Generate Hypotheses for testing
- Guide Feature Engineering decisions
- Inform Model Selection process

📊 **EDA Techniques**:
- Univariate Analysis: Distribution, central tendency
- Bivariate Analysis: Relationships between variables
- Multivariate Analysis: Complex interactions
- Visualization: Graphs, plots, dashboards

💡 Famous Quote:
"The greatest value of a picture is when it forces us to notice what we never expected to see." - John Tukey
            """,
            'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        },
        'Making Sense of Data': {
            'content': """
### Interpreting Data: From Numbers to Insights

🧠 **Statistical Concepts**:

**Descriptive Statistics**:
- Mean, Median, Mode
- Variance, Standard Deviation
- Range, IQR

**Inferential Statistics**:
- Confidence Intervals
- Hypothesis Testing
- P-values and Significance

**Correlation Analysis**:
- Pearson Correlation (linear)
- Spearman Correlation (monotonic)
- Correlation Matrices
            """,
            'image': 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=600&h=400&fit=crop',
        },
        'Software Tools for EDA': {
            'content': """
### Essential EDA Tools & Libraries

🐍 **Python Ecosystem**:

**Data Manipulation**:
- Pandas: Data manipulation and analysis
- NumPy: Numerical computing
- Dask: Scalable computing

**Visualization**:
- Matplotlib: Basic plotting
- Seaborn: Statistical visualizations
- Plotly: Interactive visualizations

**EDA Automation**:
- Pandas Profiling: Automated reports
- Sweetviz: Compare datasets
- D-Tale: Interactive interface
            """,
            'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&h=400&fit=crop',
        },
        'Visual Aids for EDA': {
            'content': """
### Essential Visualizations for EDA

📊 **Univariate Visualizations**:
- Histograms: Distribution of continuous variables
- Box plots: Identify outliers
- Bar charts: Categorical frequency
- Density plots: Smoothed distribution

**Bivariate Visualizations**:
- Scatter plots: Relationships between variables
- Line charts: Trends over time
- Heatmaps: Correlation matrices

**Chart Selection Guide**:
- Comparison → Bar charts, Line charts
- Distribution → Histograms, Box plots
- Composition → Stacked bar, Pie charts
- Relationship → Scatter plots, Heatmaps
            """,
            'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop',
        }
    }
    return theory_data.get(topic, {'content': 'Content not found', 'image': ''})

def get_quiz_questions(topic):
    """Get comprehensive quiz questions for each topic"""
    quizzes = {
        'Need for Data Science': [
            {
                'question': 'How much data is created globally every day?',
                'options': ['1 billion bytes', '2.5 quintillion bytes', '500 million bytes', '10 zettabytes'],
                'correct': 1,
                'explanation': 'Approximately 2.5 quintillion bytes of data are created daily worldwide.'
            },
            {
                'question': 'Which of these is NOT a benefit of Data Science?',
                'options': ['Improved decision making', 'Eliminated need for human oversight', 'Better customer experience', 'Risk mitigation'],
                'correct': 1,
                'explanation': 'Data Science is a tool to assist, not eliminate human oversight.'
            },
            {
                'question': 'What does "Veracity" in Big Data refer to?',
                'options': ['Data speed', 'Data quality and trustworthiness', 'Data volume', 'Data variety'],
                'correct': 1,
                'explanation': 'Veracity refers to the quality and trustworthiness of data.'
            },
            {
                'question': 'Which industry heavily uses Data Science for personalization?',
                'options': ['Manufacturing', 'Healthcare', 'Entertainment (Netflix, etc.)', 'Agriculture'],
                'correct': 2,
                'explanation': 'Entertainment platforms like Netflix use Data Science for personalized recommendations.'
            },
            {
                'question': 'What key driver of Data Science refers to real-time processing?',
                'options': ['Volume', 'Velocity', 'Variety', 'Veracity'],
                'correct': 1,
                'explanation': 'Velocity refers to the speed at which data is generated and processed.'
            }
        ],
        'Benefits & Uses': [
            {
                'question': 'Which of these is a business benefit of Data Science?',
                'options': ['Increased operational costs', 'Better decision making through insights', 'Slower processes', 'Reduced customer base'],
                'correct': 1,
                'explanation': 'Data Science enables better decision making through data-driven insights.'
            },
            {
                'question': 'In Finance, what is algorithmic trading an example of?',
                'options': ['Inventory management', 'Automated trading decisions', 'Customer service', 'Supply chain'],
                'correct': 1,
                'explanation': 'Algorithmic trading uses Data Science to make automated trading decisions.'
            },
            {
                'question': 'Which healthcare application predicts disease outcomes?',
                'options': ['Drug manufacturing', 'Hospital billing', 'Disease prediction and diagnosis', 'Medical equipment maintenance'],
                'correct': 2,
                'explanation': 'Disease prediction and diagnosis is a key healthcare application of Data Science.'
            },
            {
                'question': 'What do retail recommendation systems help with?',
                'options': ['Employee scheduling', 'Product discovery and sales', 'Building infrastructure', 'Security'],
                'correct': 1,
                'explanation': 'Recommendation systems help customers discover products and increase sales.'
            },
            {
                'question': 'How does Data Science help in fraud detection?',
                'options': ['Manual review only', 'Identifying suspicious patterns', 'Ignoring warnings', 'Random checks'],
                'correct': 1,
                'explanation': 'Data Science identifies suspicious patterns that indicate potential fraud.'
            }
        ],
        'Facets of Data': [
            {
                'question': 'Which type of data includes images, videos, and audio files?',
                'options': ['Structured', 'Unstructured', 'Semi-structured', 'Encrypted'],
                'correct': 1,
                'explanation': 'Unstructured data includes images, videos, audio, and text content.'
            },
            {
                'question': 'What does "Nominal" scale data represent?',
                'options': ['Ordered categories', 'Numeric values', 'Categories without order', 'Time series'],
                'correct': 2,
                'explanation': 'Nominal scale represents categories without inherent order (colors, names, etc.).'
            },
            {
                'question': 'Which measurement scale has a true zero point?',
                'options': ['Nominal', 'Ordinal', 'Interval', 'Ratio'],
                'correct': 3,
                'explanation': 'Ratio scale has a true zero point (height, weight, age).'
            },
            {
                'question': 'JSON and XML are examples of which data structure?',
                'options': ['Structured', 'Unstructured', 'Semi-structured', 'Binary'],
                'correct': 2,
                'explanation': 'JSON and XML are semi-structured data formats.'
            },
            {
                'question': 'What type of data is collected from personal surveys?',
                'options': ['Secondary data', 'Primary data', 'Tertiary data', 'Archived data'],
                'correct': 1,
                'explanation': 'Primary data is directly collected through surveys, experiments, or sensors.'
            }
        ],
        'Data Science Process': [
            {
                'question': 'What is the FIRST step in the Data Science process?',
                'options': ['Data Collection', 'Model Building', 'Business Understanding', 'Deployment'],
                'correct': 2,
                'explanation': 'Business Understanding comes first to define project objectives.'
            },
            {
                'question': 'Which step involves handling missing values and cleaning data?',
                'options': ['EDA', 'Data Preparation', 'Modeling', 'Deployment'],
                'correct': 1,
                'explanation': 'Data Preparation includes cleaning and transforming data.'
            },
            {
                'question': 'What is the purpose of Exploratory Data Analysis?',
                'options': ['Build models', 'Visualize patterns and generate hypotheses', 'Deploy models', 'Create datasets'],
                'correct': 1,
                'explanation': 'EDA helps visualize patterns and generate hypotheses for further analysis.'
            },
            {
                'question': 'At which stage do we evaluate model performance?',
                'options': ['Collection', 'Preparation', 'Evaluation', 'Deployment'],
                'correct': 2,
                'explanation': 'The Evaluation stage assesses how well the model performs.'
            },
            {
                'question': 'What happens in the Deployment stage?',
                'options': ['Data collection', 'Model training', 'Putting models into production', 'Hypothesis testing'],
                'correct': 2,
                'explanation': 'Deployment is when models are put into production for real-world use.'
            }
        ],
        'Setting Research Goal': [
            {
                'question': 'What does "S" in SMART goals represent?',
                'options': ['Sequential', 'Specific', 'Simple', 'Statistical'],
                'correct': 1,
                'explanation': '"S" stands for Specific - clearly define what needs to be achieved.'
            },
            {
                'question': 'Which SMART criterion ensures goals can be quantified?',
                'options': ['Specific', 'Measurable', 'Achievable', 'Relevant'],
                'correct': 1,
                'explanation': '"M" stands for Measurable - define quantifiable success metrics.'
            },
            {
                'question': 'What should research goals be aligned with?',
                'options': ['Team preferences', 'Business/organizational objectives', 'Available tools', 'Personal interests'],
                'correct': 1,
                'explanation': 'Goals should be Relevant to business/organizational objectives.'
            },
            {
                'question': 'Is "Reduce customer churn by 15% in next quarter" a good goal?',
                'options': ['Too vague', 'Not measurable', 'Yes, it is SMART', 'Not achievable'],
                'correct': 2,
                'explanation': 'This is a SMART goal - Specific, Measurable, Achievable, Relevant, Time-bound.'
            },
            {
                'question': 'Which factor ensures goals are realistic?',
                'options': ['Relevance', 'Achievability', 'Specificity', 'Timeliness'],
                'correct': 1,
                'explanation': '"A" stands for Achievable - ensure goals are realistic with available resources.'
            }
        ],
        'Retrieving Data': [
            {
                'question': 'Which tool is best for reading CSV files in Python?',
                'options': ['NumPy', 'Pandas', 'Matplotlib', 'Scikit-learn'],
                'correct': 1,
                'explanation': 'Pandas is the standard library for reading and manipulating CSV files.'
            },
            {
                'question': 'What type of data source is a REST API?',
                'options': ['File-based', 'Database', 'Streaming', 'API-based'],
                'correct': 3,
                'explanation': 'REST APIs are web services for retrieving data programmatically.'
            },
            {
                'question': 'Which library is used for web scraping?',
                'options': ['Pandas', 'NumPy', 'BeautifulSoup', 'Plotly'],
                'correct': 2,
                'explanation': 'BeautifulSoup is a popular library for web scraping and HTML parsing.'
            },
            {
                'question': 'What is data retrieved from existing databases called?',
                'options': ['Primary data', 'Secondary data', 'Tertiary data', 'Raw data'],
                'correct': 1,
                'explanation': 'Secondary data is data from existing sources like databases and public datasets.'
            },
            {
                'question': 'Which data retrieval concern prevents unauthorized access?',
                'options': ['Data quality', 'Data privacy and compliance', 'Data format', 'Data size'],
                'correct': 1,
                'explanation': 'Data privacy and compliance (GDPR, HIPAA) are critical concerns during retrieval.'
            }
        ],
        'Significance of EDA': [
            {
                'question': 'What does EDA stand for?',
                'options': ['Electronic Data Analysis', 'Exploratory Data Analysis', 'Extended Data Assessment', 'Efficient Data Analysis'],
                'correct': 1,
                'explanation': 'EDA stands for Exploratory Data Analysis.'
            },
            {
                'question': 'What is a key benefit of performing EDA?',
                'options': ['Building models', 'Understanding data structure and patterns', 'Deploying models', 'Writing code'],
                'correct': 1,
                'explanation': 'EDA helps understand data structure, patterns, and relationships.'
            },
            {
                'question': 'Which EDA technique examines distribution of one variable?',
                'options': ['Bivariate Analysis', 'Univariate Analysis', 'Multivariate Analysis', 'Time series'],
                'correct': 1,
                'explanation': 'Univariate Analysis examines the distribution of a single variable.'
            },
            {
                'question': 'How does EDA help in feature engineering?',
                'options': ['Replaces feature engineering', 'Guides feature engineering decisions', 'Eliminates need for features', 'Predicts outcomes'],
                'correct': 1,
                'explanation': 'EDA insights guide the creation of meaningful features.'
            },
            {
                'question': 'Can visualizations reveal unexpected patterns in EDA?',
                'options': ['No, visualizations are only for reporting', 'Yes, they often reveal unexpected insights', 'Only for large datasets', 'Never'],
                'correct': 1,
                'explanation': 'Visualizations often reveal patterns that numbers alone might miss.'
            }
        ],
        'Making Sense of Data': [
            {
                'question': 'Which metric describes the average of a dataset?',
                'options': ['Median', 'Mode', 'Mean', 'Range'],
                'correct': 2,
                'explanation': 'Mean is the arithmetic average of all values.'
            },
            {
                'question': 'What does standard deviation measure?',
                'options': ['Average value', 'Spread of data around mean', 'Most common value', 'Range'],
                'correct': 1,
                'explanation': 'Standard deviation measures how spread out data is from the mean.'
            },
            {
                'question': 'Pearson correlation measures what type of relationship?',
                'options': ['Non-linear relationships', 'Linear relationships', 'Causal relationships', 'Temporal relationships'],
                'correct': 1,
                'explanation': 'Pearson correlation measures linear relationships between variables.'
            },
            {
                'question': 'What is a p-value used for in hypothesis testing?',
                'options': ['Measuring data quality', 'Determining statistical significance', 'Calculating averages', 'Predicting outcomes'],
                'correct': 1,
                'explanation': 'P-values determine whether results are statistically significant.'
            },
            {
                'question': 'Which statistical method estimates population characteristics?',
                'options': ['Descriptive Statistics', 'Inferential Statistics', 'Univariate Analysis', 'Correlation'],
                'correct': 1,
                'explanation': 'Inferential Statistics uses sample data to estimate population characteristics.'
            }
        ],
        'Software Tools for EDA': [
            {
                'question': 'What is the primary purpose of Pandas?',
                'options': ['Creating visualizations', 'Data manipulation and analysis', 'Machine learning', 'Time tracking'],
                'correct': 1,
                'explanation': 'Pandas is the main library for data manipulation and analysis in Python.'
            },
            {
                'question': 'Which library is best for statistical visualizations?',
                'options': ['NumPy', 'Seaborn', 'Requests', 'SQLAlchemy'],
                'correct': 1,
                'explanation': 'Seaborn is built on Matplotlib and provides statistical visualizations.'
            },
            {
                'question': 'What does Pandas Profiling generate?',
                'options': ['Machine learning models', 'Automated EDA reports', 'Web pages', 'Databases'],
                'correct': 1,
                'explanation': 'Pandas Profiling generates comprehensive automated EDA reports.'
            },
            {
                'question': 'Which tool is used for large-scale data processing?',
                'options': ['Matplotlib', 'Plots', 'Dask', 'Flask'],
                'correct': 2,
                'explanation': 'Dask enables scalable computing for large datasets.'
            },
            {
                'question': 'What is NumPy primarily used for?',
                'options': ['Web development', 'Numerical computing', 'Data visualization', 'Database management'],
                'correct': 1,
                'explanation': 'NumPy provides numerical computing and array operations.'
            }
        ],
        'Visual Aids for EDA': [
            {
                'question': 'Which plot best shows the distribution of a numeric variable?',
                'options': ['Pie chart', 'Histogram', 'Line chart', 'Heatmap'],
                'correct': 1,
                'explanation': 'Histograms display the distribution of continuous variables.'
            },
            {
                'question': 'What do box plots help identify?',
                'options': ['Trends over time', 'Outliers and spread', 'Proportions', 'Correlations'],
                'correct': 1,
                'explanation': 'Box plots show quartiles, median, and outliers clearly.'
            },
            {
                'question': 'Which visualization shows relationship between two numeric variables?',
                'options': ['Bar chart', 'Pie chart', 'Scatter plot', 'Histogram'],
                'correct': 2,
                'explanation': 'Scatter plots display relationships between two numeric variables.'
            },
            {
                'question': 'What does a correlation heatmap display?',
                'options': ['Time trends', 'Category counts', 'Correlations between variables', 'Distribution'],
                'correct': 2,
                'explanation': 'Heatmaps show correlation coefficients between all variable pairs.'
            },
            {
                'question': 'When should you use a bar chart?',
                'options': ['Comparing categories', 'Showing distributions', 'Time series data', 'Correlations'],
                'correct': 0,
                'explanation': 'Bar charts are best for comparing values across categories.'
            }
        ]
    }
    return quizzes.get(topic, [])

# ============== Main Application ==============

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Data Science Playground</h1>
        <p>Interactive Learning Platform for First-Year Data Science Students</p>
        <p style="font-size: 0.95rem; margin-top: 0.5rem;">Complete EDA Studio + Comprehensive Theory</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tabs = st.tabs(["🔬 EDA Studio", "📚 Theory Library", "ℹ️ About"])

    # ========== Tab 1: EDA Studio ==========
    with tabs[0]:
        st.markdown("## 🚀 Exploratory Data Analysis Studio")
        st.markdown("Upload your dataset and apply various cleaning techniques with real-time before/after comparison!")

        col1, col2 = st.columns([3, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "📂 Choose a CSV or Excel file",
                type=['csv', 'xlsx', 'xls'],
                help="Supported formats: CSV, XLSX, XLS"
            )

        with col2:
            if uploaded_file is not None:
                if st.button("🔄 Reset All", use_container_width=True, help="Reset to original dataset"):
                    st.session_state.cleaned_df = st.session_state.original_df.copy()
                    st.session_state.cleaning_log = []
                    st.success("✅ Reset to original dataset!")
                    st.rerun()

        if uploaded_file is not None:
            try:
                # Load data
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Store in session state
                if st.session_state.original_df is None:
                    st.session_state.original_df = df.copy()
                    st.session_state.cleaned_df = df.copy()
                    st.session_state.cleaning_log = []

                # Show initial comparison
                show_data_comparison(st.session_state.original_df, st.session_state.cleaned_df, "📊 Current State")

                # Data Cleaning Section
                st.markdown("---")
                st.markdown("## 🧹 Data Cleaning Operations")
                st.markdown("Apply various cleaning methods and see the immediate impact!")

                clean_tabs = st.tabs(["📝 Column Operations", "🔢 Data Operations", "📊 Advanced Cleaning", "📋 Log"])

                # Column Operations
                with clean_tabs[0]:
                    st.markdown("### Column Operations")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("🧼 Clean Column Names", use_container_width=True):
                            df_cleaned, changes = clean_column_names(st.session_state.cleaned_df.copy())
                            if changes:
                                st.session_state.cleaned_df = df_cleaned
                                st.session_state.cleaning_log.append(f"✅ Cleaned {len(changes)} column names")
                                st.success(f"✅ Cleaned {len(changes)} column names!")
                                st.rerun()
                            else:
                                st.info("No column names needed cleaning")

                    with col2:
                        if st.button("✂️ Trim Whitespace", use_container_width=True):
                            df_cleaned, changes = trim_whitespace(st.session_state.cleaned_df.copy())
                            if changes:
                                st.session_state.cleaned_df = df_cleaned
                                st.session_state.cleaning_log.append(f"✅ Trimmed whitespace from {len(changes)} columns")
                                st.success(f"✅ Trimmed {len(changes)} columns!")
                                st.rerun()
                            else:
                                st.info("No text columns to trim")

                    with col3:
                        if st.button("🔄 Convert Data Types", use_container_width=True):
                            df_cleaned, changes = convert_data_types(st.session_state.cleaned_df.copy())
                            if changes:
                                st.session_state.cleaned_df = df_cleaned
                                st.session_state.cleaning_log.append(f"✅ Converted {len(changes)} data types")
                                st.success(f"✅ Converted {len(changes)} columns!")
                                st.rerun()
                            else:
                                st.info("No data type conversions needed")

                # Data Operations
                with clean_tabs[1]:
                    st.markdown("### Data Operations")
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("🗑️ Remove Duplicates", use_container_width=True):
                            df_cleaned, removed = remove_duplicates(st.session_state.cleaned_df.copy())
                            if removed > 0:
                                st.session_state.cleaned_df = df_cleaned
                                st.session_state.cleaning_log.append(f"✅ Removed {removed} duplicate rows")
                                st.success(f"✅ Removed {removed} duplicate rows!")
                                st.rerun()
                            else:
                                st.info("No duplicate rows found")

                    with col2:
                        st.markdown("##### Handle Missing Values")
                        missing_strategy = st.selectbox(
                            "Strategy",
                            ['Drop rows with missing values',
                             'Fill with mean (numeric)',
                             'Fill with median (numeric)',
                             'Fill with mode (categorical)'],
                            key="missing_strategy"
                        )
                        if st.button("Apply Missing Value Handling", use_container_width=True):
                            df_cleaned = st.session_state.cleaned_df.copy()
                            df_cleaned, missing_before, missing_after, method = handle_missing_values(df_cleaned, missing_strategy)
                            if missing_before != missing_after:
                                st.session_state.cleaned_df = df_cleaned
                                st.session_state.cleaning_log.append(f"✅ {method}")
                                st.success(f"✅ Reduced missing values from {missing_before} to {missing_after}")
                                st.rerun()
                            else:
                                st.info("No missing values found")

                # Advanced Cleaning
                with clean_tabs[2]:
                    st.markdown("### Advanced Cleaning Operations")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("##### Remove Outliers")
                        numeric_cols = st.session_state.cleaned_df.select_dtypes(include=[np.number]).columns.tolist()
                        if numeric_cols:
                            outlier_col = st.selectbox("Column", numeric_cols, key="outlier_col")
                            outlier_method = st.selectbox("Method", ['IQR', 'Z-Score'], key="outlier_method")
                            if st.button("Remove Outliers", use_container_width=True):
                                df_cleaned, removed = remove_outliers(st.session_state.cleaned_df.copy(), outlier_col, outlier_method)
                                if removed > 0:
                                    st.session_state.cleaned_df = df_cleaned
                                    st.session_state.cleaning_log.append(f"✅ Removed {removed} outliers from '{outlier_col}'")
                                    st.success(f"✅ Removed {removed} outliers!")
                                    st.rerun()
                                else:
                                    st.info("No outliers found")
                        else:
                            st.info("No numeric columns available")

                    with col2:
                        st.markdown("##### Standardize Text")
                        text_cols = st.session_state.cleaned_df.select_dtypes(include=['object']).columns.tolist()
                        if text_cols:
                            text_col = st.selectbox("Column", text_cols, key="text_col")
                            if st.button("Standardize Text", use_container_width=True):
                                df_cleaned, changed = standardize_text(st.session_state.cleaned_df.copy(), text_col)
                                if changed:
                                    st.session_state.cleaned_df = df_cleaned
                                    st.session_state.cleaning_log.append(f"✅ Standardized '{text_col}'")
                                    st.success(f"✅ Standardized '{text_col}'!")
                                    st.rerun()
                                else:
                                    st.info("Column already standardized")
                        else:
                            st.info("No text columns available")

                # Cleaning Log
                with clean_tabs[3]:
                    st.markdown("### Cleaning Operations Log")
                    if st.session_state.cleaning_log:
                        for idx, log_entry in enumerate(st.session_state.cleaning_log, 1):
                            st.write(f"{idx}. {log_entry}")
                        if st.button("Clear Log", use_container_width=True):
                            st.session_state.cleaning_log = []
                            st.rerun()
                    else:
                        st.info("No operations performed yet")

                # Final comparison
                st.markdown("---")
                show_data_comparison(st.session_state.original_df, st.session_state.cleaned_df, "✨ Final Comparison")

                # EDA Section
                st.markdown("---")
                st.markdown("## 🎨 Exploratory Data Analysis")

                # Data Preview
                with st.expander("🔍 View Dataset", expanded=False):
                    st.dataframe(st.session_state.cleaned_df.head(100), use_container_width=True)

                # Data Types
                st.markdown("### 📊 Data Types & Information")
                type_info = {}
                for col in st.session_state.cleaned_df.columns:
                    if st.session_state.cleaned_df[col].dtype in ['int64', 'float64']:
                        type_info[col] = 'numeric'
                    else:
                        try:
                            pd.to_datetime(st.session_state.cleaned_df[col])
                            type_info[col] = 'datetime'
                        except:
                            type_info[col] = 'categorical'

                type_df = pd.DataFrame([
                    {
                        'Column': col,
                        'Type': str(st.session_state.cleaned_df[col].dtype),
                        'Inferred': type_info[col],
                        'Unique': st.session_state.cleaned_df[col].nunique(),
                        'Missing %': f"{(st.session_state.cleaned_df[col].isnull().sum()/len(st.session_state.cleaned_df))*100:.1f}%"
                    }
                    for col in st.session_state.cleaned_df.columns
                ])
                st.dataframe(type_df, use_container_width=True)

                # Descriptive Statistics
                with st.expander("📈 Descriptive Statistics", expanded=False):
                    numeric_cols = st.session_state.cleaned_df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        st.dataframe(st.session_state.cleaned_df[numeric_cols].describe(), use_container_width=True)
                    else:
                        st.info("No numeric columns found")

                # Visualizations
                st.markdown("### 🎨 Interactive Visualizations")
                numeric_cols = st.session_state.cleaned_df.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = st.session_state.cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist()

                if len(numeric_cols) == 0 and len(categorical_cols) == 0:
                    st.warning("No suitable columns for visualization")
                else:
                    plots = generate_all_plots(st.session_state.cleaned_df, numeric_cols, categorical_cols)
                    for i in range(0, len(plots), 2):
                        col1, col2 = st.columns(2)
                        with col1:
                            if i < len(plots):
                                st.markdown(f"**{plots[i][0]}: {plots[i][1]}**")
                                st.plotly_chart(plots[i][2], use_container_width=True, key=f"plot_{i}")
                        with col2:
                            if i+1 < len(plots):
                                st.markdown(f"**{plots[i+1][0]}: {plots[i+1][1]}**")
                                st.plotly_chart(plots[i+1][2], use_container_width=True, key=f"plot_{i+1}")

                # Key Insights
                st.markdown("### 💡 Key Insights")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="info-box"><h4>📊 Data Quality</h4></div>', unsafe_allow_html=True)
                    missing_cols = st.session_state.cleaned_df.columns[st.session_state.cleaned_df.isnull().any()].tolist()
                    if missing_cols:
                        st.warning(f"⚠️ Missing values in: {', '.join(missing_cols)}")
                    else:
                        st.success("✅ No missing values!")
                    if len(st.session_state.cleaned_df[st.session_state.cleaned_df.duplicated()]) > 0:
                        st.warning(f"⚠️ {len(st.session_state.cleaned_df[st.session_state.cleaned_df.duplicated()])} duplicates")
                    else:
                        st.success("✅ No duplicates!")

                with col2:
                    st.markdown('<div class="info-box"><h4>🎯 Dataset Stats</h4></div>', unsafe_allow_html=True)
                    st.write(f"• **Rows**: {len(st.session_state.cleaned_df):,}")
                    st.write(f"• **Columns**: {len(st.session_state.cleaned_df.columns)}")
                    st.write(f"• **Numeric**: {len(numeric_cols)}")
                    st.write(f"• **Categorical**: {len(categorical_cols)}")

            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("Please ensure your file is properly formatted")
        else:
            st.markdown("""
            <div class="placeholder-container">
                <h3>✨ Ready to Explore Your Data?</h3>
                <p style="color: #666; font-size: 1.1rem;">Upload a CSV or Excel file to start your EDA journey!</p>
                <p style="color: #888; font-size: 0.95rem;">Supported formats: CSV, XLSX, XLS</p>
                <hr style="margin: 2rem 0;">
                <p style="font-weight: 600;">📊 What you'll discover:</p>
                <p>✓ Complete data cleaning with before/after comparison<br>
                ✓ Multiple cleaning methods (columns, missing values, outliers)<br>
                ✓ Interactive Plotly visualizations<br>
                ✓ Statistical summaries & insights<br>
                ✓ Correlation analysis & pattern detection</p>
            </div>
            """, unsafe_allow_html=True)

    # ========== Tab 2: Theory Library ==========
    with tabs[1]:
        st.markdown("## 📚 Data Science Theory Library")
        st.markdown("Explore fundamental concepts with comprehensive explanations, visuals, and interactive quizzes")

        theory_topics = [
            "Need for Data Science", "Benefits & Uses", "Facets of Data",
            "Data Science Process", "Setting Research Goal", "Retrieving Data",
            "Significance of EDA", "Making Sense of Data", "Software Tools for EDA",
            "Visual Aids for EDA"
        ]

        selected_topic = st.selectbox("📖 Select a topic to explore", theory_topics)

        if selected_topic:
            # Initialize mode for this topic
            mode_key = f"mode_{selected_topic.replace(' ', '_')}"
            if mode_key not in st.session_state:
                st.session_state[mode_key] = "theory"
            
            # Create toggle buttons for MODE selection
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                theory_btn_style = "🎯 Take Quiz" if st.session_state[mode_key] == "theory" else ""
                if st.button("📖 Read Theory", use_container_width=True, key=f"{mode_key}_theory_btn"):
                    st.session_state[mode_key] = "theory"
                    st.rerun()
            with col2:
                quiz_btn_style = "🎯 Take Quiz" if st.session_state[mode_key] == "quiz" else ""
                if st.button("🎯 Take Quiz", use_container_width=True, key=f"{mode_key}_quiz_btn"):
                    st.session_state[mode_key] = "quiz"
                    st.rerun()
            
            st.markdown("---")
            
            # ===== THEORY MODE =====
            if st.session_state[mode_key] == "theory":
                content = get_theory_content(selected_topic)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📖 Theory Content")
                    st.markdown(content['content'])
                
                with col2:
                    st.markdown("### 📷 Illustration")
                    try:
                        st.image(content['image'], use_container_width=True, caption=selected_topic)
                    except Exception as e:
                        st.markdown("""
                        <div style="text-align: center; padding: 2rem; background: #f0f0f0; border-radius: 12px; border: 2px dashed #ccc;">
                        <p style="color: #666; font-size: 1.2rem;">📷 Illustration</p>
                        <p style="color: #999; font-size: 0.9rem;">Loading image...</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # ===== QUIZ MODE =====
            elif st.session_state[mode_key] == "quiz":
                quiz_questions = get_quiz_questions(selected_topic)
                
                if quiz_questions:
                    st.markdown(f"### 🎯 Quiz: {selected_topic}")
                    st.markdown(f"**Total Questions: {len(quiz_questions)}**")
                    st.info("💡 Read all questions carefully and select your answers before submitting.")
                    st.markdown("---")
                    
                    # Initialize quiz session state
                    quiz_key = f"quiz_{selected_topic.replace(' ', '_')}"
                    if quiz_key not in st.session_state:
                        st.session_state[quiz_key] = {
                            'answers': {},
                            'submitted': False,
                            'score': 0
                        }
                    
                    quiz_state = st.session_state[quiz_key]
                    
                    # Initialize all question keys in session state
                    for idx in range(1, len(quiz_questions) + 1):
                        answer_key = f"{quiz_key}_answer_{idx}"
                        if answer_key not in st.session_state:
                            st.session_state[answer_key] = None
                    
                    # Display questions
                    for idx, q in enumerate(quiz_questions, 1):
                        st.markdown(f"#### Question {idx}/{len(quiz_questions)}")
                        st.markdown(f"**{q['question']}**")
                        st.markdown("")
                        
                        # Radio buttons for options - NO DEFAULT SELECTION
                        answer_key = f"{quiz_key}_answer_{idx}"
                        
                        user_answer = st.radio(
                            f"Answer for Q{idx}",
                            options=range(len(q['options'])),
                            format_func=lambda x: q['options'][x],
                            key=answer_key,
                            label_visibility="collapsed",
                            index=None  # No default selection
                        )
                        
                        if user_answer is not None:
                            quiz_state['answers'][idx-1] = user_answer
                        else:
                            # Remove answer if user deselected it
                            if idx-1 in quiz_state['answers']:
                                del quiz_state['answers'][idx-1]
                        
                        # Show answer feedback if submitted
                        if quiz_state['submitted']:
                            if idx-1 in quiz_state['answers']:
                                user_ans = quiz_state['answers'][idx-1]
                                if user_ans == q['correct']:
                                    st.success(f"✅ **Correct!** {q['explanation']}")
                                else:
                                    st.error(f"❌ **Incorrect!** The correct answer is: **{q['options'][q['correct']]}**")
                                    st.info(f"💡 {q['explanation']}")
                        
                        st.markdown("---")
                    
                    # Submit button
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        if st.button("✅ Submit Quiz", use_container_width=True, key=f"{quiz_key}_submit"):
                            # Check if all questions are answered
                            if len(quiz_state['answers']) == len(quiz_questions):
                                score = 0
                                for idx, q in enumerate(quiz_questions):
                                    if quiz_state['answers'].get(idx) == q['correct']:
                                        score += 1
                                
                                quiz_state['submitted'] = True
                                quiz_state['score'] = score
                                st.rerun()
                            else:
                                st.error(f"❌ Please answer all {len(quiz_questions)} questions before submitting!")
                                st.info(f"📝 You have answered {len(quiz_state['answers'])} out of {len(quiz_questions)} questions.")
                    
                    with col2:
                        if st.button("🔄 Reset Quiz", use_container_width=True, key=f"{quiz_key}_reset"):
                            st.session_state[quiz_key] = {
                                'answers': {},
                                'submitted': False,
                                'score': 0
                            }
                            st.rerun()
                    
                    # Display score if submitted
                    if quiz_state['submitted']:
                        st.markdown("---")
                        score_percentage = (quiz_state['score'] / len(quiz_questions)) * 100
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Your Score", f"{quiz_state['score']}/{len(quiz_questions)}")
                        
                        with col2:
                            st.metric("Percentage", f"{score_percentage:.1f}%")
                        
                        with col3:
                            if score_percentage >= 80:
                                st.success("🏆 Excellent!")
                            elif score_percentage >= 60:
                                st.info("👍 Good job!")
                            else:
                                st.warning("📚 Keep studying!")
                        
                        with st.expander("📊 Detailed Results", expanded=False):
                            for idx, q in enumerate(quiz_questions, 1):
                                user_ans = quiz_state['answers'].get(idx-1)
                                is_correct = user_ans == q['correct']
                                status = "✅" if is_correct else "❌"
                                st.write(f"{status} **Q{idx}: {q['question']}**")
                                if user_ans is not None:
                                    st.write(f"   📍 Your answer: {q['options'][user_ans]}")
                                if not is_correct:
                                    st.write(f"   ✔️ Correct answer: {q['options'][q['correct']]}")
                                st.write(f"   💡 {q['explanation']}")
                                st.markdown("---")
                else:
                    st.info("No quiz available for this topic yet")


    # ========== Tab 3: About ==========
    with tabs[2]:
        st.markdown("## ℹ️ About This Platform")
        st.markdown("""
        <div class="card">
            <h3>🎓 Educational Platform for First-Year Data Science</h3>
            
            <h4>✨ Key Features:</h4>
            <ul>
                <li><strong>Interactive EDA Studio</strong> - Upload datasets and apply cleaning techniques</li>
                <li><strong>Before/After Comparison</strong> - See real-time impact of each operation</li>
                <li><strong>Multiple Cleaning Methods</strong> - Column ops, missing values, outliers, text standardization</li>
                <li><strong>Cleaning Log</strong> - Track all operations performed</li>
                <li><strong>Theory Library</strong> - Fundamental concepts with visual aids</li>
                <li><strong>Interactive Visualizations</strong> - Plotly charts for deep exploration</li>
                <li><strong>Smart Insights</strong> - Automatic data quality detection</li>
            </ul>
            
            <h4>🧹 Cleaning Methods:</h4>
            <ul>
                <li><strong>Column Operations</strong> - Names, whitespace, data types</li>
                <li><strong>Data Operations</strong> - Duplicates, missing values</li>
                <li><strong>Advanced</strong> - Outliers, text standardization, categories</li>
            </ul>
            
            <h4>🔧 Built With:</h4>
            <ul>
                <li>Streamlit - Interactive web framework</li>
                <li>Pandas - Data manipulation</li>
                <li>Plotly - Interactive visualizations</li>
                <li>NumPy - Numerical computing</li>
            </ul>
            
            <h4>🎯 Learning Outcomes:</h4>
            <ul>
                <li>Master the complete data science workflow</li>
                <li>Apply professional data cleaning techniques</li>
                <li>Perform exploratory data analysis independently</li>
                <li>Create and interpret various visualizations</li>
                <li>Handle real-world data quality issues</li>
                <li>Apply statistical concepts to datasets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="font-size: 1.1rem; font-weight: 600;">📊 Data Science Playground</p>
        <p>Interactive Learning Platform for First-Year Data Science Students</p>
        <p style="font-size: 0.9rem; color: #999; margin-top: 1rem;">Built with Streamlit, Pandas, and Plotly | Complete EDA Automation</p>
        <p style="font-size: 0.85rem; color: #bbb;">© 2024-2026 Data Science Education</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
