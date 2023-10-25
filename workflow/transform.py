import os
import re

import numpy as np
import pandas as pd

from common.conf import FB_FILE_NAME, GOOGLE_FILE_NAME, WEB_FILE_NAME, \
    RAW_FOLDER, TRANSFORM_FOLDER
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

COMPANY_SUFFIXES_LIST = ['_inc', '_corp', '_llp', '_llc', '_ltd', '_co', '_limited']


def transform_web():
    """TRANSFORM WEB DATASET"""

    print('READING WEB DATASET:')
    web_df = pd.read_csv(RAW_WEB_PATH)
    print(web_df.info())

    print('STARTING CLEANING AND TRANSFORMATIONS:')
    # columns renaming
    web_rename_mapping = {
        "root_domain": "web_domain",
        "domain_suffix": "web_domain_suffix",
        "language": "web_language",
        "legal_name": "web_company_name",
        "main_city": "web_city",
        "main_country": "web_country",
        "main_region": "web_region",
        "phone": "web_phone",
        "site_name": "web_site_name",
        "tld": "web_tld",
        "s_category": "web_category"
    }
    web_df.rename(web_rename_mapping, axis=1, inplace=True)

    # to lowercase
    web_lowercase_cols_list = [
        "web_domain", "web_domain_suffix", "web_language", "web_company_name",
        "web_city", "web_country", "web_region", "web_site_name", "web_tld", "web_category"
    ]
    for col in web_lowercase_cols_list:
        web_df[col] = web_df[col].str.lower()

    # escape special characters
    web_escape_cols_list = [
        "web_language", "web_company_name", "web_city", "web_country",
        "web_region", "web_site_name", "web_tld", "web_category"
    ]
    for col in web_escape_cols_list:
        web_df[col] = web_df[col].apply(
            lambda x: np.nan if x is np.nan else escape_special_characters(str(x))
        )
        if col == "web_company_name":
            for suffix in COMPANY_SUFFIXES_LIST:
                web_df[col] = web_df[col].str.replace(suffix, "")

    # filter df
    web_df = web_df[
        web_df['web_domain'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_CHECK_RE, x))
        )
    ]
    web_df = web_df[
        web_df['web_domain_suffix'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_SUFFIX_CHECK_RE, x))
        )
    ]
    web_df = web_df[
        web_df['web_phone'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(PHONE_CHECK_RE, x))
        )
    ]

    web_df.dropna(subset=['web_domain'], inplace=True)

    # cast columns
    web_df['web_phone'] = web_df['web_phone'].astype(float, errors='ignore').astype(int, errors='ignore')

    # drop duplicates
    web_df.drop_duplicates(inplace=True)

    print(web_df.info())

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
        "domain": "fb_domain",
        "address": "fb_address",
        "categories": "fb_categories",
        "city": "fb_city",
        "country_code": "fb_country_code",
        "country_name": "fb_country",
        "description": "fb_description",
        "email": "fb_email",
        "link": "fb_link",
        "name": "fb_company_name",
        "page_type": "fb_page_type",
        "phone": "fb_phone",
        "phone_country_code": "fb_phone_country_code",
        "region_code": "fb_region_code",
        "region_name": "fb_region",
        "zip_code": "fb_zip_code"
    }
    fb_df.rename(fb_rename_mapping, axis=1, inplace=True)

    # to lowercase
    fb_lowercase_cols_list = [
        "fb_domain", "fb_categories", "fb_city", "fb_country_code",
        "fb_country", "fb_email", "fb_link", "fb_company_name", "fb_page_type",
        "fb_phone_country_code", "fb_region_code", "fb_region"
    ]
    for col in fb_lowercase_cols_list:
        fb_df[col] = fb_df[col].str.lower()

    # exploding categories into multiple rows
    fb_df = fb_df\
        .assign(
            fb_category=fb_df['fb_categories'].str.split('|')
        )\
        .explode('fb_category')\
        .reset_index(drop=True)

    fb_df.drop('fb_categories', axis=1, inplace=True)

    # escape special characters
    fb_escape_cols_list = [
        "fb_category", "fb_city", "fb_country_code",
        "fb_country", "fb_company_name", "fb_page_type",
        "fb_phone_country_code", "fb_region_code", "fb_region"
    ]
    for col in fb_escape_cols_list:
        fb_df[col] = fb_df[col].apply(
            lambda x: np.nan if x is np.nan else escape_special_characters(str(x))
        )
        if col == "fb_company_name":
            for suffix in COMPANY_SUFFIXES_LIST:
                fb_df[col] = fb_df[col].str.replace(suffix, "")

    # filter df
    fb_df = fb_df[
        fb_df['fb_domain'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_CHECK_RE, x))
        )
    ]
    fb_df.dropna(subset=['fb_domain'], inplace=True)

    # drop duplicates
    fb_df.drop_duplicates(inplace=True)

    print(fb_df.info())

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
        "address": "gg_address",
        "category": "gg_category",
        "city": "gg_city",
        "country_code": "gg_country_code",
        "country_name": "gg_country",
        "name": "gg_company_name",
        "phone": "gg_phone",
        "phone_country_code": "gg_phone_country_code",
        "raw_address": "gg_raw_address",
        "raw_phone": "gg_raw_phone",
        "region_code": "gg_region_code",
        "region_name": "gg_region",
        "text": "gg_text",
        "zip_code": "gg_zip_code",
        "domain": "gg_domain"
    }
    google_df.rename(google_rename_mapping, axis=1, inplace=True)

    # to lowercase
    google_lowercase_cols_list = [
        "gg_domain", "gg_category", "gg_city", "gg_country_code", "gg_country",
        "gg_company_name", "gg_phone_country_code", "gg_region_code", "gg_region"
    ]
    for col in google_lowercase_cols_list:
        google_df[col] = google_df[col].str.lower()

    # escape special characters
    google_escape_cols_list = [
        "gg_category", "gg_city", "gg_country_code", "gg_country",
        "gg_company_name", "gg_phone_country_code", "gg_region_code", "gg_region"
    ]
    for col in google_escape_cols_list:
        google_df[col] = google_df[col].apply(
            lambda x: np.nan if x is np.nan else escape_special_characters(str(x))
        )
        if col == "gg_company_name":
            for suffix in COMPANY_SUFFIXES_LIST:
                google_df[col] = google_df[col].str.replace(suffix, "")

    # filter df
    google_df = google_df[
        google_df['gg_domain'].apply(
            lambda x: x is np.nan or isinstance(x, str) and bool(re.match(DOMAIN_CHECK_RE, x))
        )
    ]
    google_df.dropna(subset=['gg_domain', 'gg_company_name'], inplace=True)

    # drop duplicates
    google_df.drop_duplicates(inplace=True)

    print(google_df.info())

    print(f"WRITING TRANSFORMED GOOGLE DF TO {TRANSFORM_GOOGLE_PATH}")
    google_df.to_csv(TRANSFORM_GOOGLE_PATH, index=False)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    transform_web()
    transform_fb()
    transform_google()
