#!/usr/bin/env python
#
# create_robolog_dataset.py -- create a CKAN dataset (i.e. package) to contain a set of metrics log files
#
#   This program is called by create_robolog_dataset.sh and should be run once per match (i.e. once per log file)
#   Log file names MUST be unique within the scope of a CKAN dataset
#

import argparse
import json
import requests
import pprint
import robolog

# Define the command-line arguments

parser = argparse.ArgumentParser(prog='create_robolog_dataset',
                                 description='A program to create a container for Robolog files',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50,
                                                                                     width=130))

parser.add_argument('--config_file', action='store', dest='config_file', required=True,
                    help='The name and path to the Robolog config file')
parser.add_argument('--debug', '-d', action='store_true',
                    help='Print the result of the CKAN "package_create" API call')

parameters = parser.parse_args()

# Parse the configuration file values

configuration_dict = robolog.ParseConfig(parameters.config_file)

# Package the CKAN API parameters for package_create()

dataset_dict = {
    'author': configuration_dict['ckan_author'],
    'author_email': configuration_dict['ckan_author_email'],
    'maintainer': configuration_dict['ckan_maintainer'],
    'maintainer_email': configuration_dict['ckan_maintainer_email'],
    'name': configuration_dict['ckan_name'].lower(),
    'notes': configuration_dict['ckan_notes'],
    'owner_org': configuration_dict['ckan_owner_org'],
    'title': configuration_dict['ckan_title'],
    'url': configuration_dict['ckan_name'].lower(),
    'version': configuration_dict['ckan_version'],
    'tags': [{'name': configuration_dict['district']},
             {'name': configuration_dict['driver']},
             {'name': configuration_dict['event']},
             {'name': configuration_dict['eventlat']},
             {'name': configuration_dict['eventlon']},
             {'name': configuration_dict['match']},
             {'name': configuration_dict['robot']},
             {'name': configuration_dict['station']},
             {'name': configuration_dict['teamname']},
             {'name': configuration_dict['teamnumber']}]
}

# Make the REST call

request_url = configuration_dict['server'] + '/api/action/package_create'

headers = {
    'Authorization': configuration_dict['ckan_apikey'],
    'Content-type': 'application/json'
}

print 'Attempting to create dataset "' + dataset_dict[
    'name'] + '" on ' + configuration_dict['server'] + ' using the config file "' + parameters.config_file + '"'

response = requests.post(request_url, data=json.dumps(dataset_dict), headers=headers)

# Optionally print the result

if parameters.debug:
    pprint.pprint(json.loads(response.content))

print 'Done'
