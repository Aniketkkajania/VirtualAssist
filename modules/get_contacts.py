from __future__ import print_function
import os.path
import os
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# script_dir = os.path.getcwd().replace('\\', '/')
script_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

# THIS FUNCTION FILTERS THE NUMBER THAT ARE NOT IN FORMAT
def filter_num(nums):
    if nums.startswith('+'):
        return nums.replace(' ', '').replace('-', '')
    else:
        if len(nums.strip()) < 10:
            return nums.strip()
        return '+91' + nums.replace(' ', '').replace('-', '')


# THIS FUNCTION OPENS THE CSV FILE CREATED
def display(file_path):
    os.startfile(script_dir + '/' + file_path)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


# FUNCTION TO GET THE PHONE NUMBERS FROM THE GOOGLE CONTACTS
def get_contacts():
    contacts = {}

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(script_dir+'/token.json'):
        creds = Credentials.from_authorized_user_file(script_dir+'/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                script_dir+'/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(script_dir+'/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('people', 'v1', credentials=creds)

        # Call the People API
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,emailAddresses,phoneNumbers').execute()
        connections = results.get('connections', [])

        for person in connections:
            names = person.get('names', [])
            numbers = person.get('phoneNumbers', [])
            if names and numbers:
                name = names[0].get('displayName')
                number = filter_num(numbers[0].get('value'))  # filter the numbers using the function I made earlier
                if name not in contacts:
                    contacts[name] = number

        return contacts

    except HttpError as err:
        print(err)


# FUNCTION TO SAVE THE CONTACTS IN A CSV FILE THAT RETURNS THE PATH OF THE FILE
def save_contacts(contacts):
    if os.path.exists(script_dir + '/Contacts/'):
        pass
    else:
        try:
            os.makedirs(script_dir + '/Contacts')
        except FileExistsError:
            pass

        with open(script_dir + '/Contacts/contacts.csv', 'w', newline='', encoding='utf-8') as contact:
            writer = csv.writer(contact)
            writer.writerow(['Name', 'Number'])
            for name in contacts.keys():
                writer.writerow([name, contacts[name]])
    return 'Contacts/contacts.csv'


display(save_contacts(get_contacts()))