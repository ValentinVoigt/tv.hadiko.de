#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Based on epgstuff's epg2xml.py

# Import libs/modules
import os
import re
import sys
import time
import json
import getopt
import datetime
import subprocess

# Config
dvbsnoop = 'dvbsnoop'
# tsudprecv = 'tsudpreceive'
tsudprecv = '/usr/src/epgstuff/tsudpreceive/a.out'

def usage():
	print('Usage: ')
	print('\n\t./%s <options> <Input address/device number>' % sys.argv[0].replace('./', ''))
	print('Options:')
	print('\t\t-t <type>\t- Input type, stream or adapter\t(default: stream)')
	print('\t\t-o <file>\t- Output filename or - for stdin\t(default: -)')
	print('\t\t-d <count>\t- Duplicate packet limit\t\t(default: 50000)')
	print('\t\t-v\t\t- Verbose output')
	print('\t\t-h\t\t- This help message\n')
	print('Example:')
	print('\tGenerate JSON from unicast/mulitcast stream')
	print('\t\t./%s -t stream -o output.json -d 10000 235.1.2.3:12345' % sys.argv[0].replace('./', ''))
	print('\t\t./%s 235.1.2.3:12345' % sys.argv[0].replace('./', ''))
	print('\tGenerate JSON from DVB adapter')
	print('\t\t./%s -t adapter -o output.json -d 10000 0' % sys.argv[0].replace('./', ''))
	print('\t\t./%s -t adapter' % sys.argv[0].replace('./', ''))

def die(error):
	print("Error: %s\n" % error)
	usage()
	sys.exit(1)

class EPGDepsFailedException(Exception):
	pass

