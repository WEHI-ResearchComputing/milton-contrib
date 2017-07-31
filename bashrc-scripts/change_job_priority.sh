# Change Job Priority: Qalter (modified for Milton)

# Qalter is a built-in feature of Torque, but Milton's architecture means that priorities set on Torquelord are not passed on to PBS. This script resolves that issue.
# By default, jobs have priority zero. Jobs with higher priority will run sooner than jobs with lower priority. Priorities range from -1023 to 1024.
# Priority only affects jobs that are in the node_waiting queue. Once a node is being built for your job, you are unable to change its priority.

# USAGE
# qalter [-h] [-p PRIORITY] [-t WAIT_TIME] [-n NUM_ATTEMPTS] PROC_ID
#   -h Print help and exit
#   -p PRIORITY: the new priority value (1023)
#   -n NUM_ATTEMPTS: number of attempts before giving up (5)
#   -t WAIT_TIME: numer of seconds to wait between attempts (10)
#   PROC_ID: Torque job id (required)

# EXAMPLES
# % qalter 42330
# Job 42330 (PBS ID 101048) set to priority -1023
# % qalter -p 100 42330
# Job 42330 (PBS ID 101048) set to priority 100

# RUN FIRST TIME
# % ssh hpc1-pbs mkdir -p .ssh
# % scp ~/.ssh/id_rsa.pub hpc1-pbs:.ssh/authorized_keys

# ADD TO BASHRC
qalter () {
  OPTIND=1
  PRIORITY=1023
  ATTEMPTS=5
  WAIT_TIME=10
  HELP="qalter (modified for Milton)
Scott Gigante, 2017-06-15
Usage: qalter [-h] [-p PRIORITY] [-t WAIT_TIME] [-n NUM_ATTEMPTS] PROC_ID"
  local arg
  while getopts 'hp:n:t:' arg
  do
    case ${arg} in
      h) echo "$HELP"; return 0;;
      p) PRIORITY=${OPTARG};;
      n) ATTEMPTS=${OPTARG};;
      t) WAIT_TIME=${OPTARG};;
      *) echo "$HELP" >&2; return 1 # illegal option
      esac
  done
  shift $(($OPTIND - 1))
  for PROC in $@; do
    PBS_ID=$(curl -ks "https://hpc1-pbs.wehi.edu.au/idmapping/get_pbs_id.php?headnode=$HOSTNAME&jobid=$PROC")
    if [ $( echo $PBS_ID | wc -c ) -eq 1 ]; then
      i=1
      while [ $( echo $PBS_ID | wc -c ) -eq 1 -a $i -lt $ATTEMPTS ]; do
        echo "PBS node ID request failed... (attempt $i of $ATTEMPTS) Trying again in 10 seconds."
        sleep $WAIT_TIME
        PBS_ID=$(curl -ks "https://hpc1-pbs.wehi.edu.au/idmapping/get_pbs_id.php?headnode=$HOSTNAME&jobid=$PROC")
        i=$(($i+1))
      done
      if [ $( echo $PBS_ID | wc -c ) -eq 1 ]; then
        echo "PBS ID request failed for job $PROC. Skipping."
        continue 2
      fi
    fi
    ssh hpc1-pbs qalter -p $PRIORITY $PBS_ID
    echo "Job $PROC (PBS ID $PBS_ID) set to priority $PRIORITY"
  done
}; export -f qalter
