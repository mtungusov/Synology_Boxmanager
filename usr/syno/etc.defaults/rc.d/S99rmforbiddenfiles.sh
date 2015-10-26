#!/bin/sh
#
PROCNAME="S99rmforbiddenfiles"
LOGGER="/usr/bin/logger"

CMD="/usr/bin/nohup /home/boxmanager/bin/rm_daemon.py"
# LOG="/volume1/homes/log/rm_forbidden_files_daemon.log"
PIDFILE=/var/run/$PROCNAME.pid

log_msg()
{
  $LOGGER -sp $1 -t $PROCNAME "$2"
}

case "${1}" in
start)
  if [ -e $PIDFILE ] ; then
     echo "$PROCNAME already running. PID=`cat $pidfile`"
     exit
  fi
  /usr/bin/logger -t "$PROCNAME" -p error "Starting RmDaemon"
  log_msg err "Starting RmDaemon..."
  echo "Starting RmDaemon: "
  $CMD > /dev/null 2>&1 &
  # echo $! > $PIDFILE
  ;;
stop)
  if [ -e $PIDFILE ] ; then
    /usr/bin/logger -t "$PROCNAME" -p error "Stopping RmDaemon"
    log_msg info "Starting RmDaemon..."
    echo "Stopping RmDaemon..."
    kill `cat $PIDFILE`
    # rm $PIDFILE
  else
    echo "RmDaemon is not running. No PID file."
  fi
  ;;
restart)
  $0 stop
  sleep 5
  $0 start
  ;;

*) echo "Usage: ${PROCNAME} {start|stop|restart}"
   exit 1
   ;;
esac
