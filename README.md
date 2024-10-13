# Stock-quantitative-analysis-and-visualization-platform
Python Programming Assignment1  (Spring 2023)


## Project Overview

This project is a **Stock Data Analysis System** that collects, analyzes, and predicts stock data for A-share listed companies using web crawlers and machine learning techniques. The project includes functionalities for collecting historical stock prices, company profiles, financial data, and institutional forecasts. It also computes various technical indicators like Moving Averages (MA), Bollinger Bands (BOLL), and KDJ, and offers stock price trend predictions using deep learning models like LSTM.
<img width="816" alt="10f613a6952fd6bab21fe8b1635b560" src="https://github.com/user-attachments/assets/543c0711-a9c8-438b-be51-15fc3640284c">
## Features

### 1. **Data Collection (Web Crawlers)**
   - Collects real-time stock data, including:
     - Historical stock K-line data
     - Company profiles
     - Financial statement data
     - Institutional forecasts
   - Data is fetched from financial websites using Python web crawlers.

### 2. **Quantitative Calculation of Technical Indicators**
The system uses `pandas` and `numpy` to calculate stock technical indicators such as:

- Moving Average (MA)
- Bollinger Bands (BOLL)
- KDJ (Stochastic Oscillator)
- MACD (Moving Average Convergence Divergence)

### 3. **Data Visualization**

The project implements data visualization through:

- **Front-end tools:** `Bootstrap` and `Echarts`
- **Real-time rendering** of stock data trends and technical analysis

### 4. **Stock Price Prediction**

   - Uses Long Short-Term Memory (LSTM) neural networks from `tensorflow` for time-series analysis to predict stock price trends.
   - Allows comparative analysis of multiple stocks and offers stock portfolio investment suggestions.

## System Modules

### 1. **User Module**

   - **User Registration:** Allows new users to register an account.
   - **User Login:** Supports login for registered users.
   - **Password Retrieval:** Provides password reset functionality.
   - **Profile Management:** Allows users to update their profile information.

### 2. **Stock System Module**

   - **Real-time Stock Data Acquisition:** Fetches real-time data for the entered stock code.
   - **Stock Prediction using LSTM:** Predicts stock trends based on historical data using an LSTM model.
   - **Comparative Analysis of Multiple Stocks:** Enables comparison of various stocks for trend analysis.
   - **Market Visualization:** Offers graphical representation of stock trends and technical analysis.
   - **Stock Portfolio Investment Advice:** Provides suggestions for portfolio optimization based on analysis.
   - **Historical Stock Trend Visualization:** Visualizes historical stock data trends.

## Installation and Setup

### 1. **Pre-requisites**

   - Python 3.8+
   - Anaconda (recommended for managing the environment)

### 2. **Installation**

1. Clone the repository:

   ```bash
   git https://github.com/lxy0068/Stock-quantitative-analysis-and-visualization-platform.git
   cd Stock-quantitative-analysis-and-visualization-platform
   ```

2. Create a new virtual environment using conda (recommended):

   ```bash
   conda create -n StockEnv python=3.9
   conda activate StockEnv
   ```

3. Install the required dependencies by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

   The dependencies include:

   ```txt
   pandas==1.5.3
   numpy<2
   requests==2.27.1
   flask
   tensorflow==2.11.0
   scikit-learn
   tqdm
   ```

4. Set up front-end dependencies and ensure your environment supports visualization (e.g., `echarts`).

### 3. **Running the Application**

- To start the Flask web application, navigate to the root folder and run:

  ```bash
  python app.py
  ```

- The application will be accessible at `http://127.0.0.1:5000`.

## Usage Instructions

### 1. **Register/Login**

   - Users can register an account and log in to access stock analysis features.

### 2. **Stock Data Analysis**

   - Enter a stock code to fetch real-time data.
   - Visualize stock trends and technical indicators such as MA, BOLL, KDJ, and MACD.

### 3. **Stock Price Prediction**

   - Input historical data for a stock to receive a prediction of future price trends using the LSTM model.

### 4. **Comparative Analysis**

   - Analyze multiple stocks simultaneously for better decision-making.

### 5. **Investment Advice**

   - Receive stock portfolio recommendations based on technical analysis and predictions.

## Project Structure

```plaintext
stock-analysis-system/
│
├── README.md                # Project documentation
├── requirements.txt         # List of dependencies
├── user_info.db             # User information database
├── analysis_util.py         # Utility functions for data analysis
├── util.py                  # General utility functions
├── config.py                # Configuration settings
├── stock_data_crawler.py    # Script for web crawling stock data
├── app.py                   # Flask application for the web server
├── service/                 # Backend service modules
│   ├── east_money_service.py
│   └── ts_service.py
├── spider/                  # Web scraping scripts and modules
│   ├── fund/
│   │   ├── fund_history_price_spider.py
│   │   ├── fund_realtime_price.py
│   │   └── search.py
│   └── stock/
│       ├── run_fund_history_spider.py
│       └── run_stock_history_spider.py
├── static/                  # Static files (CSS, JavaScript, images)
│   ├── css/
│   ├── img/
│   ├── js/
│   └── vendor/
├── templates/               # HTML templates for rendering web pages
└── .idea/                   # PyCharm project settings
```
## License

This project is licensed under the MIT License.

## Function demonstration
### Main interface
![image](https://github.com/user-attachments/assets/1b5f6866-28ae-493e-8e98-2c73392483d4)
![image](https://github.com/user-attachments/assets/b35fb2ba-10ec-424b-8aab-fcc06ac08f09)
You can start after successful registration and login. Users who have saved before do not need to re-register.

### Market index market
![image](https://github.com/user-attachments/assets/dafc1253-42ca-432a-b04b-746f9cd21431)
![image](https://github.com/user-attachments/assets/9b7a3d77-55f2-4ae2-baea-4fd3816fdbc1)
Click to select the Shanghai Composite Index, etc. for viewing, and you can move the support bar below to view different time periods with different degrees of precision. Note that this system is real-time.

### Hot spot direction of funds
![image](https://github.com/user-attachments/assets/618f7a9a-3b67-43fe-a3f0-3d5bd54d6c65)

### Stock diagnostic analysis
![image](https://github.com/user-attachments/assets/9b3a9b57-087d-4992-aa99-f01621ec7015)
![image](https://github.com/user-attachments/assets/334e07b6-847e-4e54-b5cc-72440cf7ef66)
![image](https://github.com/user-attachments/assets/bfbf2d1e-fd46-4e3a-a888-af32ece60043)

### Stock comparison analysis
Stock comparison analysis based on technical and fundamental aspects
![image](https://github.com/user-attachments/assets/7886ce42-66c0-435c-86d1-7993b67bbfd1)
![image](https://github.com/user-attachments/assets/74e24827-9f6b-4e6d-9a8e-3423928177e1)

### Stock price time series modeling prediction
Stock price prediction based on LSTM neural network
By entering the stock code and manually debugging the model parameters, the best prediction effect can be achieved.
![image](https://github.com/user-attachments/assets/9e44da01-4de8-4c39-bf39-1bd2f9f3f461)

### Quantitative analysis of stock yield and stock diagnosis
![image](https://github.com/user-attachments/assets/05ef5fb4-7093-4e44-8277-5201f7cf4608)
![image](https://github.com/user-attachments/assets/24082343-b769-4c2c-92de-d2b857727ea9)
