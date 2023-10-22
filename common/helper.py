import os
import re


def get_project_path():
    helper_path = os.path.abspath(__file__)
    common_path = os.path.dirname(helper_path)
    project_path = os.path.dirname(common_path)
    return project_path


def escape_special_characters(name: str, replace_char: str = ''):
    escaped = ''.join(
        char if char.isalnum() or char == ' ' else replace_char
        for char in name
    )
    escaped = re.sub(' +', '_', escaped)
    return escaped
