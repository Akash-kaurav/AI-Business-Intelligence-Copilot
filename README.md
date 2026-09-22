ðŸ¤– AI Business Intelligence Copilot

An AI-powered Business Intelligence application built on the Olist
Brazilian E-Commerce dataset to transform raw e-commerce data into
actionable business insights.

The project combines Python, SQL, Power BI, Machine Learning, Data
Quality Monitoring, Streamlit, and LLM-based business analysis into an
end-to-end analytics workflow.

ðŸŽ¯ Project Overview

The AI Business Intelligence Copilot allows business users to ask
questions in natural language and receive data-driven insights about:

Revenue performance

Customer behavior and retention risk

Product performance

Seller performance

Delivery performance

Data quality

Revenue forecasting

Instead of manually exploring multiple datasets, users can ask business
questions directly through the Copilot interface.

ðŸ’¼ Business Problem

E-commerce businesses generate large amounts of data across customers,
orders, products, sellers, payments, reviews, and deliveries.

The challenge is to convert this raw data into useful business
information such as:

Which products generate the most revenue?

Which customers are at risk?

Which sellers have delivery problems?

Which products have high demand but low value?

What is the expected revenue for the next day?

Are data-quality problems affecting analysis?

This project addresses these questions through an integrated BI and AI
solution.

ðŸ’¡ Solution Architecture

Olist E-Commerce Data
        â†“
Data Cleaning & Validation
        â†“
Python / SQL Analytics
        â†“
Business Metrics & Intelligence
        â†“
Machine Learning
        â†“
Power BI Data Quality Dashboard
        â†“
AI Business Copilot
        â†“
Business Insights & Recommended Actions

ðŸ› ï¸ Tech Stack

Technology         Purpose

Python             Data analysis and business logic
Pandas             Data cleaning and transformation
NumPy              Numerical analysis
MySQL / SQL        Data querying and analysis
Power BI           Data-quality and business visualization
Scikit-learn       Machine learning
Random Forest      Daily revenue forecasting
Streamlit          AI Copilot web interface
OpenAI API         Natural-language business explanations
Jupyter Notebook   Data exploration
Git / GitHub       Version control and portfolio

ðŸ“Š Business Intelligence Features

ðŸ’° 1. Revenue Intelligence

The project analyzes:

Total revenue

Monthly revenue

Revenue trends

Revenue changes

Business performance

Revenue decline explanations

Example questions

Why did revenue decline in June 2018?

What happened to revenue in May 2018?

The Copilot retrieves the relevant analytics result and converts it into
a concise business explanation.

ðŸ‘¥ 2. Customer Intelligence

Customer analysis uses purchase behavior and RFM-based segmentation.

Customer Segments

VIP

Loyal

Potential Loyal

At Risk

Lost

Supported Questions

How many VIP customers do we have?

Which customers are at risk?

What is our customer retention risk?

Which customers should we prioritize for retention?

The analysis considers:

Recency

Frequency

Monetary value

Retention risk

Priority score

ðŸ“¦ 3. Product Intelligence

Product performance is analyzed using:

Revenue

Units sold

Average price

Product classification

Product Classification

Products can be classified as:

Business Winner

Premium Product

High Demand - Low Value

Low Performer

Supported Questions

What are the top 10 products by revenue?

Which products are business winners?

Which products have high demand but low value?

This helps separate products that generate both strong revenue and
volume from products that sell frequently but generate comparatively
lower value.

ðŸ† 4. Seller Intelligence

Seller performance is evaluated using:

Revenue

Order volume

Average order value

Delivery performance

Late delivery rate

Performance score

Seller Analysis

The Copilot can identify:

Top-performing sellers

Risky sellers

Sellers with high late-delivery rates

Example Questions

Which sellers are top performers?

Show me the top 10 risky sellers.

Which sellers have the highest late delivery rate?

ðŸ”Ž 5. Data Quality Monitor

A dedicated data-quality engine checks multiple datasets for potential
issues.

The system evaluates:

Missing values

Duplicate keys

Data types

Date logic

Statistical outliers

Business-key behavior

Dataset-level quality status

The project also generates a consolidated report:

master_quality_report_final.csv

This report is visualized through the Power BI Data Quality Monitoring
& Business Validation dashboard.

Dashboard Screenshot



ðŸ“ˆ 6. Revenue Forecasting

The project includes a machine-learning based next-day revenue
forecasting system.

Approach

Historical daily revenue is transformed into time-series features such
as:

Previous-day revenue

Previous-week revenue

Rolling 7-day revenue

Rolling 7-day orders

Rolling 7-day units

Calendar features

A chronological train/test split is used to reduce the risk of
future-data leakage.

Model

A Random Forest regression model is used for daily revenue
forecasting.

Saved model:

models/daily_revenue_forecast_model.pkl

Supported Questions

What will tomorrow's revenue be?

Can you predict the next day's revenue?

What is the revenue forecast?

How accurate is the revenue forecast model?

ðŸ¤– AI Business Copilot

The Copilot provides a natural-language interface for business analysis.

Users can ask questions such as:

Which products are business winners?

Which customers are at risk?

Which sellers have the highest late delivery rate?

What is our customer retention risk?

What will tomorrow's revenue be?

How It Works

User Question
      â†“
Intent Detection
      â†“
Relevant Analytics Engine
      â†“
Business Result
      â†“
LLM Explanation
      â†“
Business Insight

The system first retrieves the appropriate analytics result and then
uses an LLM to convert that result into a concise business explanation.

AI Response Structure

ðŸ“Š Business Insight

ðŸ’¡ Why It Matters

ðŸŽ¯ Recommended Action

