# View job output
# Read stdout and stderr for ongoing jobs

# USAGE
# {stderr,stdout} PROC_ID
#   PROC_ID The Torque job to be viewed (must be running)

# EXAMPLES
# stderr 95345 | less
# stdout 95345 > temp.log

# ADD TO BASHRC
stdout () {
  # change array jobs from 1234[1] to 1234-1
  PROC=$(echo "$1" | sed 's/\[\([0-9]*\)\]/-\1/g')
  cat /stornext/HPCScratch/.torque/spool/$PROC.$HOSTNAME.OU
}; export -f stdout
stderr () {
  # change array jobs from 1234[1] to 1234-1
  PROC=$(echo "$1" | sed 's/\[\([0-9]*\)\]/-\1/g')
  cat /stornext/HPCScratch/.torque/spool/$PROC.$HOSTNAME.ER
}; export -f stderr
