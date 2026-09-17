# 🤖 AI Business Intelligence Copilot

An AI-powered Business Intelligence application built on the **Olist Brazilian E-Commerce dataset** to transform raw e-commerce data into actionable business insights.

The project combines **Python, SQL, Power BI, Machine Learning, Data Quality Monitoring, and LLM-based business analysis** in a single analytics workflow.

---

## 🎯 Project Overview

The **AI Business Intelligence Copilot** allows business users to ask questions in natural language and receive data-driven insights about:

* Revenue performance
* Customer behavior
* Customer retention risk
* Product performance
* Seller performance
* Delivery performance
* Data quality
* Revenue forecasting

Instead of manually exploring multiple datasets, users can ask business questions directly through the Copilot interface.

---

## 💼 Business Problem

E-commerce businesses generate large amounts of data across customers, orders, products, sellers, payments, and deliveries.

The challenge is to convert this raw data into useful business information such as:

* Which products generate the most revenue?
* Which customers are at risk?
* Which sellers have delivery problems?
* Which products have high demand but low value?
* What is the expected revenue for the next day?
* Are there data-quality problems affecting analysis?

This project addresses these questions through an integrated BI and AI solution.

---

## 💡 Solution

The project follows this workflow:

```text
Olist E-Commerce Data
        ↓
Data Cleaning & Validation
        ↓
SQL / Python Analytics
        ↓
Business Metrics
        ↓
Machine Learning
        ↓
Power BI Dashboards
        ↓
AI Business Copilot
        ↓
Business Insights & Actions
```

---

## 🛠️ Tech Stack

| Technology       | Purpose                                |
| ---------------- | -------------------------------------- |
| Python           | Data analysis and business logic       |
| Pandas           | Data cleaning and transformation       |
| NumPy            | Numerical analysis                     |
| MySQL / SQL      | Data querying and analysis             |
| Power BI         | Interactive dashboards                 |
| Scikit-learn     | Machine learning                       |
| Random Forest    | Revenue forecasting                    |
| Streamlit        | Copilot web interface                  |
| OpenAI API       | Natural-language business explanations |
| Jupyter Notebook | Data exploration                       |
| Git / GitHub     | Version control and portfolio          |

---

# 📊 Business Intelligence Features

## 💰 Revenue Intelligence

The project analyzes:

* Total revenue
* Monthly revenue
* Revenue trends
* Revenue changes
* Business performance
* Revenue decline explanations

Example questions:

```text
Why did revenue decline in June 2018?
What happened to revenue in May 2018?
```

---

# 👥 Customer Intelligence

Customer analysis uses customer-level purchase behavior and RFM-based segmentation.

### Customer Segments

* VIP
* Loyal
* Potential Loyal
* At Risk
* Lost

### Supported Questions

```text
How many VIP customers do we have?
Which customers are at risk?
What is our customer retention risk?
Which customers should we prioritize for retention?
```

The system can identify customers based on:

* Recency
* Frequency
* Monetary value
* Retention risk
* Priority score

---

# 📦 Product Intelligence

Product performance is analyzed using:

* Revenue
* Units sold
* Average price
* Product classification

### Product Categories

Products can be classified as:

* Business Winner
* Premium Product
* High Demand - Low Value
* Low Performer

### Supported Questions

```text
What are the top 10 products by revenue?
Which products are business winners?
Which products have high demand but low value?
```

---

# 🏆 Seller Intelligence

Seller performance is evaluated using:

* Revenue
* Order volume
* Average order value
* Delivery performance
* Late delivery rate
* Performance score

### Seller Analysis

The Copilot can identify:

* Top-performing sellers
* Risky sellers
* Sellers with high late-delivery rates

Example questions:

```text
Which sellers are top performers?
Show me the top 10 risky sellers.
Which sellers have the highest late delivery rate?
```

---

# 🔎 Data Quality Monitor

A dedicated data-quality engine checks multiple datasets for potential issues.

The system evaluates:

* Missing values
* Duplicate keys
* Data types
* Date logic
* Outliers
* Business-key behavior
* Dataset-level quality status

The project also generates a consolidated:

```text
master_quality_report_final.csv
```

This report is visualized through Power BI.

---

# 📈 Revenue Forecasting

