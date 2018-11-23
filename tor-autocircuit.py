#!/usr/bin/python
# tor-autocircuit.py v.0.2 - automatically creates circuits and attaches streams
# according to predefined rules such as circuit geolocation, path length, etc.
#
# Note: enable tor config port 9051 by editing torrc file or starting tor
# with --torcontrol 9051 command line parameter
#
# Change History
# 0.2 - Fixed a single hop circuits bug. FastFirstHopPK=0 does the trick.
#       You will need to edit tor/src/or/control.c file.   Remove or comment 
#       out the following lines of code which limit one hop circuit creation:
#
#	  if (circ && (circuit_get_cpath_len(circ)<2 || hop==1)) {
#	    connection_write_str_to_buf(
#	                    "551 Can't attach stream to one-hop circuit.\r\n", conn);
#	    return 0;
#	  }
#
#	Also updated TorCtl library to the latest copy from svn
#
# 0.1 - initial release
#
#
# Author: iphelix

import os
import sys
import time
import socket

from TorCtl import *

###############################################################################
# Configuration

# Number of circuits to build
num_circs = 10

# Construct GeoIPConfig
geoip_config = GeoIPSupport.GeoIPConfig(
       unique_countries    = True, 	# Do not use a country twice in a route 
    				    	# [True --> unique, False --> same or None --> pass] 

       continent_crossings = 3,     	# Configure max continent crossings in one path 
    					# [integer number 0-n or None --> ContinentJumper/UniqueContinent]

       ocean_crossings     = 1,         # Configure max ocean crossings in one path 
   				 	# [integer number 0-n or None --> OceanJumper/UniqueOcean]

       entry_country       = None,      # Specify countries for positions [single country code or None]
       middle_country      = None,      # Specify countries for positions [single country code or None]
       exit_country        = None,      # Specify countries for positions [single country code or None]

       excludes            = None    	# List of countries not to use in routes 
    					# [(empty) list of country codes or None]
)  

# Construct SelectionManager
selmgr = PathSupport.SelectionManager(
      pathlen       = 3,       		# Number of hops in circuits

      order_exits   = False,       	# True   - produces exits in an ordered fashion for a specific port.
					# False  - If uniform is set to True, exists will be produced in a uniform fashion,
					#	   otherwise it produces exits in a bandwidth weighted fashion.

      percent_fast  = 100,		# Maximum percentile requirement of bandwidth rankings to be included in the circuit
      percent_skip  = 0,		# Minimum percentile requirement of bandwidth rankings to be included in the circuit

      min_bw        = 1024,		# Minimum hop bandwidth

      use_all_exits = False,		# True   - the same router can't appear more than once in a path, otherwise no path restriction
			   		# False  - no two nodes from the same /16 subnet can be in the path and the same router can't 
					#          appear more than once in a path. Set to False when using percent_fast or percent_skip

      uniform       = False,		# True   - produces nodes in the uniform distribution
					# False  - produces nodes in the bandwidth weighted distribution

      use_exit      = None,    		# Name of the exit node or None

      use_guards    = True,    		# True   - entry node must have "Guard", "Valid", and "Running" flags set
					# False  - entry node must have "Valid" and "Running" flags set

      geoip_config  = geoip_config
)



###############################################################################
# Build circuits

#Connect to TOR
try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(("localhost",9051))
	c = PathSupport.Connection(s)
	c.authenticate()
except socket.error, e:
	print "[!] Couldn't connect to TOR."
	sys.exit(-1)

# Configure TOR Environment 
c.set_events([TorCtl.EVENT_TYPE.CIRC,TorCtl.EVENT_TYPE.STREAM,TorCtl.EVENT_TYPE.ADDRMAP,TorCtl.EVENT_TYPE.NS,TorCtl.EVENT_TYPE.NEWDESC], True)
c.set_option("__DisablePredictedCircuits", "1")
c.set_option("__LeaveStreamsUnattached", "1")
c.set_option("FastFirstHopPK","0") # necessary for one-hop circuits

# Set up stream handler
handler = PathSupport.StreamHandler(c, selmgr, num_circs, GeoIPSupport.GeoIPRouter)

try:
	while True:
		time.sleep(60)
except KeyboardInterrupt:
	c.close()
	sys.exit(1)
