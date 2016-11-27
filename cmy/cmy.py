#!/usr/bin/env python
# cmy:- c-mee
# DUMP your thoughts and CLEAR your mind using c-mee.
# Version : v1-beta 
# email:- cmy.project.mail@gmail.com
# cmy is short form of Clear Mind YAML

import yaml
import datetime
import os
import sys

# Create the yaml file, if it does not exist.
def create_yaml_file(cmy_dir, now):
	if not os.path.exists(cmy_dir):
		os.makedirs(cmy_dir)
	yaml_file = yaml_fp_creator(cmy_dir, now)
	if not os.path.exists(yaml_file):
		yaml_data_dict = first_log_entry(now)
		yaml_data_final = yaml_printer(yaml_data_dict)
		with open(yaml_file, 'w') as yaml_fd:
			yaml_fd.write(yaml_data_final)

# Common function for writing the final data to YAML file.
def write_yaml_file(yaml_file, yaml_data_final):
	with open(yaml_file,'w') as yaml_fd:
		yaml_fd.write(yaml_data_final)

# Common function for creating full path to current YAML file
def yaml_fp_creator(cmy_dir, now):
	yaml_file = cmy_dir+"/"+now[2]+"_"+now[3]+".yaml"
	return yaml_file

# Generate time and date fileds. 
def ttmy():
	now = datetime.datetime.now()
	month = now.strftime("%b").upper()
	day_of_the_month = now.strftime("%d")
	day_of_the_week = now.strftime("%a").upper()
	# time = 1315
	time = now.strftime("%H%M")
	# today = 24_JUN_FRI
	today = day_of_the_month+"_"+month+"_"+day_of_the_week
	# year = 2016
	year = now.strftime('%G')
	return time, today, month, year

# Common function for reading the contents in YAML.
def read_yaml_file(yaml_file):
        try:
                yaml_fd = open(yaml_file, 'r')
                yaml_raw_data = yaml.load(yaml_fd) or {}
        except IOError:
	        print "Error opening cmy.conf."
		sys.exit()
    
	return yaml_raw_data

# list command function
def list_cmd(args, cmy_dir, now):
	#print args
	yaml_file = yaml_fp_creator(cmy_dir, now)
	yaml_raw_data = read_yaml_file(yaml_file)
	if (len(args) > 2):
		if args[2] == "today":
			log_today = now[1]
			yaml_raw_data = yaml_raw_data[log_today]
			yaml_data_final = yaml_printer(yaml_raw_data)
			print now[1]+":"
			return yaml_data_final
	else:
		yaml_data_final = yaml_printer(yaml_raw_data)
		return yaml_data_final

# convert YAML data in dict to YAML writable format.		
def yaml_printer(yaml_data_dict):
	yaml_data_final = yaml.dump(yaml_data_dict, default_flow_style=False)
	return yaml_data_final

# The first entry in any YAML file.
def first_log_entry(now):
	#yaml_data_dict = {now[1]:{'LOG00':{'TIME':'time', 'TYPE':'type', 'ENTRY':'entry'}}}
	yaml_data_dict = {now[1]:{'LOG0':{}}}
	return yaml_data_dict

# Common function to append YAML dict.
def x_log_entry(args, now, yaml_data_dict):
	#{log_today:{log_id:{'TIME':log_time, 'TYPE':log_type, 'ENTRY':'log_entry'}}}
	log_today = str(now[1])
	log_id = log_id_creator(yaml_data_dict, now)
	log_time = int(now[0])
	log_type = args[1]
	log_entry = str(' '.join(args[2:]))
	data_to_append = {'TIME':log_time,'TYPE':log_type,'ENTRY':log_entry}
	yaml_data_dict[log_today][log_id] = data_to_append
	yaml_data_final = yaml_data_dict
	return yaml_data_final

# Get the dictonary to modify
def log_dict_to_modify(yaml_raw_data, date_key):
	yaml_data_dict = yaml_raw_data[date_key]
	return yaml_data_dict

# info and todo cmds function
def info_todo_cmds(args, cmy_dir, now):
	yaml_file = yaml_fp_creator(cmy_dir, now)
	yaml_raw_data = read_yaml_file(yaml_file)
	yaml_data_dict_modified = x_log_entry(args, now, yaml_raw_data)
	yaml_data_final = yaml_printer(yaml_data_dict_modified)
	write_yaml_file(yaml_file, yaml_data_final)
	print "Saved.\nContinue your work buddy !!"

# Genereate LOG* to append.
def log_id_creator(yaml_raw_data, now):
	today = now[1]
	# Sorting LOG* keys.
	sorted_log_id_keys = sorted(yaml_raw_data[today].keys())
	# Incrementing LOGID. LOG0 to LOG1
	new_log_id_int = int(sorted_log_id_keys[-1].replace('LOG','')) + 1
	new_log_id = 'LOG'+str(new_log_id_int)
	return new_log_id

# Create "today" key & LOG0, if it is not present in the file.
def check_for_today_key(cmy_dir, now):
	yaml_file = yaml_fp_creator(cmy_dir, now)
	yaml_raw_data = read_yaml_file(yaml_file)
	today = now[1]
	if not yaml_raw_data.has_key(today):
		data_to_append = first_log_entry(now)
		yaml_raw_data[today] = data_to_append[today]
		yaml_data_dict_modified = yaml_raw_data
		yaml_data_final = yaml_printer(yaml_data_dict_modified)
		write_yaml_file(yaml_file, yaml_data_final)
def read_conf():
	cmy_conf = read_yaml_file("cmy.conf")

        #check empty dictionary
        if (not bool(cmy_conf)):
                print "cmy.conf is empty."
                sys.exit()

	cmy_dir = cmy_conf['cmy_dir']+"/logs"
	if ("cmy_dir" not in locals() or cmy_dir == ""):
		print "cmy_dir is empty or not defined. set a location for your logs."
		sys.exit()

	return cmy_dir

def starting_up():
	cmy_dir = read_conf()
	now = ttmy()
	args = 	sys.argv
	create_yaml_file(cmy_dir, now)
	check_for_today_key(cmy_dir, now)
	return args, now, cmy_dir

def start_here():
	args, now, cmy_dir = starting_up()

	if len(args) ==	 1:
		print "Supported options are show, info & todo"
	elif args[1] == "test":
		print "test"
		print yaml_fp_creator(cmy_dir)
	elif args[1] == "list":
		print list_cmd(args, cmy_dir, now)
	elif args[1] == "info":
		info_todo_cmds(args, cmy_dir, now)
	elif args[1] == "todo":
		info_todo_cmds(args, cmy_dir, now)
	else:
		print "enna maira"

if __name__ == '__main__':
	start_here()
