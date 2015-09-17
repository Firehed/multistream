#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCEDIR="$SCRIPTDIR/../"
TARGETUNAME=kbmod
TARGETSERVER=bdir.multistre.am
TARGETDIR=/var/virtualenv/multistream/files/

rsync -rvz --delete -e 'ssh' --exclude '*.pyc' --exclude '__pycache__' --exclude '.git' --exclude 'site_specific_settings.py' --exclude 'multistream.db' "$SOURCEDIR" ${TARGETUNAME}@$TARGETSERVER:"$TARGETDIR"
