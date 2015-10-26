# About

Services for Synology Box.

Service for removing forbidden files from folder of internal users.

And copy user files for security department.

# Deploy

## SSH

### Generate keys

```
ssh-keygen -t rsa -C "boxmanager@your_synology" -f ~/.ssh/your_synology
```

### Make home dir

```
mkdir -p /home/boxmanager
chown boxmanager:administrators /home/boxmanager
```

### Copy ssh keys to host

```
  ssh-copy-id boxmanager@your_ip
  -or-
  cat ~/.ssh/your_synology.pub | ssh boxmanager@your_ip "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"

  cd cd /var/services/homes/boxmanager/
  chmod 700 .ssh
  chmod 640 .ssh/authorized_keys
```

### Config sshd

```
scp sshd_config root@your_ip:/etc/ssh/sshd_config
```

### Restart SSHD

```
synoservicectl --reload sshd
```

## Rsync

```
cd backup
./run_backup.sh
```

## SU command

```
chmod 4755 /bin/busybox
su - -c whoami
```

## Logrotate.d

```
touch /etc/logrotate.d/cp_usr_folders_to_mirror
touch /etc/logrotate.d/clear_usr_folders

logrotate -d /etc/logrotate.d/clear_usr_folders
```

## Config Groups

```
vi /etc/passwd
change boxmanager:x:1026:100: to boxmanager:x:1026:101:
```

## Crond

```
synoservicectl --restart crond
```

## Python

### setup-tools

```
wget https://bootstrap.pypa.io/ez_setup.py
python ez_setup.py
```

### PIP

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
scp get-pip.py root.dropbox.pik:~/src

python get-pip.py

pip install -U setuptools
```

### watchdog

```
pip install watchdog
```

## Remove forbidden file daemon

```
chmod 755 /usr/syno/etc.defaults/rc.d/S99rmforbiddenfiles.sh
<!-- /usr/local/etc/rc.d -->
```

### Restart

```
/usr/syno/etc.defaults/rc.d/S99rmforbiddenfiles.sh restart
```

### Log

```
/volume1/homes/log/rm_forbidden_files_daemon.log
```

## httpd - Redirect 5001 to 443

### Config

```
scp ./etc/httpd/conf/httpd-redirect-vh.conf-user root.your_ip:/etc/httpd/conf/
```

edit /etc/httpd/conf/httpd.conf-user

```
  Include conf/httpd-redirect-vh.conf-user
```

### Write config

```
/usr/syno/etc/rc.sysv/httpd-user-conf-writer.sh
```

### Restart

```
/sbin/initctl stop httpd-user
/sbin/initctl start httpd-user
```
