# Python module for checking your Microsoft Teams status

This python script will check if you are in Microsoft Teams meeting/call and also it will print your current status.

This is an alternative to using Microsoft Graph Presence API to check your MS Teams status

Microsoft Graph Presense API has some limitation if you are not an a tenant admin. Therefore, this script uses
a much simpler approach by reading the standard MS Teams log file to check your ongoing call status.

You can use this with any other scripts if you want to automate using a Raspberry PI to light up a color-changing bulb 
according to your MS Teams call status

## Installation
* Clone the repository and open ms_teams_status.py 

## Requirements
* Works with Python 2.7+

## Usage
* python ms_teams_status.py

## Built With
* Python

