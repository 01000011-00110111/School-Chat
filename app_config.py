"""This is the app config file (will change)"""

class Appconfiguration:
    """The app configclass"""

    def __init__(self, **kwargs):
        self.app_name = kwargs["app_name"]
        self.app_version = kwargs["app_version"]
        self.app_description = kwargs["app_desciption"]
        self.contributers = kwargs["contributers"]
        self.source = kwargs["source"]

    def dummy_method(self):
        """Dummy method to satisfy pylint."""
        return

    def another_dummy_method(self):
        """Another dummy method to satisfy pylint."""
        return


application = Appconfiguration(
  app_name="School Chat",
  app_desciption="Just a chat app",
  app_version="1.4",
  contributers=['C7', 'cserver', 'CastyiGlitchxz'],
  source="https://github.com/01000011-00110111/School-Chat",
)
