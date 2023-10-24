import os

import pandas as pd

from common.conf import FB_FILE_NAME, GOOGLE_FILE_NAME, WEB_FILE_NAME, FB_GOOGLE_WEB_FILE_NAME, \
    TRANSFORM_FOLDER, PROCESS_FOLDER
from common.helper import get_project_path

PROJECT_PATH = get_project_path()

TRANSFORM_WEB_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, WEB_FILE_NAME)
TRANSFORM_FB_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, FB_FILE_NAME)
TRANSFORM_GOOGLE_PATH = os.path.join(PROJECT_PATH, TRANSFORM_FOLDER, GOOGLE_FILE_NAME)

PROCESS_FB_GOOGLE_WEB_PATH = os.path.join(PROJECT_PATH, PROCESS_FOLDER, FB_GOOGLE_WEB_FILE_NAME)

FINAL_DF_COLUMNS = [
    "fb_domain",
    "web_domain",
    "gg_domain",
    "fb_company_name",
    "web_company_name",
    "gg_company_name",
    "fb_category",
    "web_category",
    "gg_category",
    "fb_country",
    "web_country",
    "gg_country",
    "fb_region",
    "web_region",
    "gg_region",
    "fb_city",
    "web_city",
    "gg_city",
    "fb_phone",
    "web_phone",
    "gg_phone",
    "fb_country_code",
    "gg_country_code",
    "fb_region_code",
    "gg_region_code",
    "fb_address",
    "gg_address",
    "fb_zip_code",
    "gg_zip_code",
    "fb_phone_country_code",
    "gg_phone_country_code",
    "fb_description",
    "fb_email",
    "fb_link",
    "fb_page_type",
    "web_domain_suffix",
    "web_language",
    "web_site_name",
    "web_tld",
    "gg_raw_address",
    "gg_raw_phone",
    "gg_text"
]


def join_web_and_fb():
    web_df = pd.read_csv(TRANSFORM_WEB_PATH)
    fb_df = pd.read_csv(TRANSFORM_FB_PATH)

    result_df = fb_df.merge(web_df, left_on='fb_domain', right_on='web_domain', how='left')
    print("Joined WEB and FB datasets info")
    print(result_df.info())

    return result_df


def join_web_fb_google():
    google_join_cols = ['gg_company_name', 'gg_phone', 'gg_domain']
    fb_join_cols = ['fb_company_name', 'fb_phone', 'fb_domain']
    web_join_cols = ['web_company_name', 'web_phone', 'web_domain']

    google_df = pd.read_csv(TRANSFORM_GOOGLE_PATH)
    google_df.dropna(subset=google_join_cols)

    web_fb_df = join_web_and_fb()
    web_fb_not_equal_domains_df = web_fb_df[web_fb_df.fb_company_name != web_fb_df.web_company_name]

    web_fb_df = web_fb_df.dropna(subset=fb_join_cols)
    web_fb_not_equal_domains_df = web_fb_not_equal_domains_df.dropna(subset=web_join_cols)

    result_df = pd.concat(
        [
            google_df.merge(
                web_fb_df,
                left_on=google_join_cols,
                right_on=fb_join_cols
            ),
            google_df.merge(
                web_fb_not_equal_domains_df,
                left_on=google_join_cols,
                right_on=web_join_cols
            )
        ]
    )
    result_df = result_df[FINAL_DF_COLUMNS]
    result_df.sort_values(
        by=[
            "fb_domain",
            "fb_company_name",
            "fb_category",
            "fb_country",
            "fb_region",
            "fb_city"
        ],
        ascending=True,
        inplace=True
    )
    print("RESULT DF info:")
    print(result_df.info())

    result_df.to_csv(PROCESS_FB_GOOGLE_WEB_PATH, index=False)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    join_web_fb_google()
