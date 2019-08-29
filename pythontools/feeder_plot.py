import csv 
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as matplotlib
import glmptime as glmptime
import numpy as np
skip_names=['Total Number of Houses per Phase', 'Run Name', "", 'Start Time', 'Stop Time', "Weather File"]
filename_perc = []
with open('config/simulation_configuration.csv', newline='') as config_file : 
	fc = csv.reader(config_file, delimiter=',', quotechar='|')
	for line in fc : 
		if line[0] in skip_names: 
			continue
		else : 
			filename_perc.append([str(line[0]).replace(" ", "_"), float(line[1])])

path = 'output/feeder_power/'
max_real = []
max_reac = []
energy_per_run = []
plt.figure(1)
files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith( ".csv" )]
files_sorted=sorted(filename_perc, key=lambda x: x[1])
for file_tuple in files_sorted :
	file = 'feeder_'+file_tuple[0]+'.csv'
	time_stamp = []
	real_power = []
	reactive_power = []
	tmp_label=[]
	with open(path+file, newline='') as csvfile : 
		fr = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in fr : 
			if '#' in row[0] : 
				continue 
			else : 
				time_stamp.append(glmptime.glmptime(row[0]))
				real_power.append(float(row[1][:-3]))
				reactive_power.append(float(row[2][:-4]))
		energy_per_run.append([file[:-4],sum(real_power)])
		max_real.append([file[:-4], max(real_power)])
		max_reac.append([file[:-4], max(reactive_power)])
		for p in filename_perc : 
			if file[7:-4] in p[0] : 
				tmp_label=round(float(p[1])*100)
		plt.plot(time_stamp, real_power, label=str(tmp_label)+'% Electrification')
		# plt.plot(time_stamp, reactive_power, label='reactive_'+file[:-4])
plt.gcf().autofmt_xdate()
myFmt = md.DateFormatter('%y-%m-%d %H:%M:%S')
plt.gca().xaxis.set_major_formatter(myFmt)
plt.legend()
plt.tight_layout()
tmp = plt.gcf() # get current figure
plt.xlabel("Time")
plt.ylabel("Power [kW]")
plt.draw()
tmp.set_size_inches(21.5, 10.5)
tmp.savefig("output/feeder_plot/feeder_timeseries.png")

plt.figure(2)
for i in max_real : 
	for p in filename_perc : 
		if p[0] in i[0] : 
			plt.scatter(p[1], i[1])
tmp_1 = plt.gcf() # get current figure
plt.draw()
plt.xlabel("Electrification Fraction")
plt.ylabel("Peak feeder power [kW]")
tmp_1.savefig("output/feeder_plot/peak_power.png")