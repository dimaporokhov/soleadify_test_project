import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common.conf import FB_FILE_NAME, GOOGLE_FILE_NAME, WEB_FILE_NAME, \
    RAW_FOLDER, TRANSFORM_FOLDER
from common.helper import get_project_path

PROJECT_PATH = get_project_path()

RAW_WEB_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, WEB_FILE_NAME)
TRANSFORM_WEB_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, WEB_FILE_NAME)

RAW_FB_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, FB_FILE_NAME)
TRANSFORM_FB_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, FB_FILE_NAME)

RAW_GOOGLE_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, GOOGLE_FILE_NAME)
TRANSFORM_GOOGLE_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, GOOGLE_FILE_NAME)


def unique_values_percent(path: str):
    df = pd.read_csv(path)
    unique_percentage = (df.nunique() / len(df)) * 100

    # Plot the percentage of unique values
    plt.figure(figsize=(10, 5))
    sns.barplot(x=unique_percentage.index, y=unique_percentage.values)
    plt.title('Percentage of Unique Values')
    plt.ylabel('Percentage')
    plt.xlabel('Columns')
    plt.xticks(rotation=90)

    # Show the plot
    plt.tight_layout()
    plt.show()


def nan_percent(path):
    df = pd.read_csv(path)
    nan_percentage = (df.isna().sum() / len(df)) * 100

    # Plot the percentage of NaN values
    plt.figure(figsize=(10, 5))
    sns.barplot(x=nan_percentage.index, y=nan_percentage.values)
    plt.title('Percentage of NaN Values')
    plt.ylabel('Percentage')
    plt.xlabel('Columns')
    plt.xticks(rotation=90)

    # Show the plot
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    unique_values_percent(RAW_WEB_PATH)
    unique_values_percent(RAW_FB_PATH)
    unique_values_percent(RAW_GOOGLE_PATH)

    nan_percent(TRANSFORM_WEB_PATH)
    nan_percent(TRANSFORM_FB_PATH)
    nan_percent(TRANSFORM_GOOGLE_PATH)
