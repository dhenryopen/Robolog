# Shared functions

import ConfigParser

# Used with the configuration files (e.g. robolog.cfg)

Config = ConfigParser.RawConfigParser()


def ParseConfigSectionMap(section):
    dict = {}
    options = Config.options(section)
    for option in options:
        try:
            dict[option] = Config.get(section, option)
            if dict[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict[option] = None
    return dict


def ParseConfig(cfg_file):
    dict = {}
    Config.read(cfg_file)  # e.g. read robolog.cfg

    # Assign configuration values to dictionary variables
    # Values should be set by set_robolog_config.py using set_robolog_config.sh

    # Specific to CKAN
    section_ckan = "robolog:ckan"

    dict['ckan_apikey'] = ParseConfigSectionMap(section_ckan)['ckan_apikey']
    dict['ckan_package_id'] = ParseConfigSectionMap(section_ckan)['ckan_name']
    dict['ckan_apikey'] = ParseConfigSectionMap(section_ckan)['ckan_apikey']
    dict['ckan_author'] = ParseConfigSectionMap(section_ckan)['ckan_author']
    dict['ckan_author_email'] = ParseConfigSectionMap(section_ckan)['ckan_author_email']
    dict['ckan_maintainer'] = ParseConfigSectionMap(section_ckan)['ckan_maintainer']
    dict['ckan_maintainer_email'] = ParseConfigSectionMap(section_ckan)['ckan_maintainer_email']
    dict['ckan_name'] = ParseConfigSectionMap(section_ckan)['ckan_name']
    dict['ckan_notes'] = ParseConfigSectionMap(section_ckan)['ckan_notes']
    dict['ckan_owner_org'] = ParseConfigSectionMap(section_ckan)['ckan_owner_org']
    dict['ckan_title'] = ParseConfigSectionMap(section_ckan)['ckan_title']
    dict['ckan_version'] = ParseConfigSectionMap(section_ckan)['ckan_version']

    # Specific to Robolog
    section_frc = "robolog:frc"

    dict['cfg_file'] = ParseConfigSectionMap(section_frc)['cfg_file']
    dict['district'] = ParseConfigSectionMap(section_frc)['district']
    dict['driver'] = ParseConfigSectionMap(section_frc)['driver']
    dict['event'] = ParseConfigSectionMap(section_frc)['event']
    dict['eventlat'] = ParseConfigSectionMap(section_frc)['eventlat']
    dict['eventlon'] = ParseConfigSectionMap(section_frc)['eventlon']
    dict['match'] = ParseConfigSectionMap(section_frc)['match']
    dict['robot'] = ParseConfigSectionMap(section_frc)['robot']
    dict['server'] = ParseConfigSectionMap(section_frc)['server']
    dict['station'] = ParseConfigSectionMap(section_frc)['station']
    dict['teamname'] = ParseConfigSectionMap(section_frc)['teamname']
    dict['teamnumber'] = ParseConfigSectionMap(section_frc)['teamnumber']
    return dict
