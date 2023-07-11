# Belgian Real Estate - Data Analysis / Visualisation

## Project description

This is the second stage of a larger project to create a Machine Learning (ML) model to predict sale prices of real estate properties in Belgium. The first stage of the project which consisted on building the dataset using a scraper can be viewed [here](https://github.com/feldeh/immoweb-scraper).

## Objective

The main objective is to use our dataset to analyse the Belgian real estate market to find patterns and relationships in our data. In order to achieve that we will be using the [**pandas**](https://pandas.pydata.org/) python library for data manipulation and the [**seaborn**](https://seaborn.pydata.org/) library for data visualisation.

### Data Cleaning

The first step was to clean the dataset in order to improve the accurancy of our analysis.

The data cleaning process involved the following:

- Removing parameters that were irrelevant, contained constant value or had a small sample size.
- Removing rows that contained missing values on the most important parameters such as `price` or `netHabitableSurface`.
- Removing duplicates based on matching `latitude`, `longitude`, `price`, `street`, `postalCode` and `number`.
- Imputing missing values to False for certain parameters such as `hasGarden`.

The raw dataset contained 19980 rows and 52 columns, which was reduced to 15872 rows and 38 columns after the cleaning.

### Data Analysis

This part was centered around exploring the dataset by visualising the `price` correlations and the `price` distribution accross the different regions of Belgium after removing outliers. The visualisations and their interpretations can be consulted in [notebooks/data_analysis.ipynb](https://github.com/feldeh/immoweb-data-analysis/blob/main/notebooks/data_analysis.ipynb)

## Installation

If you wish to manipulate the dataset and play around with the notebook follow these steps:

1. Clone the [immoweb-data-analysis](https://github.com/feldeh/immoweb-data-analysis) repository
2. Navigate to the root of the repository
3. Install the required libraries by running `pip install -r requirements.txt`

## Timeline

This project lasted 4 days, starting from the 06/07/2023 and ending on the 11/07/2023.

It was completed by [Félicien De Hertogh](https://www.linkedin.com/in/feliciendehertogh/) as part of the Data and AI training at [BeCode.org](https://becode.org/) under the supervision of [Vanessa Rivera Quiñones](https://www.linkedin.com/in/vriveraq/) and [Samuel Borms](https://www.linkedin.com/in/sam-borms/?originalSubdomain=be).
