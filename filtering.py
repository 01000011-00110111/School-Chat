def filter_username(message):
  user_name = message.split(":")[0]

  if (user_name == ""):
    user_name = "Anonymous"
  elif (user_name == "Owen "):
    user_name = "Owen"
  elif (user_name == "Owen"):
    return
  elif (user_name == "Admin" or user_name == "admin" or user_name == "[admin]" or user_name == "[admin]" or user_name == "[ADMIN]"):
    return
  elif (user_name == "Dev EReal"): 
    user_name = "Dev E"
  elif (user_name == "Dev E"):
    return
  elif (user_name == "cserverReal"):
      user_name = "cserver"
  elif (user_name == "cserver"):
    return
  elif (user_name == "SYSTEM" or user_name == "[SYSTEM]"):
    return#//im working on the account and google accounts is what we are doing or do you want somthing else its gona be hard ok ill push to git then /ok/ no I cant need to learn how to might need to make a stackoverflow queston