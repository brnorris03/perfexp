import ConfigParser

class GENParams:
    modparams = {'DEBUG': None, 'legend':None}

    def _processConfigFile(self):
        mysection = 'Models'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.modparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.modparams['legend'] = self.config.get(mysection, 'legend')
        
        except:
            raise Exception('Error: could not find legend in configuration file %s' % self.config_file)


class LogGPFTParams:

    modparams = {'DEBUG':None, 'tc':None, 'legend':None, 'N':None, 'L':None, 'o':None, 'g':None, 'G':None, 'm':None}

    def _processConfigFile(self):
        
        mysection = 'Models'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.modparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.modparams['legend'] = self.config.get(mysection, 'legend')
        
        except:
            raise Exception('Error: could not find legend in configuration file %s' % self.config_file)


        try:
            self.modparams['tc'] = self.config.get(mysection, 'tc')
        
        except:
            raise Exception('Error: could not find tc in configuration file %s' % self.config_file)

        try:
            self.modparams['N'] = self.config.get(mysection, 'N')
        
        except:
            raise Exception('Error: could not find N in configuration file %s' % self.config_file)

        try:
            self.modparams['L'] = self.config.get(mysection, 'L')
        
        except:
            raise Exception('Error: could not find L in configuration file %s' % self.config_file)

        try:
            self.modparams['o'] = self.config.get(mysection, 'o')
        
        except:
            raise Exception('Error: could not find o in configuration file %s' % self.config_file)

        try:
            self.modparams['g'] = self.config.get(mysection, 'g')
        
        except:
            raise Exception('Error: could not find g in configuration file %s' % self.config_file)

        try:
            self.modparams['G'] = self.config.get(mysection, 'G')
        
        except:
            raise Exception('Error: could not find G in configuration file %s' % self.config_file)

        try:
            self.modparams['m'] = self.config.get(mysection, 'm')
        
        except:
            raise Exception('Error: could not find m in configuration file %s' % self.config_file)

class FTParams:

    modparams = {'DEBUG':None, 'tc':None, 'legend':None, 'N':None, 'L':None, 'o':None, 'g':None, 'm':None}

    def _processConfigFile(self):
        
        mysection = 'Models'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.modparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.modparams['legend'] = self.config.get(mysection, 'legend')
        
        except:
            raise Exception('Error: could not find legend in configuration file %s' % self.config_file)


        try:
            self.modparams['tc'] = self.config.get(mysection, 'tc')
        
        except:
            raise Exception('Error: could not find tc in configuration file %s' % self.config_file)

        try:
            self.modparams['N'] = self.config.get(mysection, 'N')
        
        except:
            raise Exception('Error: could not find N in configuration file %s' % self.config_file)

        try:
            self.modparams['L'] = self.config.get(mysection, 'L')
        
        except:
            raise Exception('Error: could not find L in configuration file %s' % self.config_file)

        try:
            self.modparams['o'] = self.config.get(mysection, 'o')
        
        except:
            raise Exception('Error: could not find o in configuration file %s' % self.config_file)

        try:
            self.modparams['g'] = self.config.get(mysection, 'g')
        
        except:
            raise Exception('Error: could not find g in configuration file %s' % self.config_file)

        try:
            self.modparams['m'] = self.config.get(mysection, 'm')
        
        except:
            raise Exception('Error: could not find m in configuration file %s' % self.config_file)

class RAParams:

    modparams = {'DEBUG':None, 'rc':None, 'legend':None, 'lc':None,'numupdates':None}

    def _processConfigFile(self):
        
        mysection = 'Models'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.modparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.modparams['legend'] = self.config.get(mysection, 'legend')
        
        except:
            raise Exception('Error: could not find legend in configuration file %s' % self.config_file)

        try:
            self.modparams['rc'] = self.config.get(mysection, 'rc')
        
        except:
            raise Exception('Error: could not find rc in configuration file %s' % self.config_file)


        try:
            self.modparams['lc'] = self.config.get(mysection, 'lc')
        
        except:
            raise Exception('Error: could not find lc in configuration file %s' % self.config_file)

        try:
            self.modparams['numupdates'] = self.config.get(mysection, 'numupdates')
        
        except:
            raise Exception('Error: could not find numupdates in configuration file %s' % self.config_file)

class RARMAParams:

    modparams = {'DEBUG':None, 'tn':None, 'legend':None, 'tg':None, 'tu':None, 'tl':None, 'ta':None, 'm':None, 'tul':None}

    def _processConfigFile(self):
        
        mysection = 'Models'
        self.config = ConfigParser.ConfigParser()
        self.config_file = 'src/examples/params.txt'
        self.config.readfp(open(self.config_file))
        
        try:
            self.modparams['DEBUG'] = self.config.get('General', 'DEBUG')
        
        except:
            raise Exception('Error: could not find DEBUG in configuration file %s' % self.config_file)

        try:
            self.modparams['legend'] = self.config.get(mysection, 'legend')
        
        except:
            raise Exception('Error: could not find legend in configuration file %s' % self.config_file)


        try:
            self.modparams['tn'] = self.config.get(mysection, 'tn')
        
        except:
            raise Exception('Error: could not find tn in configuration file %s' % self.config_file)

        try:
            self.modparams['tg'] = self.config.get(mysection, 'tg')
        
        except:
            raise Exception('Error: could not find tg in configuration file %s' % self.config_file)

        try:
            self.modparams['tu'] = self.config.get(mysection, 'tu')
        
        except:
            raise Exception('Error: could not find tu in configuration file %s' % self.config_file)

        try:
            self.modparams['tl'] = self.config.get(mysection, 'tl')
        
        except:
            raise Exception('Error: could not find tl in configuration file %s' % self.config_file)

        try:
            self.modparams['ta'] = self.config.get(mysection, 'ta')
        
        except:
            raise Exception('Error: could not find ta in configuration file %s' % self.config_file)

        try:
            self.modparams['m'] = self.config.get(mysection, 'm')
        
        except:
            raise Exception('Error: could not find m in configuration file %s' % self.config_file)

        try:
            self.modparams['tul'] = self.config.get(mysection, 'tul')
        
        except:
            raise Exception('Error: could not find tul in configuration file %s' % self.config_file)














