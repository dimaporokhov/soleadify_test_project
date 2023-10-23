import os
import re

import numpy as np
import pandas as pd

from common.conf import FB_FILE_NAME, GOOGLE_FILE_NAME, WEB_FILE_NAME, \
    RAW_FOLDER, TRANSFORM_FOLDER, COMPANY_SUFFIXES_LIST
from common.helper import get_project_path, escape_special_characters

PROJECT_PATH = get_project_path()

RAW_WEB_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, WEB_FILE_NAME)
TRANSFORM_WEB_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, WEB_FILE_NAME)

RAW_FB_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, FB_FILE_NAME)
TRANSFORM_FB_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, FB_FILE_NAME)

RAW_GOOGLE_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, GOOGLE_FILE_NAME)
TRANSFORM_GOOGLE_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, GOOGLE_FILE_NAME)

DOMAIN_CHECK_RE = r'^[a-z0-9._-]*$'
DOMAIN_SUFFIX_CHECK_RE = r'^[a-z0-9._-]*$'
PHONE_CHECK_RE = r'^[0-9E.+]*$'


def transform_web():
    """TRANSFORM WEB DATASET"""

    print('READING WEB DATASET:')
    web_df = pd.read_csv(RAW_WEB_PATH)
    print(web_df.info())

    print('STARTING CLEANING AND TRANSFORMATIONS:')
    # columns renaming
    web_rename_mapping = {
        "root_domain": "domain",
        "legal_name": "company_name",
        "main_city": "city",
        "main_country": "country",
        "main_region": "region",
        "s_category": "category"
    }
    web_df.rename(web_rename_mapping, axis=1, inplace=True)

    # to lowercase
    web_lowercase_cols_list = [
        "domain", "domain_suffix", "language", "company_name",
        "city", "country", "region", "site_name", "tld", "category"
    ]
    for col in web_lowercase_cols_list:
        web_df[col] = web_df[col].str.lower()

    # escape special characters
    web_escape_cols_list = [
        "language", "company_name", "city", "country",
        "region", "site_name", "tld", "category"
    ]
    for col in web_escape_cols_list:
        web_df[col] = web_df[col].apply(
            lambda x: np.nan if x is np.nan else escape_special_characters(str(x))
        )
        if col == "company_name":
            for suffix in COMPANY_SUFFIXES_LIST:
                web_df[col] = web_df[col].str.replace(suffix, "")

    # filter df
    web_df = web_df[
        web_df['domain'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_CHECK_RE, x))
        )
    ]
    web_df = web_df[
        web_df['domain_suffix'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_SUFFIX_CHECK_RE, x))
        )
    ]
    web_df = web_df[
        web_df['phone'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(PHONE_CHECK_RE, x))
        )
    ]

    web_df.dropna(subset=['domain'], inplace=True)

    # cast columns
    web_df['phone'] = web_df['phone'].astype(float, errors='ignore').astype(int, errors='ignore')

    # drop duplicates
    web_df.drop_duplicates(inplace=True)

    print(web_df.info())
    print(web_df)

    print(f"WRITING TRANSFORMED WEB DF TO {TRANSFORM_WEB_PATH}")
    web_df.to_csv(TRANSFORM_WEB_PATH, index=False)


def transform_fb():
    """TRANSFORM FB DATASET"""
    print('READING FB DATASET:')
    fb_df = pd.read_csv(RAW_FB_PATH)
    print(fb_df.info())

    print('STARTING CLEANING AND TRANSFORMATIONS:')
    # columns renaming
    fb_rename_mapping = {
        "country_name": "country",
        "name": "company_name",
        "region_name": "region"
    }
    fb_df.rename(fb_rename_mapping, axis=1, inplace=True)

    # to lowercase
    fb_lowercase_cols_list = [
        "domain", "categories", "city", "country_code",
        "country", "email", "link", "company_name", "page_type",
        "phone_country_code", "region_code", "region"
    ]
    for col in fb_lowercase_cols_list:
        fb_df[col] = fb_df[col].str.lower()

    # exploding categories into multiple rows
    fb_df = fb_df\
        .assign(
            category=fb_df['categories'].str.split('|')
        )\
        .explode('category')\
        .reset_index(drop=True)

    fb_df.drop('categories', axis=1, inplace=True)

    # escape special characters
    fb_escape_cols_list = [
        "category", "city", "country_code",
        "country", "company_name", "page_type",
        "phone_country_code", "region_code", "region"
    ]
    for col in fb_escape_cols_list:
        fb_df[col] = fb_df[col].apply(
            lambda x: np.nan if x is np.nan else escape_special_characters(str(x))
        )
        if col == "company_name":
            for suffix in COMPANY_SUFFIXES_LIST:
                fb_df[col] = fb_df[col].str.replace(suffix, "")

    # filter df
    fb_df = fb_df[
        fb_df['domain'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_CHECK_RE, x))
        )
    ]
    fb_df.dropna(subset=['domain'], inplace=True)

    # drop duplicates
    fb_df.drop_duplicates(inplace=True)

    print(fb_df.info())
    print(fb_df)

    print(f"WRITING TRANSFORMED FB DF TO {TRANSFORM_FB_PATH}")
    fb_df.to_csv(TRANSFORM_FB_PATH, index=False)


def transform_google():
    # TRANSFORM GOOGLE DATASET
    print('READING GOOGLE DATASET:')
    google_df = pd.read_csv(RAW_GOOGLE_PATH)
    print(google_df.info())
    print('STARTING CLEANING AND TRANSFORMATIONS:')

    # columns renaming
    google_rename_mapping = {
        "country_name": "country",
        "name": "company_name",
        "region_name": "region"
    }
    google_df.rename(google_rename_mapping, axis=1, inplace=True)

    # to lowercase
    google_lowercase_cols_list = [
        "domain", "category", "city", "country_code", "country",
        "company_name", "phone_country_code", "region_code", "region"
    ]
    for col in google_lowercase_cols_list:
        google_df[col] = google_df[col].str.lower()

    # escape special characters
    google_escape_cols_list = [
        "category", "city", "country_code", "country",
        "company_name", "phone_country_code", "region_code", "region"
    ]
    for col in google_escape_cols_list:
        google_df[col] = google_df[col].apply(
            lambda x: np.nan if x is np.nan else escape_special_characters(str(x))
        )
        if col == "company_name":
            for suffix in COMPANY_SUFFIXES_LIST:
                google_df[col] = google_df[col].str.replace(suffix, "")

    # filter df
    google_df = google_df[
        google_df['domain'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_CHECK_RE, x))
        )
    ]
    google_df.dropna(subset=['domain'], inplace=True)

    # drop duplicates
    google_df.drop_duplicates(inplace=True)

    print(google_df.info())
    print(google_df)

    print(f"WRITING TRANSFORMED GOOGLE DF TO {TRANSFORM_GOOGLE_PATH}")
    google_df.to_csv(TRANSFORM_GOOGLE_PATH, index=False)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    transform_web()
    transform_fb()
    transform_google()
