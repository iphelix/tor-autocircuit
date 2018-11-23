Tor Autocircuit was developed to give users a finer control over Tor circuit creation. The tool exposes the functionality of TorCtl library which allows its users to control circuit length, speed, geolocation, and other parameters.

In order to control the script, you must edit the source file and change the following default parameters in the *Configuration* section:

    # Number of circuits to build
    num_circs = 10

    # Do not use a country twice in a route 
    # [True --> unique, False --> same or None --> pass] 
    unique_countries    = True,

    # Configure max continent crossings in one path  
    # [integer number 0-n or None --> ContinentJumper/UniqueContinent]
    continent_crossings = 3,
        					
    # Configure max ocean crossings in one path 
    # [integer number 0-n or None --> OceanJumper/UniqueOcean]
    ocean_crossings     = 1,         

    # Specify countries for positions [single country code or None]
    entry_country       = None,
           
    # Specify countries for positions [single country code or None]
    middle_country      = None,
           
    # Specify countries for positions [single country code or None]
    exit_country        = None,      

    # List of countries not to use in routes 
    # [(empty) list of country codes or None]
    excludes            = None
    
    # Number of hops in circuits
    pathlen       = 3,

    # True   - produces exits in an ordered fashion for a specific port.
    # False  - If uniform is set to True, exists will be produced in a uniform fashion,
    #	   otherwise it produces exits in a bandwidth weighted fashion.
    order_exits   = False,
					    
    # Maximum percentile requirement of bandwidth rankings to be included in the circuit
    percent_fast  = 100,
          
    # Minimum percentile requirement of bandwidth rankings to be included in the circuit
    percent_skip  = 0,

    # Minimum hop bandwidth
    min_bw        = 1024,

    # True   - the same router can't appear more than once in a path, otherwise no path restriction
	# False  - no two nodes from the same /16 subnet can be in the path and the same router can't 
	#          appear more than once in a path. Set to False when using percent_fast or percent_skip
    use_all_exits = False,

    # True   - produces nodes in the uniform distribution
	# False  - produces nodes in the bandwidth weighted distribution
    uniform       = False,

    # Name of the exit node or None
    use_exit      = None,

    # True   - entry node must have "Guard", "Valid", and "Running" flags set
	# False  - entry node must have "Valid" and "Running" flags set
    use_guards    = True,
