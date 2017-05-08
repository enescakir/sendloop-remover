import os, requests, json, csv, argparse, re, sys

# Parse arguments from command line
parser = argparse.ArgumentParser(description='Sendloop unsubscribe app')
parser.add_argument('-s', '--start', dest="start", action='store')
parser.add_argument('-c', '--count', dest="count", action='store')
parser.add_argument('-f', '--file', dest="file", action='store', required=True)
parser.add_argument('-l', '--log', dest="log", action='store', required=True)
parser.add_argument('-r', '--regex', dest="regex", action='store')
arguments = parser.parse_args()

# Default value for starting
start = 0
if arguments.start:
    start = int(arguments.start)

# Default value for number of rows
count = 1000000
if arguments.count:
    count = int(arguments.count)

# Create iteration range
region = range(start, start + count)

# Default value for REGEX
regex = ".*?"
if arguments.regex:
    regex = arguments.regex

# File location
file = arguments.file

# Log filename
log = arguments.log

# Read .env file
env = {}
with open('.env') as env_data:
    for line in env_data:
        parts = line.replace("\n", "").split("=")
        env[parts[0]] = parts[1]

# Checks is .env has API_KEY
api_key = env.get('API_KEY')
if not api_key:
    print('Please give a Sendloop "API_KEY" in your .env file')
    sys.exit()

# Checks is .env has LIST_ID
list_id = env.get('LIST_ID')
if not list_id:
    print('Please give a Sendloop "LIST_ID" in your .env file')
    sys.exit()

# Checks is .env has UNSUB_IP
unsub_ip = env.get('UNSUB_IP')
if not unsub_ip:
    print('Please give a "UNSUB_IP" in your .env file')
    sys.exit()

# Get EMAIL_KEY from .env with default value 'Email'
email_key = env.get('EMAIL_KEY', 'Email')

print('== Unsubscribing ' + str(start) + " to " + str(start + count) + " => " + log)

log_file = open(log, "w")
with open(file) as csvfile:
    reader = csv.DictReader(csvfile)
    for i,row in enumerate(reader):
        if i in region:
            if email_key in row.keys():
                email = row[email_key]
            else:
                print('Please give a correct "EMAIL_KEY" in your .env file.')
                print('It should matched with your CSV file column header')
                print('Default: Email')
                sys.exit()

            if re.search(regex, email):
                sendloop_payload = {'APIKey': api_key,'EmailAddress': email, 'ListID': list_id, 'UnsubscriptionIP': unsub_ip}
                sendloop_request = requests.post('http://app.sendloop.com/api/v3/subscriber.unsubscribe/json', data = sendloop_payload)
                response = sendloop_request.json()

                if response['Success']:
                    log = str(i+1) + " - " + email + " => Unsubscribed"
                else:
                    log = str(i+1) + " - " + email + " => " + response['ErrorMessage']

                print(log)
                log_file.write(log + "\n")
log_file.close()
