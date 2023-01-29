#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""This module checks your current Microsoft Teams status and also if you are in a call/meeting.

It reads the standard Microsoft Teams log file and extracts your current call status and your user status
and prints it to the console.

You can customize the refresh interval by setting up the value of refresh_interval variable. Default value is 10 seconds.
"""

__version__ = '1.0'
__author__ = 'Krypton B'

import time

# Refresh interval to check your status. Give the value in seconds (default is 10 seconds)
refresh_interval = 10

# MS Teams log path. Make sure to give the path according to your username.
ms_teams_log = 'C:\\Users\\<your username>\\AppData\\Roaming\\Microsoft\\Teams\\logs.txt'

# Text to search for ongoing call status
# As of 2023/01/10 - MS Teams log contains lines similar to below which we can use to extract the user's status. We read
# the whole log and take only the last occurrance of this line to determine the current status of the user.
#   <17396> -- info -- StatusIndicatorStateService: Removing NewActivity (current state: NewActivity -> OnThePhone)
current_status_text = 'current state:'


# Text to search for ongoing call status
# As of 2023/01/10 - MS Teams log contains lines similar to below which we can use to extract the user's status. We read
# the whole log and take only the last occurrance of this line to determine if the user in currently in a Teams call/meeting.
#   <17396> -- event -- eventpdclevel: 2, name: desktop_call_state_change_send, isOngoing: false, AppInfo.Language: en-us,
ongoing_call_text = 'isOngoing:'

  

def get_status(string_to_read):
    """Return a list of two elements for Microsoft Teams user status and a human-friendly status text relevant to the given string."""
    last_status = string_to_read[string_to_read.find('->')+3 :-3]
    
    # List of statuses 
    #   Away  -- away
    #   Offline   -- offline
    #   Focusing  -- focusing
    #   Presenting   -- presenting
    #   InAMeeting  -- in a meeting
    #   BeRightBack  -- be right back
    #   DoNotDisturb  -- do not disturb
    #   Available  -- available (green)
    #   OnThePhone  -- in a call (not a meeting)
    #   NewActivity  -- some change eg: new message, new like, new mention   
    
    if last_status == 'Available':
        last_status_human_friendly = 'Available'
    elif last_status == 'NewActivity':
        last_status_human_friendly = 'New Activity'
    elif last_status == 'OnThePhone':
        last_status_human_friendly = 'In a call'
    elif last_status == 'Away':
        last_status_human_friendly = 'Away'
    elif last_status == 'BeRightBack':
        last_status_human_friendly = 'Be right back'
    elif last_status == 'DoNotDisturb':
        last_status_human_friendly = 'Do not disturb'
    elif last_status == 'Focusing':
        last_status_human_friendly = 'Focusing'
    elif last_status == 'Presenting':
        last_status_human_friendly = 'Presenting'
    elif last_status == 'InAMeeting':
        last_status_human_friendly = 'In a meeting'
    elif last_status == 'Offline':
        last_status_human_friendly = 'Offline'
    else:
        last_status_human_friendly = 'Unknown'
    
    return [last_status, last_status_human_friendly]  


def get_last_line_of_given_text(file_to_read, text_to_check):
    """Return last line that contains the given string from the given file."""
    all_lines = []
    with open(file_to_read, 'rt') as f:
        data = f.readlines()
        
    for line in data:
        # Check the last occurrance of 'desktop_call_state_change_send, isOngoing' line. This will tell us if a call is ongoing or not
        # Check the last occurrance of 'current state:' line. This will tell us your current MS Teams status
        if text_to_check in line:
            all_lines.append(line)
            
    # Check if there is at least one occurrance of the given text.
    # If not, then return None
    if len(all_lines) > 0:
        return all_lines[-1]
    else:
        return None


def check_ms_teams_status():
    """Check Microsoft Teams log to see if a call/meeting is in proress."""
    while True:
    
        # Check last status line to get my current MS Teams Status and get human friendly status from it
        last_status_line = get_last_line_of_given_text(ms_teams_log, current_status_text)
               
        if last_status_line is not None:
            print ('last status line: ' + last_status_line)
            status_list = get_status(last_status_line)
                        
            # Check last ongoing line to see if a call is ongoing                
            last_ongoing_line = get_last_line_of_given_text(ms_teams_log, ongoing_call_text)
            
            if last_ongoing_line is not None:
                print ('last ongoing line: ' + last_ongoing_line)
                if 'isOngoing: true' not in last_ongoing_line:
                    print('Not in a meeting/call')
                    print('Your current status is ' + status_list[0] + ':' + status_list[1])               
                else:
                    print('There is a call in progress...')
                    print('Your current status is ' + status_list[0] + ':' + status_list[1])
            else:
                print('Could not find a line containing your text: ' + ongoing_call_text)
        else:
            print('Could not find a line containing your text: ' + current_status_text)
                
        time.sleep(refresh_interval)
    
if __name__ == "__main__":
    check_ms_teams_status()

