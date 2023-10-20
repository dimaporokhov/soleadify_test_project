import os
import pandas as pd

from common.conf import FB_FILE_NAME, GOOGLE_FILE_NAME, WEB_FILE_NAME, \
    SOURCE_FOLDER, RAW_FOLDER
from common.helper import get_project_path

PROJECT_PATH = get_project_path()

SOURCE_WEB_PATH = os.path.join(PROJECT_PATH, SOURCE_FOLDER, WEB_FILE_NAME)
RAW_WEB_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, WEB_FILE_NAME)

SOURCE_FB_PATH = os.path.join(PROJECT_PATH, SOURCE_FOLDER, FB_FILE_NAME)
RAW_FB_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, FB_FILE_NAME)

SOURCE_GOOGLE_PATH = os.path.join(PROJECT_PATH, SOURCE_FOLDER, GOOGLE_FILE_NAME)
RAW_GOOGLE_PATH = os.path.join(PROJECT_PATH, RAW_FOLDER, GOOGLE_FILE_NAME)


print('READING WEB DATASET:')
web_df = pd.read_csv(SOURCE_WEB_PATH, sep=';')
print('GOT DF:')
print(web_df.info())
print(f"WRITING WEB DF TO {RAW_WEB_PATH}")
web_df.to_csv(RAW_WEB_PATH, index=False)

print('READING FACEBOOK DATASET:')
fb_df = pd.read_csv(SOURCE_FB_PATH, quotechar='"', escapechar='\\', doublequote=False)
print('GOT DF:')
print(fb_df.info())
print(f"WRITING FB DF TO {RAW_FB_PATH}")
fb_df.to_csv(RAW_FB_PATH, index=False)

print('READING GOOGLE DATASET:')
google_df = pd.read_csv(SOURCE_GOOGLE_PATH, quotechar='"', escapechar='\\', doublequote=False)
print('GOT DF:')
print(google_df.info())
print(f"WRITING GOOGLE DF TO {RAW_GOOGLE_PATH}")
google_df.to_csv(RAW_GOOGLE_PATH, index=False)