class EPGReader():

	verbose = False
	max_duplicates = 10000
	in_type = "stream"

	def check_deps(self):
		"""
		Checks for dependecy errors.
		@throws EPGDepsFailedException if dependencies are not met.
		"""
		programs = [tsudprecv]

		for program in programs:
			try:
				p = subprocess.Popen([program], stdout=self.devnull, stderr=self.devnull)
				output1 = p.communicate()[0]

				if not (p.returncode in [0, 255]):
					raise OSError()
			except OSError:
				raise EPGDepsFailedException('%s was not found.\n' % program)

		if not self.in_type in ['stream', 'adapter']:
			raise EPGDepsFailedException("EPGReader.in_type must be in ['stream', 'adapter'] (is %s)." % self.in_type)
	
		try:
			assert int(self.max_duplicates > 0)
		except:
			raise EPGDepsFailedException('Invalid duplicate packets count: %s' % self.max_duplicates)

		if self.verbose:
			print("Dependecy checks\t\t\tpassed")

	def read(self):
		# Variable initializiation
		dup_counter = 0
		packet_counter = 0
		slist = []
		epg = {}
		sid = ''; tid = ''; dur = ''
		enm = ''; lcd = ''; tnm = ''

		# Build command
		if self.in_type == 'stream':
			ipaddr, port = self.in_source.split(':')
			sniff_cmd = '%s %s %s' % (tsudprecv, ipaddr, port)
			sniff_cmd += ' | dvbsnoop -if - -s ts -tssubdecode 0x12 -nph -ph 0'
			if self.verbose:
				print('Input type:\t\t\t\tmulticast')
				print('Snooping EPG from\t\t\tudp://%s:%s' % (ipaddr, port))
		else:
			sniff_cmd = 'dvbsnoop -n 5000000 -dvr %s -nph 0x12' % (in_source, )
			if self.verbose:
				print('Input type:\t\t\t\tDVB adapter')
				print('Snooping EPG from\t\t\t/dev/dvb/adapter%s/dvr%s' % (in_source, in_source))
		
		# Start snooping
		snoop_proc = subprocess.Popen(sniff_cmd,
				bufsize=-1, shell=True,
				stdout=subprocess.PIPE,
				stderr=self.devnull)

		# Analyze output
		while dup_counter < int(self.max_duplicates):
			line = snoop_proc.stdout.readline()

			# Visual stuff
			packet_counter += 1
			if packet_counter % 1000 == 0 and self.verbose:
				sys.stdout.write('\rRecived packets\t\t\t\t%s/%s' % (dup_counter, self.max_duplicates))
				sys.stdout.flush()
			
			# Line parsing
			if line == None:
				print('dvbsnoop exited.\n')
				break
			elif 'Service_ID' in line:
				sid = re.findall('Service_ID: (.*) \(', line)[0].strip()
			elif 'Transport_stream_ID:' in line:
				tid = re.findall('Transport_stream_ID: (.*) \(', line)[0].strip()
			elif 'Transport_Stream_ID:' in line:
				tid = re.findall('Transport_Stream_ID: (.*) \(', line)[0].strip()
			elif line.find('Duration') > 1:
				dur = re.findall('\[\=  (.*) \(', line)[0].strip()
				try:
					hr, mi, sc = map(int, dur.split(':'))
					duration = datetime.timedelta(hours=hr, minutes=mi, seconds=sc)
				except: continue
			elif line.find('event_name:') > 1:
				enm = re.findall('event_name: "(.*)"', line)[0].strip()
			elif line.find('language_code') > 1:
				lcd = re.findall('language_code: (.*)', line)[0].strip()
			elif line.find('text_char') > 1:
				tnm = re.findall('text_char: "(.*)"', line)[0].strip()
				sdtime = '%s@%s@%s' % (str(stime), sid, tid)
				try: etime = stime + duration
				except: continue
				if not etime:
					print("Can't parse time [%s]. Skipping!\n" % stime)
					continue

				if sdtime in slist:
					dup_counter += 1
				else:
					slist.append(sdtime)
					if not sid in epg.keys():
						epg[sid] = []
					epg[sid].append({
						'sid': sid,
						'tid': tid,
						'duration': duration.seconds,
						'name': enm.decode('iso-8859-5').encode('utf-8', 'replace'),
						'language': lcd,
						'description': tnm.decode('iso-8859-5').encode('utf-8', 'replace'),
						'start': stime.isoformat(),
						'end': etime.isoformat(),
					})

				enm = ''; lcd = ''; tnm = ''
			elif line.find('Start_time:') > 1:
				stime = " ".join(line.split()[3:][:2])
				time_format = '%Y-%m-%d %H:%M:%S'
				try: stime = datetime.datetime.strptime(stime, time_format)
				except:	continue
		
		if self.verbose:
			print("\n")
		snoop_proc.stdout.flush()
		snoop_proc.stdout.close()
		snoop_proc.terminate()

		return epg

	def __enter__(self):
		self.devnull = open(os.devnull, 'w')
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		# Kill all procs
		# Is this really necessary?
		kill_cmds = []# [dvbsnoop, tsudprecv]
		
		for cmd in kill_cmds:
			cmd = 'killall -9 %s' % cmd
			subprocess.Popen(cmd, shell=True, stdout=self.devnull, stderr=self.devnull)

		# Close /dev/null
		try:
			self.devnull.close()
		except:
			pass

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:o:d:vh")
	except getopt.GetoptError as err:
		die(err)

	if len(args) != 1:
		die("Please add input address / device number.")

	with EPGReader() as epg:
		epg.in_source = args[0]

		for param, value in opts:
			if param == '-h':
				usage()
				sys.exit(0)
			if param == '-t':
				epg.in_type = value
			elif param == '-v':
				epg.verbose = True
			elif param == '-d':
				epg.max_duplicates = value
			elif param == '-o':
				if value in ('', '-'):
					output = sys.stdout
				else:
					output = open(value, 'w+')

		epg.check_deps()
		epg_data = epg.read()

		output.write(json.dumps(epg_data) + "\n")
		output.flush()
		output.close()

if __name__ == '__main__':
	main()
