#!/usr/bin/env python
#
# set_robolog_config.py -- set robolog configuration via command-line interface
#
#   This program is called by set_robolog_config.sh and should be run once per event (i.e. practice or FRC competition)

import argparse
import ConfigParser

# Define the command-line arguments


parser = argparse.ArgumentParser(prog='set_robolog_config',
                                 description='A program to set the robolog configuration parameters. "--match" should be updated for each match',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50,
                                                                                     width=130))

parser.add_argument('--ckan_apikey', action='store', dest='ckan_apikey', required=True, default='MISSING API KEY',
                    help='Set the CKAN API key')
parser.add_argument('--ckan_author', action='store', dest='ckan_author', default='UNDEFINED',
                    help='Set the CKAN dataset author name')
parser.add_argument('--ckan_author_email', action='store', dest='ckan_author_email', default='UNDEFINED',
                    help='Set the CKAN dataset author e-mail address')
parser.add_argument('--ckan_maintainer', action='store', dest='ckan_maintainer', default='UNDEFINED',
                    help='Set the CKAN dataset maintainer')
parser.add_argument('--ckan_maintainer_email', action='store', dest='ckan_maintainer_email', default='UNDEFINED',
                    help='Set the CKAN dataset maintainer e-mail address')
parser.add_argument('--ckan_name', action='store', dest='ckan_name', required=True, default='UNDEFINED',
                    help='Set the CKAN dataset name')
parser.add_argument('--ckan_notes', action='store', dest='ckan_notes', default='UNDEFINED',
                    help='Set the CKAN dataset notes')
parser.add_argument('--ckan_owner_org', action='store', dest='ckan_owner_org', required=True, default='UNDEFINED',
                    help='Set the CKAN organization name')
parser.add_argument('--ckan_title', action='store', dest='ckan_title', default='0.9',
                    help='Set the CKAN datset title')
parser.add_argument('--ckan_version', action='store', dest='ckan_version', default='0.9',
                    help='Set the CKAN datset version number')
parser.add_argument('--cfg_file', action='store', dest='cfg_file', required=True, default='UNDEFINED',
                    help='Set the FRC Robolog config file name (e.g. robolog.cfg)')
parser.add_argument('--district', action='store', dest='district', default='UNDEFINED',
                    help='Set the FRC district name (e.g. PNW)')
parser.add_argument('--driver', action='store', dest='driver', required=True, default='UNDEFINED',
                    help='Set the FRC robot driver name (e.g. BusterBoy)')
parser.add_argument('--event', action='store', dest='event', required=True, default='UDEFINED',
                    help='Set the FRC event code (e.g PRACT)')
parser.add_argument('--eventlat', action='store', dest='eventlat', default='UNDEFINED',
                    help='Set the FRC event venue (e.g. 48.101)')
parser.add_argument('--eventlon', action='store', dest='eventlon', default='UNDEFINED',
                    help='Set the FRC event venue longitude (e.g. -122.799)')
parser.add_argument('--match', action='store', dest='match', required=True, default='UNDEFINED',
                    help='Set the FRC event match number (e.g. P1)')
parser.add_argument('--robot', action='store', dest='robot', required=True, default='UNDEFINED',
                    help='Set the FRC robot name (e.g. Buster)')
parser.add_argument('--server', action='store', dest='server', default='UNDEFINED',
                    help='Set the FRC robolog server name (e.g. http://frc-robolog.org:5000)')
parser.add_argument('--station', action='store', dest='station', required=True, default='UNDEFINED',
                    help='Set the FRC robot driver station (e.g. station1)')
parser.add_argument('--teamname', action='store', dest='teamname', required=True, default='UNDEFINED',
                    help='Set the FRC team name (e.g. Roboctopi)')
parser.add_argument('--teamnumber', action='store', dest='teamnumber', required=True, default='UNDEFINED',
                    help='Set the FRC team number (e.g. 4918)')

# Parse the commannd-line arguments

parameters = parser.parse_args()

# Map command-line arguments to configuration file values

config = ConfigParser.RawConfigParser()

# Values specific to CKAN

config.add_section('robolog:ckan')
config.set('robolog:ckan', 'ckan_apikey', parameters.ckan_apikey)
config.set('robolog:ckan', 'ckan_author', parameters.ckan_author)
config.set('robolog:ckan', 'ckan_author_email', parameters.ckan_author_email)
config.set('robolog:ckan', 'ckan_maintainer', parameters.ckan_maintainer)
config.set('robolog:ckan', 'ckan_maintainer_email', parameters.ckan_maintainer_email)
config.set('robolog:ckan', 'ckan_name', parameters.ckan_name)
config.set('robolog:ckan', 'ckan_notes', parameters.ckan_notes)
config.set('robolog:ckan', 'ckan_owner_org', parameters.ckan_owner_org)
config.set('robolog:ckan', 'ckan_title', parameters.ckan_title)
config.set('robolog:ckan', 'ckan_version', parameters.ckan_version)

# Values specific to FRC (i.e. Robolog)

config.add_section('robolog:frc')
config.set('robolog:frc', 'cfg_file', parameters.cfg_file)
config.set('robolog:frc', 'district', 'District.' + parameters.district)
config.set('robolog:frc', 'driver', 'Driver.' + parameters.driver)
config.set('robolog:frc', 'event', 'Event.' + parameters.event)
config.set('robolog:frc', 'eventlat', 'EventLat.' + parameters.eventlat)
config.set('robolog:frc', 'eventlon', 'EventLon.' + parameters.eventlon)
config.set('robolog:frc', 'match', 'Match.' + parameters.match)
config.set('robolog:frc', 'robot', 'Robot.' + parameters.robot)
config.set('robolog:frc', 'server', parameters.server)
config.set('robolog:frc', 'station', 'Station.' + parameters.station)
config.set('robolog:frc', 'teamname', 'Teamname.' + parameters.teamname)
config.set('robolog:frc', 'teamnumber', 'Teamnumber.' + parameters.teamnumber)

# Write the configuration values to the configuration file (robolog.cfg by default)

with open(parameters.cfg_file, 'wb') as configfile:
    config.write(configfile)

print "Settings written to " + parameters.cfg_file
