class appConfiguration:
  def __init__(self, appName, appVersion, appDesciption, contributers, source):
    self.appName = appName
    self.appVersion = appVersion
    self.appDescription = appDesciption
    self.contributers = contributers
    self.source = source


application = appConfiguration(
  appName="School Chat",
  appDesciption="Just a chat app",
  appVersion="1.3.0.RC.6",
  contributers=['C7', 'cserver', 'CastyiGlitchxz'],
  source="https://github.com/01000011-00110111/School-Chat",
)