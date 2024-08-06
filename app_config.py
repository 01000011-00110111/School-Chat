"""app_config.py: App configuration.
    (This may change in a future update)
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from dataclasses import dataclass

@dataclass
class Appconfiguration:
    """The app configclass"""

    def __init__(self, **kwargs):
        self.app_name = kwargs["app_name"]
        self.app_version = kwargs["app_version"]
        self.app_description = kwargs["app_desciption"]
        self.contributers = kwargs["contributers"]
        self.source = kwargs["source"]


application = Appconfiguration(
    app_name="School Chat",
    app_desciption="Just a chat app",
    app_version="1.4",
    contributers=['C7', 'cserver', 'CastyiGlitchxz'],
    source="https://github.com/01000011-00110111/School-Chat",
)
