#
# A simple utility to query the Milton monitor to get cluster configurations,
# summarise them and produce a report
#
# Requires python 3
#
# Author: Evan


import requests
import json
import sys


def get_as_json(url):
	return requests.get(url).json()

def increment(counter, key, value):
	if not key in counter:
		counter[key] = 0
	counter[key] = counter[key] + value

# List clusters
clusters = get_as_json('http://mrm.wehi.edu.au/clusters')['clusters']

# Get data for each cluster
total_cores  = 0
max_core     = 0
total_ram    = 0
host_cnt     = 0
guest_cnt    = 0
core_details = dict()
min_ram      = sys.maxsize
max_ram      = 0

for cluster in clusters:
	cluster_detail = get_as_json('http://mrm.wehi.edu.au/cluster-detail/'+cluster['name'])
	hosts = cluster_detail['hosts']
	guests = cluster_detail['guests']

	host_cnt = host_cnt + len(hosts)
	for guest in guests:
		if guest['powerState'] == 'Powered On':
			guest_cnt = guest_cnt + 1

	for host in hosts:
		num_cpu = host['numCpu']
		max_core = max(max_core, num_cpu)
		total_cores = total_cores + num_cpu
		ram = host['memory']/1024/1024/1024
		total_ram = total_ram + ram
		min_ram = min(min_ram, ram)
		max_ram = max(max_ram, ram)
		increment(core_details, host['cpuModel'], num_cpu)


print(f'Total cores: {total_cores}')
print(f'Total ram: {total_ram/1024}TB')
print(f'Physical hosts: {host_cnt}')
print(f'Total guests: {guest_cnt}')
print('Core details:')
print(f'Largest memory machine: {max_ram/1024}TB')
print(f'Largest core count: {max_core}')
for (k, v) in core_details.items():
	print(f'   {k} - {v} cores')
