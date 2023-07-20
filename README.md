# Belgian Real Estate - Machine Learning Project

## Project description

This is the third stage of a larger project to create a Machine Learning (ML) model to predict sale prices of real estate properties in Belgium. The first stage of the project, which consisted of building the dataset using a scraper. The second stage involved data cleaning and analysis.

In this stage, we are going to implement two types of machine learning models to predict property prices. These models are Linear Regression and XGBoost.

## Objective

The main objective is to use our cleaned dataset to train machine learning models that can accurately predict the sale prices of real estate properties in Belgium.

## Methodology

1. **Data Splitting**: We split the data into training and testing datasets for model evaluation. We also split the data based on the type of property (House or Apartment).

2. **Feature Scaling**: We scale the features in the dataset using a MinMaxScaler to ensure that all features have the same scale. This improves the performance of our models.

3. **Model Training**: We train a Linear Regression model and an XGBoost model on the training data.

4. **Model Evaluation**: We evaluate the performance of our models on the testing data using Mean Squared Error (MSE) and model score (R^2).

## Installation

If you wish to manipulate the dataset and play around with the notebook follow these steps:

1. Clone the [immoweb-data-analysis](https://github.com/feldeh/immoweb-data-analysis) repository
2. Navigate to the root of the repository
3. Install the required libraries by running `pip install -r requirements.txt`

## Timeline

This project lasted 4 days, starting from the 17/07/2023 and ending on the 20/07/2023.

It was completed by [Félicien De Hertogh](https://www.linkedin.com/in/feliciendehertogh/) as part of the Data and AI training at [BeCode.org](https://becode.org/) under the supervision of [Vanessa Rivera Quiñones](https://www.linkedin.com/in/vriveraq/) and [Samuel Borms](https://www.linkedin.com/in/sam-borms/?originalSubdomain=be).
