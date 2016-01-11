# Robolog Server

Robolog uses the [CKAN open source data portal](http://ckan.org/) for data ingestion, tagging, indexing, search, retrieval and collaboration. CKAN is used with the default "development" configuration which simplifies installation and allows Robolog to run in a variety of Linux environments. This brief guide walks through the minimum steps needed to install CKAN for use with the Robolog client scripts.

## Overview

The simplest way to install Robolog and CKAN is to follow this process:

1. Create an Ubuntu server using your own hardware or a hosted VM
2. Make the server accessible to external clients (optional)
3. Download and configure the CKAN prerequisites (e.g. open-jdk, solr, git, postgres and python)
4. Download and install the CKAN source code package
5. Configure CKAN-related directories and configuration files and the CKAN repository 
6. Test your installation
7. Clone the Robolog github repository to access the client scripts and sample data
8. Create your Team's "robolog.cfg" file with the appropriate parameter settings
9. Load a sample telemetry file and verify that it's both visible in the CKAN portal and accessible via its URL

## Prerequisities

This guide summarizes the [Install CKAN from Source](http://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html) documentation on the CKAN website. Consult that site for complete information.

The following setup is recommended for a basic evaluation:

* [Ubuntu 14.04.03 LTS (64-bit)](https://wiki.ubuntu.com/TrustyTahr/ReleaseNotes?_ga=1.253912650.374798248.1451753044). Use the desktop version if you want to evaluate Robolog in a self-contained environment.
* 4.0GB (4096MB) of RAM
* 10GB of disk space (minimum). Each Robolog telemetry file will use between 2MB-3MB of space (uncompressed).

The guide assumes the use of CKAN 2.5.1 and Python 2.7.6.

## Create an Ubuntu server using your own hardware or a hosted VM

If you've never installed Ubuntu, consider following the [Ubuntu Installation Tutorial for FRC](Ubuntu Installation Tutorial for FRC.md). That tutorial will guide you through the installation of Oracle VirtualBox and Ubuntu Desktop 14.04 LTS.

## Make the server accessible to external clients (optional)

A publicly-visible IP address is required if you want to access CKAN from external web browsers and programs. Network setup will vary depending on how Ubuntu has been deployed. For VirtualBox see the VirtualBox documentation section on [virtual networking](http://www.virtualbox.org/manual/ch06.html).

NOTE: this is an optional step. You can use Firefox from the Ubuntu desktop to connect to CKAN locally. If you decide to configure Ubuntu as a network host, change the "127.0.0.1" references below to the assigned IP address for your Ubuntu instance.

## Download and configure the CKAN prerequisites

Install the Ubuntu package prerequisites:

    sudo apt-get install python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty openjdk-7-jdk python-pastescript python-pylons

Create the required CKAN directories and set permissions:

    cd $HOME
    mkdir -p ~/ckan/lib
    sudo ln -s ~/ckan/lib /usr/lib/ckan
    mkdir -p ~/ckan/etc
    sudo ln -s ~/ckan/etc /etc/ckan
    
    sudo mkdir -p /usr/lib/ckan/default
    sudo chown `whoami` /usr/lib/ckan/default
    sudo mkdir -p /usr/lib/ckan/default
    sudo chown `whoami` /usr/lib/ckan/default

    sudo mkdir  /var/lib/ckan
    sudo chown `whoami` /var/lib/ckan
    
Setup a Python virtual environment for CKAN, then activate it in your shell:

    virtualenv --no-site-packages /usr/lib/ckan/default
    . /usr/lib/ckan/default/bin/activate

## Download and install the CKAN source code package

Install the CKAN software from source:

    pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.5.1#egg=ckan'
    
Install the python packages required by CKAN: 

    pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt

## Configure CKAN-related directories and configuration files and the CKAN repository 
    
Deactivate, then re-initialize the Python virtual environment

    deactivate
    . /usr/lib/ckan/default/bin/activate

Create the postgres user and database used by CKAN.  Give the 'ckan_default' user the password 'frc2016':
    
    sudo -u postgres createuser -S -D -R -P ckan_default
    sudo -u postgres createdb -O ckan_default ckan_default -E utf-8
    
Create a CKAN development configuration file:

    paster make-config ckan /etc/ckan/default/development.ini
    
Use vi (or another Linux editor) to make the following changes to the development.ini file:

    vi /etc/ckan/default/development.ini
	
	# the following are settings in the file, not shell commands:
	
	sqlalchemy.url = postgresql://ckan_default:frc2016@localhost/ckan_default
	ckan.site_url = http://127.0.0.1:5000
	solr_url=http://127.0.0.1:8983/solr
	ckan.storage_path = /var/lib/ckan


Use vi (or another Linux editor) to make the following changes to /etc/defaut/jetty:

    sudo vi /etc/default/jetty

	# the following are settings in the file, not shell commands:

	NO_START=0            
	JETTY_HOST=127.0.0.1
	JETTY_PORT=8983
	JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/

Configure Solr to work with CKAN:

    sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml

Download and install JSP support for Jetty, then restart the service:

    cd $HOME/Downloads
    wget 'https://maven-us.nuxeo.org/nexus/content/repositories/public/jetty/jsp/2.1-6.0.2/jsp-2.1-6.0.2.jar'
    sudo cp jsp-2.1-6.0.2.jar /usr/share/jetty/lib/.
    sudo service jetty restart

Initialize the CKAN database:

    cd /usr/lib/ckan/default/src/ckan
    paster db init -c /etc/ckan/default/development.ini
    
Initialize CKAN security, giving the 'sysadmin' account the password 'frc2016':

    cd /usr/lib/ckan/default/src/ckan
    ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini
    paster sysadmin add sysadmin -c /etc/ckan/default/development.ini

## Test your installation

Start CKAN

    cd /usr/lib/ckan/default/src/ckan
    paster serve /etc/ckan/default/development.ini

*Tip*: to start CKAN so it remains running in the backgroup after you log out of Ubuntu, type:

    nohup serve /etc/ckan/default/development.ini &
    
From the Ubuntu desktop, launch Firefox and navigate to the CKAN URL (http://127.0.0.1:5000).  Click "login", if you see the following log page you have successfully started CKAN:

![alt text](images/login.png)

Once you've logged in, click on the "sysadmin" user in the upper right hand corner of the screen:

![alt text](images/sysadmin.png)

At the bottom left hand side of the screen you will find your CKAN API Key. Copy this to the clipboard and save it in a file.

![alt text](images/apikey.png)

From the _Organizations_ menu, create an organization using your FRC team number:

![alt text](images/add_organization.png)

## Clone the Robolog repository to access the client scripts

    cd $HOME
    git clone https://github.com/Juxtapose-Technologies/Robolog.git
    cd Robolog/client
    
## Create your Team's "robolog.cfg" file with the appropriate parameter settings

Use vi (or another Linux editor) to changes the _set_robolog_cfg.sh_ file.  Replace values in "< >" with values specific to your installation and team:

    vi ./set_robolog_cfg.sh

	# the following are settings in the file, not shell commands:
	
	--ckan_apikey <API Key> \
    --ckan_author "My Name" \
    --ckan_author_email myemail@email.com \
    --ckan_maintainer "My Name" \
    --ckan_maintainer_email myemail@email.com \
    --ckan_name practicedata \
    --ckan_notes "Log generated during team practice" \
    --ckan_owner_org <team-NNNN> \
    --ckan_title "Upload Test #1"  \
    --ckan_version 0.9 \
    --cfg_file robolog.cfg \
    --district <DISTRICT> \
    --driver <DRIVER> \
    --event PRACT \
    --eventlat 48.101 \
    --eventlon -122.799 \
    --match P1 \
    --robot <ROBOT_NAME> \
    --server http://127.0.0.1:5000 \
    --station station1 \
    --teamname <TEAMNAME> \
    --teamnumber <TEAMNUMBER>
 
*Tip*: strings with spaces should be enclosed in quotation marks.
 
After saving this script, execute it:
 
    ./set_robolog_cfg.sh
    
Review the robolog.cfg file to make sure that your settings are correct:
 
    cat ./robolog.cfg

## Load a sample telemetry log file and verify that it's visible in the CKAN portal and accessible via its URL

Execute the _create_robolog_dataset to create a "container" for our practice file:
 
    ./create_robolog_dataset.sh
    
If the dataset has been successfully created you'll see output like this:

    frc@frc-VirtualBox:~/FRC-2016/Robolog/client$ ./create_robolog_dataset.sh 
    Attempting to create dataset "practicedata" on http://127.0.0.1:5000 using the config file "robolog.cfg"
    {u'help': u'http://127.0.0.1:5000/api/3/action/help_show?name=package_create',
     u'result': {u'author': u'My Name',
                 u'author_email': u'myemail@email.com',
                 u'creator_user_id': u'34684373-3d67-4257-b5cf-351b21b0f30d',
                 u'extras': [],
                 u'groups': [],
                 u'id': u'58bc513a-cd9c-409f-b856-4e40d60bfc86',
                 u'isopen': False,
                 u'license_id': None,
                 u'license_title': None,
                 u'maintainer': u'My Name',
                 u'maintainer_email': u'myemail@email.com',
                 u'metadata_created': u'2016-01-08T23:16:46.170005',
                 u'metadata_modified': u'2016-01-08T23:16:46.250940',
                 u'name': u'practicedata',
                 u'notes': u'Log generated during team practice',
                 u'num_resources': 0,
                 u'num_tags': 10,
                 u'organization': {u'approval_status': u'approved',
                                   u'created': u'2016-01-08T15:16:40.022003',
                                   u'description': u'',
                                   u'id': u'720c7ff4-67ab-4939-ab0c-f17686f82646',
                                   u'image_url': u'',
                                   u'is_organization': True,
     ...
     # truncated

Manually execute the create_robolog_resource.py program to load the practice dataset:

    python create_robolog_resource.py --metrics_file practicedata.json --config_file robolog.cfg --description "Our first data upload" -d

If the file has been successfully upload you'll see output like this:

    (default)frc@frc-VirtualBox:~/FRC-2016/Robolog/client$ ./create_robolog_resource.sh 
    Attempting to upload "practicedata.json" to http://127.0.0.1:5000 using the config file "robolog.cfg"
    {u'help': u'http://127.0.0.1:5000/api/3/action/help_show?name=resource_create',
     u'result': {u'cache_last_updated': None,
                 u'cache_url': None,
                 u'created': u'2016-01-08T16:15:06.412852',
                 u'description': u'Our first data upload',
                 u'format': u'JSON',
                 u'hash': u'',
                 u'id': u'a0680ee0-c7de-45cb-8b60-c8b42474bd3c',
                 u'last_modified': u'2016-01-09T00:15:06.298837',
                 u'mimetype': None,
                 u'mimetype_inner': None,
                 u'name': u'practicedata.json',
                 u'package_id': u'4b11daaf-abe5-4a22-8b1d-67f899fcd659',
                 u'position': 0,
                 u'resource_type': None,
                 u'revision_id': u'3faff7b0-f01d-4ccd-a025-8616c3bb7e55',
                 u'size': None,
                 u'state': u'active',
                 u'url': u'http://127.0.0.1:5000/dataset/4b11daaf-abe5-4a22-8b1d-67f899fcd659/resource/a0680ee0-c7de-45cb-8b60-c8b42474bd3c/download/practicedata.json',
                 u'url_type': u'upload',
                 u'webstore_last_updated': None,
                 u'webstore_url': None},
     u'success': True}
    Done

To verify and view the uploaded metrics file, click on "Datasets', then click on "Upload Test #1" : 

![alt text](images/successful_dataset.png)

Select "Explore" on the button next to "practicedata.json":

![alt text](images/successful_resource.png)

Click on the URL:

![alt text](images/more_information_resource.png)

You should see raw JSON output similar to this:

![alt text](images/json_output.png)
    
    
  
    
    