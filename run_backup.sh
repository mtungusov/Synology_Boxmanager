#!/usr/bin/env sh

CMD="rsync -azh --progress your_remote_user.your_hostname:"

BACKUPDIR="/Users/your_local_user/fileexchange/backup"

if [ ! -d "$BACKUPDIR/etc" ]; then
  mkdir -p $BACKUPDIR/etc
fi
$CMD/etc/passwd $BACKUPDIR/etc
$CMD/etc/group $BACKUPDIR/etc
$CMD/etc/crontab $BACKUPDIR/etc

if [ ! -d "$BACKUPDIR/etc/logrotate.d" ]; then
  mkdir -p $BACKUPDIR/etc/logrotate.d
fi
$CMD/etc/logrotate.d/clear_usr_folders $BACKUPDIR/etc/logrotate.d/
$CMD/etc/logrotate.d/cp_usr_folders_to_mirror $BACKUPDIR/etc/logrotate.d/
$CMD/etc/logrotate.d/rm_forbidden_files $BACKUPDIR/etc/logrotate.d/

if [ ! -d "$BACKUPDIR/etc/ssh" ]; then
  mkdir -p $BACKUPDIR/etc/ssh
fi
$CMD/etc/ssh/sshd_config $BACKUPDIR/etc/ssh

$CMD/home $BACKUPDIR

if [ ! -d "$BACKUPDIR/volume1/homes/etc" ]; then
  mkdir -p $BACKUPDIR/volume1/homes/etc
fi
$CMD/volume1/homes/etc $BACKUPDIR/volume1/homes

if [ ! -d "$BACKUPDIR/usr/syno/etc.defaults/rc.d" ]; then
  mkdir -p $BACKUPDIR/usr/syno/etc.defaults/rc.d
fi
$CMD/usr/syno/etc.defaults/rc.d/S99rmforbiddenfiles.sh $BACKUPDIR/usr/syno/etc.defaults/rc.d
