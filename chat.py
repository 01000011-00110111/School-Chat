logfile = "backend/chat.txt"
logfile_b = "backend/Chat-backup.txt"


# Returns a list of dictionaries. Each dictionary in the list
# is a message that has been sent in our chat server
def get_chat():
  ret_val = []
  with open(logfile) as f_in:
    for line in f_in:
      line = line.rstrip("\n\r")
      rec = {"message": line}
      ret_val.append(rec)
  return ret_val

def get_line_count():
  ret_val = []
  with open(logfile, "r") as f:
    lines = len(f.readlines())
  with open(logfile, "a") as f:
    f.write(f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>\n")
    ret_val.append(lines)
  return ret_val


# Adds the message text to our file containing all the messages
def add_message(message_text):
  with open(logfile, "r") as f:
    lines = len(f.readlines())
  if lines > 500:
    with open(logfile, "w") as f_out:
      f_out.write("[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font>\n" + message_text + "\n")
  else:
    with open(logfile, "a") as f:
      f.write(message_text + "\n")
  with open(logfile_b, "a") as f_out:
    f_out.write(message_text + "\n")
  # This return is not needed, but ensures replit shows the updated
  # file when it is selected from the file browser during our demo
  return None

# force the message text to our file containing all the messages
def force_message(message_text):
  with open(logfile, "a") as f:
    f.write(message_text + "\n")
  with open(logfile_b, "a") as f_out:
    f_out.write(message_text + "\n")
  # This return is not needed, but ensures replit shows the updated
  # file when it is selected from the file browser during our demo
  return None

# returns list of commands.
# will be run at loading of page
def get_command_list():
  ret_val = []
  with open("backend/commands.txt", "r") as commands:
    for command in commands:
      line = command.rstrip("\n\r")
      rec = {"commands": line}
      ret_val.append(rec)
  return ret_val

def get_command_defs():
  ret_val = []
  with open("backend/cmd_def.txt", "r") as commands:
    for command in commands:
      line = command.rstrip("\n\r")
      rec = {"commands": line}
      ret_val.append(rec)
  return ret_val
