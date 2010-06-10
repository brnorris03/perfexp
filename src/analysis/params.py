import ConfigParser

class ANSParams:

    ansparams = {'DEBUG':None, 'resultsdir':None, 'programevent':None, 'metric':None, 'metricparams':None, 'xaxislabel':None, 'yaxislabel':None, 'graphtitle':None, 'mhz':None, 'ptool':None, 'l2cache':None, 'plotfilename':None}	

    def _processConfigFile(self):
        
        mysection = 'Analysis'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.ansparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.ansparams['resultsdir'] = self.config.get(mysection, 'resultsdir')
        
        except:
            raise Exception('Error: could not find resultsdir in configuration file %s' % self.config_file)

        try:
            self.ansparams['programevent'] = self.config.get(mysection, 'programevent')
        
        except:
            raise Exception('Error: could not find programevent in configuration file %s' % self.config_file)

        try:
            self.ansparams['metric'] = self.config.get(mysection, 'metric')
        
        except:
            raise Exception('Error: could not find metric in configuration file %s' % self.config_file)

        try:
            self.ansparams['metricparams'] = self.config.get(mysection, 'metricparams')
        
        except:
            raise Exception('Error: could not find metricparams in configuration file %s' % self.config_file)

        try:
            self.ansparams['xaxislabel'] = self.config.get(mysection, 'xaxislabel')
        
        except:
            raise Exception('Error: could not find xaxislabel in configuration file %s' % self.config_file)


        try:
            self.ansparams['yaxislabel'] = self.config.get(mysection, 'yaxislabel')
        
        except:
            raise Exception('Error: could not find yaxislabel in configuration file %s' % self.config_file)

        try:
            self.ansparams['graphtitle'] = self.config.get(mysection, 'graphtitle')
        
        except:
            raise Exception('Error: could not find graphtitle in configuration file %s' % self.config_file)


        try:
            self.ansparams['mhz'] = self.config.get(mysection, 'mhz')
        
        except:
            raise Exception('Error: could not find mhz in configuration file %s' % self.config_file)

        try:
            self.ansparams['ptool'] = self.config.get(mysection, 'ptool')
        
        except:
            raise Exception('Error: could not find ptool in configuration file %s' % self.config_file)

        try:
            self.ansparams['l2cacheline'] = self.config.get(mysection, 'l2cacheline')
        
        except:
            raise Exception('Error: could not find l2cacheline in configuration file %s' % self.config_file)

        try:
            self.ansparams['plotfilename'] = self.config.get(mysection, 'plotfilename')
        
        except:
            raise Exception('Error: could not find plotfilename in configuration file %s' % self.config_file)







