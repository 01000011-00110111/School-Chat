"""This is the app config file (will change)"""
class Appconfiguration:
    """The app configclass"""

    def __init__(self, app_name, app_version, app_desciption, contributers, source):
        self.app_name = app_name
        self.app_version = app_version
        self.app_description = app_desciption
        self.contributers = contributers
        self.source = source


application = Appconfiguration(
  app_name="School Chat",
  app_desciption="Just a chat app",
  app_version="1.4",
  contributers=['C7', 'cserver', 'CastyiGlitchxz'],
  source="https://github.com/01000011-00110111/School-Chat",
)
