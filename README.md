ckanext-OSED
===================

## Requirements

- CKAN 2.4+
- ckanext-scheming
- ckanext-fluent

## Update translations

To generate a new pot file use the following command::

    vagrant ssh
    source /home/vagrant/pyenv/bin/activate
    cd /var/www/ckanext/ckanext-osed/
    python setup.py extract_messages --mapping-file babel.cfg --output i18n/ckanext-osed.pot

Or follow the official CKAN guide at https://github.com/ckan/ckan/wiki/Translations-and-Extensions

All translations are done via Transifex. To compile the po files use the following command:

## Installation

To install:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the Python package into your virtual environment::

     pip install ckanext-osed

3. Add ``osed`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


## Development Installation

To install ckanext-osed for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/krishnatejaperannagari/OSED
    cd ckanext-osed
    python setup.py develop
    pip install -r dev-requirements.txt
    pip install -r requirements.txt