The project includes a machine-learning based **next-day revenue forecasting system**.

### Approach

Historical daily revenue is transformed into time-series features such as:

* Previous-day revenue
* Previous-week revenue
* Rolling 7-day revenue
* Rolling 7-day orders
* Rolling 7-day units
* Calendar features

A chronological train/test split is used to avoid future-data leakage.

### Model

A Random Forest regression model is used for daily revenue forecasting.

The saved model is:

```text
models/daily_revenue_forecast_model.pkl
```

The Copilot can answer:

```text
What will tomorrow's revenue be?
Can you predict the next day's revenue?
What is the revenue forecast?
How accurate is the revenue forecast model?
```

---

# 🤖 AI Business Copilot

The Copilot provides a natural-language interface for business analysis.

Users can ask questions such as:

```text
Which products are business winners?

Which customers are at risk?

Which sellers have the highest late delivery rate?

What is our customer retention risk?

What will tomorrow's revenue be?
```

The system first retrieves the appropriate analytics result and then uses an LLM to convert that result into a concise business explanation.

### AI Response Structure

```text
📊 Business Insight

💡 Why It Matters

🎯 Recommended Action
```

The LLM is instructed to use the analytics result as its source and avoid inventing business metrics.

---

# 📊 Power BI

Power BI is used to create interactive business dashboards for:

* Revenue
* Customer analysis
* Product performance
* Seller performance
* Data quality

The dashboards provide business users with visual exploration in addition to the AI Copilot.

---

# 📁 Project Structure

```text
AI-Business-Intelligence-Copilot/
│
├── .env
├── .gitignore
│
├── ai/
│   └── copilot_llm.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   ├── product_category_name_translation.csv
│   └── master_quality_report_final.csv
│
├── models/
│   └── daily_revenue_forecast_model.pkl
│
├── notebooks/
│   └── 01_data_inspection.ipynb
│
├── screenshots/
│
├── sql/
│
└── src/
    ├── business_engine.py
    ├── copilot_data.py
    ├── data_quality_engine.py
    └── intent_router.py
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <your-github-repository-url>
cd AI-Business-Intelligence-Copilot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install pandas numpy scikit-learn streamlit python-dotenv openai
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Do **not** commit `.env` to GitHub.

The project includes `.env` in `.gitignore`.

---

# ▶️ Run the Application

From the project root:

```bash
streamlit run dashboard/app.py
```

The application will open in the browser.

---

# 💬 Example Business Questions

### Revenue

```text
Why did revenue decline in June 2018?
What happened to revenue in May 2018?
```

### Forecasting

```text
What will tomorrow's revenue be?
How accurate is the revenue forecast model?
```

### Customer

```text
How many VIP customers do we have?
Which customers are at risk?
What is our customer retention risk?
Which customers should we prioritize for retention?
```

### Products

```text
What are the top 10 products by revenue?
Which products are business winners?
Which products have high demand but low value?
```

### Sellers

```text
Which sellers are top performers?
Show me the top 10 risky sellers.
Which sellers have the highest late delivery rate?
```

### Data Quality

```text
Are there any data quality issues?
Which datasets have the most quality issues?
Show me the quality report.
```

---

# 📌 Key Project Insights

The analysis identified several useful business patterns, including:

* A small proportion of customers generate a large share of customer revenue.
* Customer RFM analysis can identify VIP, loyal, at-risk, and lost customer groups.
* Some sellers generate significant revenue while also showing elevated late-delivery rates.
* Product analysis separates high-revenue products from high-demand, low-value products.
* Data-quality monitoring identifies datasets requiring further review.
* Daily revenue forecasting can provide a machine-learning based estimate for the next day.

---

# 🚀 Future Improvements

Possible future improvements include:

* Automated dashboard refresh
* Advanced customer churn prediction
* Product recommendation system
* Seller anomaly detection
* Automated business alerts
* More advanced forecasting models
* Conversational Power BI integration
* Deployment to a cloud platform
* Automated data pipelines

---

# 👨‍💻 Project Objective

This project demonstrates practical skills in:

**Data Analysis → SQL → Business Intelligence → Machine Learning → Data Quality → Generative AI**

It is designed as an end-to-end portfolio project demonstrating how raw business data can be transformed into analytical insights and natural-language business intelligence.
