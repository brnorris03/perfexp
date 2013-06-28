#!/usr/bin/env python

import os,os.path,sys,glob,time,subprocess
import timer
from globals import Globals
from messages import *

have_hashlib = False
try:
    import hashlib
    have_hashlib = True
except ImportError:
    ### hashlib not present before 2.5, use md5
    import md5

try:
    from subprocess import Popen,PIPE,STDOUT
except ImportError:
    ### subprocess was not present before Python 2.4. Workaround if needed.
    print >> sys.stderr, 'subprocess not found (python too old?), trying popen2'
    import popen2
    PIPE=1
    STDOUT=1
    class Popen:
        def __init__(self,command,shell=True,
                stdout=PIPE,stderr=STDOUT):
                if (shell != True) or (stdout != PIPE) or (stderr != STDOUT):
                    raise RuntimeError,"Popen hack only compatible with certain inputs"
                self.popen4 = popen2.Popen4(command)
                self.stdout = self.popen4.fromchild

        def poll(self):
            self.returncode = self.popen4.poll()
            if self.returncode == -1:
                return None
            else:
                return self.returncode

start_time = -1.7724539
def create_tag(target):
    f = open("%s" % target[0],'w')
    f.write('%s (%f)\n' % (time.strftime("%Y-%m-%d %H:%M:%S"),time.time()))
    f.close()

# Set Attribute Mode    <ESC>[{attr1};...;{attrn}m
#     * Sets multiple display attribute settings. The following lists
#       standard attributes:

# 0    Reset all attributes
# 1    Bright
# 2    Dim
# 4    Underscore    
# 5    Blink
# 7    Reverse
# 8    Hidden

#     Foreground Colours
# 30    Black
# 31    Red
# 32    Green
# 33    Yellow
# 34    Blue
# 35    Magenta
# 36    Cyan
# 37    White

#     Background Colours
# 40    Black
# 41    Red
# 42    Green
# 43    Yellow
# 44    Blue
# 45    Magenta
# 46    Cyan
# 47    White

if sys.stdout.isatty():
    command_pre = "\x1B[01;34m"
    command_post = "\x1B[00m"
    time_pre = "\x1B[02;32m"
    time_post = "\x1B[00m"
    error_msg_pre = "\x1B[00;41;37m"
    error_msg_post = "\x1B[00m"
    error_pre = "\x1B[00;31m"
    error_post = "\x1B[00m"
else:
    command_pre = "*** perfexp command: "
    command_post = ""
    time_pre = "--- perfexp time: "
    time_post = ""
    error_msg_pre = "XXXXXXXXXXXXXX "
    error_msg_post = ""
    error_pre = ""
    error_post = ""

def command_message(description):
    info("%s[%s]%s"%(command_pre,description,command_post))
    
def throbbing_wait(pid):
    # Basic little throbber (hourglass, spinny, whatever)
    throbber = "-\\|/"
    sys.stdout.write(throbber[0])
    sys.stdout.flush()
    i = 1
    ret = os.waitpid(pid, os.WNOHANG)
    while ret == ( 0, 0 ):
       time.sleep(0.125)
       sys.stdout.write("\b" + throbber[i])
       sys.stdout.flush()
       i = (i + 1) % len(throbber)
       ret = os.waitpid(pid, os.WNOHANG)
    sys.stdout.write("\b")
    return ret[1]

