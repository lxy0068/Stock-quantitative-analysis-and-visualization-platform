# Stock-quantitative-analysis-and-visualization-platform
Python Programming Assignment1  (Spring 2023)


## Project Overview

This project is a stock data analysis system designed to collect, analyze, and predict stock prices for A-share listed companies. Using web crawler technology, the system gathers various stock-related data such as historical stock prices, company profiles, financial indicators, and institutional forecasts. The data is used to compute technical indicators like KDJ and Bollinger Bands (BOLL), which assist in visualizing and predicting stock price trends using deep learning models like LSTM.
<img width="816" alt="10f613a6952fd6bab21fe8b1635b560" src="https://github.com/user-attachments/assets/543c0711-a9c8-438b-be51-15fc3640284c">
## Features

### 1. **Data Collection (Web Crawlers)**

The project uses Python-based web crawlers to collect the following data from financial websites:

- **Historical K-line data** of stocks
- **Company profiles** for listed companies
- **Financial statement data**
- **Institutional forecast data** from major financial institutions

### 2. **Quantitative Calculation of Technical Indicators**

Using Python libraries such as `pandas` and `numpy`, the system calculates key stock technical indicators:

- **Moving Average (MA)**
- **Bollinger Bands (BOLL)**
- **KDJ (Stochastic Oscillator)**
- **MACD (Moving Average Convergence Divergence)**

### 3. **Data Visualization**

The project implements data visualization through:

- **Front-end tools:** `Bootstrap` and `Echarts`
- **Real-time rendering** of stock data trends and technical analysis

### 4. **Stock Price Prediction**

Using deep learning algorithms, the system provides stock price prediction features:

- **Recurrent Neural Networks (RNNs)** are used, specifically an **LSTM** model, to predict stock price trends based on historical data.

### 5. **Stock System Module**

- **Real-time Stock Data Acquisition:** Real-time data fetching for analysis and prediction based on input stock codes.
- **Stock Prediction with LSTM:** Leveraging LSTM for time-series forecasting of stock prices.
- **Comparative Analysis of Multiple Stocks:** Perform side-by-side analysis of different stocks.
- **Market Visualization:** Clear visualization of stock movements and technical analysis.
- **Stock Portfolio Investment Advice:** Provide investment recommendations based on trends and analyses.
- **Historical Trend Visualization:** Present the stock's historical performance graphically for better insights.

## System Modules

### 1. **User Module**

- **User Registration:** New users can register an account.
- **User Login:** Registered users can log in to access features.
- **Password Retrieval:** Recover forgotten passwords via the system.
- **Profile Management:** Modify basic account information.

### 2. **Stock System Module**

- **Real-time Stock Data Acquisition:** Fetch real-time stock data for any stock code provided by the user.
- **Stock Prediction Using LSTM:** Predict future stock prices using the LSTM model based on historical market data.
- **Comparative Analysis of Multiple Stocks:** Perform analysis across different stocks and compare trends and predictions.
- **Market Visualization:** Visual representation of stock performance using Echarts.
- **Stock Portfolio Investment Advice:** Offer investment strategy suggestions based on trends and performance.
- **Historical Stock Trend Visualization:** Display graphical trends over time for stock price movements.



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

## License

This project is licensed under the MIT License.
