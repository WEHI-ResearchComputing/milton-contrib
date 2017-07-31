# Access Job Host
# Finds Milton hosts running a particular Torque job, and accesses the host by ssh if only one host is found

# USAGE
# % host [PROC_ID]
#   PROC_ID Torquelord job id. Optional but recommended.

# EXAMPLES
# % host
# torque_big-95435-n1.hpc.wehi.edu.au
# torque_big-95447-n1.hpc.wehi.edu.au
# torque_big-95453-n1.hpc.wehi.edu.au
# % host 95345
# runs `ssh torque_big-95435-n1.hpc.wehi.edu.au`

# ADD TO BASHRC
host () {
  PROC=$1
  HOSTS=$(qstat -u $USER -rnt1 $PROC | tail -n +6 | sed "s/.* //" | tr + "\n")
  if [ $(echo "$HOSTS" | wc -l) -eq 1 ]
    then
    ssh $HOSTS
  else
    echo "$HOSTS"
  fi
}; export -f host