def system_cmd(command_in, log_file=None):
    t0 = time.time()
    sys.stdout.write("%s%s%s "%(command_pre,command_in,command_post))
    sys.stdout.flush()
    Globals().logger.info(command_in)
    
    if log_file:
        command = "%s &> %s" % (command_in,log_file)
        if not os.path.isdir(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
    else:
        command = command_in        
    #info("Running cmd... " + command)
    #retval = os.system(command)
    #retval = os.spawnlp(os.P_WAIT, "sh", "sh", "-c", command)
    pid = os.spawnlp(os.P_NOWAIT, Globals().shell, Globals().shell, "-c", command)
    retval = throbbing_wait(pid)
    t1 = time.time()
    info('\b',end = ' ',logging=False)
    if log_file:
        f = open(log_file + ".time","w")
        f.write("%0.4g seconds\n" % (t1-t0))
        f.close()
    # Print wallclock time (in yellow) for this command
    sys.stdout.write(' %s%1.2fs%s\n'%(time_pre,t1-t0,time_post))
    return retval

def system_or_die(command_in, log_file=None, command_log_file=None,
                  log_stdout = None, raise_exception = False):
    t0 = time.time()
    if log_stdout == None:
        log_stdout = True
    output = ''
    print "%s%s%s"%(command_pre,command_in,command_post)
    dry_run = False
    if dry_run:
        return 0
    else:
        if command_log_file:
            if not os.path.isdir(os.path.dirname(command_log_file)):
                os.makedirs(os.path.dirname(command_log_file))
            f = open(command_log_file,"a")
            f.write("%s\n" % command_in)
            f.close()
        if log_file:
            if not os.path.isdir(os.path.dirname(log_file)):
                os.makedirs(os.path.dirname(log_file))
            log_file_file = open(log_file,"a")
        subproc = Popen(command_in,shell=True,
                        stdout=PIPE,stderr=STDOUT)
        while True:
            o = subproc.stdout.readline()
            output += o
            if o == '' and subproc.poll() != None: 
                break
            if log_stdout:
                sys.stdout.write(o)
            if log_file:
                log_file_file.write(o)
        if log_file:
            log_file_file.close()
            t1 = time.time()
            f = open(log_file + ".time","a")
            f.write("%0.4g seconds\n" % (t1-t0))
            f.close()
        if subproc.returncode!= 0:
            if raise_exception:
                raise RuntimeError, "%s failed" % command_in
            if log_file:
                print "%sperfexp failed command output (final 10 lines):%s" % \
                      (error_msg_pre,error_post)
                os.system('tail -n 10 %s' % log_file)
                print "%sperfexp failed command output end.%s" % \
                      (error_msg_pre,error_post)
                sys.stdout.write("%slog file is %s%s\n" % \
                                 (error_pre,log_file,error_post))
            timer.show_timer()
            #raise RuntimeError, 'Failed system command'
            send_error_email()
            sys.exit(1)
        return subproc.returncode, output

def get_stats(vals):
    # Given a list of values, return the mean, min, and max
    if not vals: return 0.0, 0.0, 0.0
    mean = 0.0
    min = vals[0]
    max = vals[0]
    sum = 0.0
    for v in vals: 
        sum += v
        if v > max: max = v
        if v < min: min = v
    mean = sum / float(len(vals))
    return mean, min, max
        
    
def send_error_email():
    if Globals().email:
        import root

        siteinfo = open('siteinfo.txt', 'w')
        siteinfo.write(os.popen('echo "# uname -a"; uname -a 2>&1; echo "# env"; env 2>&1;').read())
        siteinfo.close()
        try: os.system('cp siteinfo.txt ' + root.local_root.vars["log_dir"])
        except: pass

        archive = generate_error_archive(root.local_root.vars['base_dir'], 
                                         [root.local_root.vars["log_dir"], 
                                          root.local_root.vars["config_dir"]])

        info("An archive of the logs has been saved to " + archive + \
             ". Please email this file to the CCA tools developers at " + \
             Globals().email)        
        try:
            send_email(archive, [Globals().email])
        except: 
            pass
    return

def check_shell():
    realshellpath = os.path.realpath(Globals().shell)
    if realshellpath == '/bin/dash':
        warning = False
        if os.path.exists('/bin/bash'):
            warning = True 
            Globals().shell = '/bin/bash'
        elif os.path.exists('/bin/ksh'):
            warning = True
            Globals().shell = '/bin/ksh'
        else:
            err('default shell is /bin/dash, which will likely cause many problems downstream. Giving up.')
        warn('default shell is /bin/dash. perfexp will use ' + Globals().shell + ', but you will likely encounter problems in other tools.')
    
 
def generate_error_archive(rootdir, dirs):
    from configuration import check_bin
    d = os.getcwd()
    save = os.path.join(os.environ["HOME"], "perfexp-logs.tar")

    if rootdir: os.chdir(rootdir)
    if os.path.exists(save): os.unlink(save)
    for dir in dirs:
        if dir.startswith(rootdir): d = dir[len(rootdir)+1:]
        os.system("tar -upf " + save + ' ' + d)
    logpath = os.path.join(rootdir,Globals().logfile)
    if os.path.exists(logpath): os.system("tar -upf " + save + ' ' + logpath)
    zip = check_bin('bzip2')
    suffix = '.bz2'
    if not zip: 
        zip = check_bin('tar')
        suffix = '.gz'
    if zip:
        if os.path.exists(save + suffix): os.unlink(save + suffix)
        os.system(zip + ' ' + save)
        save += suffix
    return save

def send_email(file, to, server="localhost"):
    try:
        import smtplib
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEBase import MIMEBase
        from email.MIMEText import MIMEText
        from email.Utils import COMMASPACE, formatdate
        from email import Encoders
    except:
        return
    try:
        smtp = smtplib.SMTP(server)
    except:
        return
    response = raw_input('Would you like to try to send the email with the log now (y/n) ? [n] ')
    if not str(response).lower() in ['yes', 'y']:
        return 
    name = raw_input('Please enter your name: ')
    emailaddr = raw_input('Please enter your email address: ')
    fro = name + '<' + emailaddr + '>'

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'error log for perfexp'

    text = 'PerfExp build log: ' + msg['Date']
    msg.attach( MIMEText(text) )

    # Encode file and atach
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(file,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"'
                   % os.path.basename(file))
    msg.attach(part)


    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()
    return
    
def abs_rel_dir(base_dir, dir):
    if os.path.isabs(dir):
        retval = dir
    else:
        retval = os.path.join(base_dir,dir)
    return retval

def env_path_add(var, item, delimiter=':'):
    if os.environ.has_key(var):
        os.environ[var] = item + delimiter + os.environ[var]
    else:
        os.environ[var] = item

"""
Re-implementation of md5sum in python, vername is the base filename without the suffix.
"""
def get_md5sum_file(filename):
    """Return the hex digest of a file without loading it all into memory"""
    fh = open(filename)
    if ( have_hashlib ):
        digest = hashlib.md5()
    else:
        digest = md5.new()

    while 1:
        buf = fh.read(4096)
        if buf == "":
            break
        digest.update(buf)
    fh.close()
    hexdigest = digest.hexdigest()
    return hexdigest

def listify(x):
    if type(x) == type([]) or type(x) == type(()):
        return x
    else:
        return [x]

#-------------------------------------------------------------------------------
def grep(strings, pattern):
    """
    Provide grep-like functionality for returning strings that match a pattern.
    The first argument can be either a list of strings or a string (with or 
    without multiple lines through '\n' characters).
    
    Usage
    -----
    Please see the regular expression syntax for the re module located here:
    http://docs.python.org/lib/re-syntax.html
    
    matches = grep("This is a test string", "^This")
    => ["This is a test string"]
    
    matches = grep("alpha\nbeta\ncappa\ngamma\nzappa", ".*appa$")
    => ["cappa", "zappa"]
    
    @param strings: A string or list of strings
    @type strings: str or list
    @param pattern: A pattern to match
    @type pattern: str
    @return: A list of all matched strings
    """
    import re
    matches = []
    
    # If strings is a string, split it into separate lines
    if type(strings) == str:
        strings = strings.split("\n")
    
    # For every line try and match it agains the pattern, adding it to matches
    # if we get a positive match
    for line in strings:
        if re.compile(pattern).match(line):
            matches.append(line)
    
    return matches


class Changed_files:
    def __init__(self, path):
        self.old = {}
        self.new = {}
        self.new_files = []
        self.modified_files = []
        self.path = path
        os.path.walk(self.path,self.walker,self.old)
        
    def walker(self, arg, dirname, names):
        for name in names:
            fullpath = os.path.join(dirname,name)
            if not os.path.isdir(fullpath):
                try:
                    arg[fullpath] = os.path.getmtime(fullpath)
                except OSError:
                    arg[fullpath] = None
    def end(self):
        os.path.walk(self.path,self.walker,self.new)
        for key in self.new.keys():
            if self.old.has_key(key):
                if self.old[key] != self.new[key]:
                    self.modified_files.append(key)
            else:
                self.new_files.append(key)

    def _dump(self,filename,pathlists):
        if not global_runtime_options.dry_run:
            f = open(filename,"w")
            for pathlist in pathlists:
                for path in pathlist:
                    f.write("%s\n" % path)
            f.close()
        
    def dump_new(self, filename):
        self._dump(filename,[self.new_files])
        
    def dump_modified(self, filename):
        self._dump(filename,[self.modified_files])

    def dump_all(self, filename):
        self._dump(filename,[self.new_files,self.modified_files])

