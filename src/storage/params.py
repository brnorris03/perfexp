import ConfigParser
import os

class DBParams:

    dbparams = {'DEBUG':None, 'datadir':None, 'appname':None, 'expname':None, 'trialname':None, 'cqosloaderdir':None, 'cqosloader':None, 'dbconfig':None}	

    def _processConfigFile(self):
        
        mysection = 'DataManager'
        self.config = ConfigParser.ConfigParser()
        self.config_file = os.environ.get("PERFEXPDIR") + '/src/examples/params/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.dbparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.dbparams['datadir'] = self.config.get(mysection, 'datadir')
        
        except:
            raise Exception('Error: could not find datadir in configuration file %s' % self.config_file)

        try:
            self.dbparams['appname'] = self.config.get(mysection, 'appname')
        
        except:
            raise Exception('Error: could not find appname in configuration file %s' % self.config_file)

        try:
            self.dbparams['expname'] = self.config.get(mysection, 'expname')
        
        except:
            raise Exception('Error: could not find expname in configuration file %s' % self.config_file)

        try:
            self.dbparams['trialname'] = self.config.get(mysection, 'trialname')
        
        except:
            raise Exception('Error: could not find trialname in configuration file %s' % self.config_file)

        try:
            self.dbparams['cqosloaderdir'] = self.config.get(mysection, 'cqosloaderdir')
        
        except:
            raise Exception('Error: could not find cqosloaderdir in configuration file %s' % self.config_file)


        try:
            self.dbparams['cqosloader'] = self.config.get(mysection, 'cqosloader')
        
        except:
            raise Exception('Error: could not find cqosloader in configuration file %s' % self.config_file)

        try:
            self.dbparams['dbconfig'] = self.config.get(mysection, 'dbconfig')
        
        except:
            raise Exception('Error: could not find dbconfig in configuration file %s' % self.config_file)







