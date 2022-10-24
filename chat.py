logfile = "chat.txt"

# Returns a list of dictionaries. Each dictionary in the list
# is a message that has been sent in our chat server
def get_chat():
  ret_val = []
  with open(logfile) as f_in:
    for line in f_in:
      line = line.rstrip("\n\r")
      rec = {"message" :  line }
      ret_val.append(rec)
  return ret_val

# Adds the message text to our file containing all the messages
def add_message(message_text):
  with open(logfile, "a") as f_out:
    f_out.write(message_text + "\n")
  # This return is not needed, but ensures replit shows the updated
  # file when it is selected from the file browser during our demo
  return None