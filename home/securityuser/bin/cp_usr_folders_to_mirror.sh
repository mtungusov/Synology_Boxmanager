#!/bin/sh

DST="/volume1/homes/.security_mirror"
SNAPSHOT="$DST/snapshot/`date \+\%Y_\%m_\%d`"
SRC="/volume1/[I,E]_*"
# SRC1="/volume1/E_*"

# Make snapshot dir
if [[ ! -d $SNAPSHOT ]]; then
  mkdir -p $SNAPSHOT
fi

rsync -ahv --delete --backup --backup-dir=$SNAPSHOT $SRC $DST

# 0,5,10,15,20,25,30,35,40,45,50,55        *        *        *        *        root        /home/securityuser/bin/cp_usr_folders_to_mirror.sh 2>&1 >> /volume1/homes/.security_mirror/cp_usr_folders_to_mirror.log
