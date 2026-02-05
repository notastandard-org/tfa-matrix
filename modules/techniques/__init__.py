import json

from . import techniques, techniques_config


def get_priority():
    return techniques_config.priority


def get_menu():
    return {
        "display_name": techniques_config.module_name,
        "module_name": techniques_config.module_name,
        "url": "/techniques/tfa/",
        "external_link": False,
        "priority": techniques_config.priority,
        "children": [],
    }


def run_module():
    return techniques.generate_techniques(), techniques_config.module_name
