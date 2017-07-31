# Reliable Logging Qsub

# Ensures that Torque log files are not "lost" when qsub is invoked from an unusual location
# This will override the standard qsub command

# RUN FIRST TIME
# % mkdir -p ~/torque_logs/

# ADD TO BASHRC
alias qsub="qsub -o ~/torque_logs/ -e ~/torque_logs/"