The LLM is instructed to use the analytics result as its source and
avoid inventing business metrics or unsupported facts.

ðŸ–¼ï¸ Project Screenshots

### Revenue Intelligence

[View Revenue Intelligence Screenshot](screenshots/revenue_intelligence.pdf)

### Customer Intelligence

[View Customer Intelligence Screenshot](screenshots/customer_intelligence.pdf)

### Seller Intelligence

[View Seller Intelligence Screenshot](screenshots/seller_intelligence.pdf)

### Product Intelligence

[View Product Intelligence Screenshot](screenshots/product_intelligence.pdf)

### Data Quality Dashboard

[View Data Quality Dashboard Screenshot](screenshots/data_quality_dashboard.pdf)
Project Structure

AI-Business-Intelligence-Copilot/
â”‚
â”œâ”€â”€ .env
â”œâ”€â”€ .gitignore
â”œâ”€â”€ README.md
â”‚
â”œâ”€â”€ ai/
â”‚   â””â”€â”€ copilot_llm.py
â”‚
â”œâ”€â”€ dashboard/
â”‚   â””â”€â”€ app.py
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ olist_customers_dataset.csv
â”‚   â”œâ”€â”€ olist_geolocation_dataset.csv
â”‚   â”œâ”€â”€ olist_order_items_dataset.csv
â”‚   â”œâ”€â”€ olist_order_payments_dataset.csv
â”‚   â”œâ”€â”€ olist_order_reviews_dataset.csv
â”‚   â”œâ”€â”€ olist_orders_dataset.csv
â”‚   â”œâ”€â”€ olist_products_dataset.csv
â”‚   â”œâ”€â”€ olist_sellers_dataset.csv
â”‚   â”œâ”€â”€ product_category_name_translation.csv
â”‚   â””â”€â”€ master_quality_report_final.csv
â”‚
â”œâ”€â”€ models/
â”‚   â””â”€â”€ daily_revenue_forecast_model.pkl
â”‚
â”œâ”€â”€ notebooks/
â”‚   â””â”€â”€ 01_data_inspection.ipynb
â”‚
â”œâ”€â”€ screenshots/
â”‚   â”œâ”€â”€ data_quality_dashboard.png
â”‚   â”œâ”€â”€ revenue_intelligence.png
â”‚   â”œâ”€â”€ customer_intelligence.png
â”‚   â”œâ”€â”€ seller_intelligence.png
â”‚   â””â”€â”€ product_intelligence.png
â”‚
â””â”€â”€ src/
    â”œâ”€â”€ business_engine.py
    â”œâ”€â”€ copilot_data.py
    â”œâ”€â”€ data_quality_engine.py
    â””â”€â”€ intent_router.py

Security: .env is kept local and should never be committed to
GitHub.

âš™ï¸ Installation

1. Clone the repository

git clone https://github.com/Akash-kaurav/AI-Business-Intelligence-Copilot.git
cd AI-Business-Intelligence-Copilot

2. Create a virtual environment

python -m venv venv

Windows

venv\Scripts\activate

3. Install dependencies

pip install pandas numpy scikit-learn streamlit python-dotenv openai

If your local environment uses additional packages from the project,
install those packages as well.

ðŸ” Environment Variables

Create a local .env file:

OPENAI_API_KEY=your_api_key_here

Never commit your API key to GitHub.

The project uses .gitignore to keep .env out of version control.

â–¶ï¸ Run the Application

From the project root:

streamlit run dashboard/app.py

The application will open in the browser.

ðŸ’¬ Example Business Questions

Revenue

Why did revenue decline in June 2018?

What happened to revenue in May 2018?

Forecasting

What will tomorrow's revenue be?

How accurate is the revenue forecast model?

Customer

How many VIP customers do we have?

Which customers are at risk?

What is our customer retention risk?

Which customers should we prioritize for retention?

Products

What are the top 10 products by revenue?

Which products are business winners?

Which products have high demand but low value?

Sellers

Which sellers are top performers?

Show me the top 10 risky sellers.

Which sellers have the highest late delivery rate?

Data Quality

Are there any data quality issues?

Which datasets have the most quality issues?

Show me the quality report.

ðŸ“Œ Key Project Insights

The analysis demonstrates several useful business patterns:

Customer RFM analysis can identify VIP, loyal, potential-loyal,
at-risk, and lost customer groups.

A relatively small group of high-value customers contributes a
substantial share of customer revenue.

Some sellers generate significant revenue while also showing
elevated late-delivery rates.

Product analysis separates high-revenue products from high-demand,
lower-value products.

Data-quality monitoring identifies datasets and checks that require
investigation.

Daily revenue forecasting can provide a machine-learning based
estimate for the next day.

ðŸš€ Future Improvements

Possible future improvements include:

Automated dashboard refresh

Advanced customer churn prediction

Product recommendation system

Seller anomaly detection

Automated business alerts

More advanced forecasting models

Conversational Power BI integration

Cloud deployment

Automated data pipelines

ðŸ‘¨â€ðŸ’» Project Objective

This project demonstrates practical skills across:

Data Analysis
      â†“
SQL
      â†“
Business Intelligence
      â†“
Machine Learning
      â†“
Data Quality
      â†“
Generative AI

The objective is to demonstrate how raw business data can be transformed
into analytical insights, forecasts, data-quality findings, and
natural-language business intelligence through a single end-to-end
portfolio project.

ðŸ“š Dataset

Olist Brazilian E-Commerce Public Dataset

The dataset contains anonymized Brazilian e-commerce data covering
customers, orders, products, sellers, payments, reviews, and related
information.

Dataset source:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

