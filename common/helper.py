import os


def get_project_path():
    helper_path = os.path.abspath(__file__)
    common_path = os.path.dirname(helper_path)
    project_path = os.path.dirname(common_path)
    return project_path
