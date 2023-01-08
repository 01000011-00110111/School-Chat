import psutil
from time import time
from datetime import timedelta, datetime

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


def get_stats():
  # long stats list lol

  # get line count
  with open(logfile, "r") as f:
    lines = len(f.readlines())
  with open(logfile_b, "r") as f:
    lines_b = len(f.readlines())

  # other stats on the repl
  p = psutil.Process()
  with p.oneshot():
    uptime = timedelta(seconds=time() - p.create_time())
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    pname = p.name()
    thread_count = p.num_threads()
    mem = p.memory_full_info()

  begin_f = "[SYSTEM]: <font color='#ff7f00'>Server Stats:</font>"
  lines_f = f"Temp logfile: {lines} lines.\nBackup logfile: {lines_b} lines."
  uptime_f = f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} seconds."
  cpu_info = f"Threads: {thread_count}"
  longstats = f"{begin_f}\n{lines_f}\n{uptime_f}\n"
  with open(logfile, "a") as f:
    f.write(longstats)
  return


# Adds the message text to our file containing all the messages
def add_message(message_text):
  with open(logfile, "r") as f:
    lines = len(f.readlines())
  if lines >= 500:
    reset_chat(message_text, False)
  else:
    with open(logfile, "a") as f:
      f.write(message_text + "\n")
  with open(logfile_b, "a") as f_out:
    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S: ")
    f_out.write(date + message_text + "\n")
  # This return is not needed, but ensures replit shows the updated
  # file when it is selected from the file browser during our demo
  return None


def reset_chat(message, admin):
  if admin == True:
    with open(logfile, "w") as f_out:
      f_out.write(
        "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font>\n")
  else:
    with open(logfile, "w") as f_out:
      f_out.write(
        "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font>\n"
        + message + "\n")


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
