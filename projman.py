import subprocess
import os
import argparse
import sys
import traceback

class projman:
    """usage: newproj <branchname>"""
    conf_file = ".projman.conf"
   
    def __init__(self):
        try:
            execfile(self.conf_file)
        except: 
            self.error(self.conf_file + " file not found")
             
    def error(t, msg):
        print "ERROR: " +  msg
        sys.exit(1)
        
    def success(t, msg):
        print msg

    def su_check(self):
        if not os.getuid() == 0:
            self.error("sorry, you need to run this as root")

    def vhost_create(self, site):
       self.su_check()

       # add virtual host:
       config_handle = open(os.path.join(self.webserver_config_file,site + ".dev.conf"),"w")
       try:
           self.vhost_template = self.vhost_template.replace("SECURE", self.ssl_config)
       except:
           self.vhost_template = self.vhost_template.replace("SECURE", "")
      
       config = self.vhost_template.replace("HOSTNAME", site)
       config = config.replace("HOSTPATH",os.path.join(self.webserver_site_root, site + ".dev"))
       config_handle.write(config)
       config_handle.close()
       self.success('virtual host file created')

    def hostfile_add(self, site):
               
       # write out hosts file:
       hosts_handle = open(self.hosts_file, "r")
       hosts_data = hosts_handle.read()
       hosts_string = self.hosts_string.replace("SITE",site)
               
       if not hosts_string in hosts_data:
           hosts_handle.close()
           hosts_handle = open(self.hosts_file, "w")
           hosts_data += "\n" + hosts_string + "\n"
           hosts_handle.write(hosts_data)
       hosts_handle.close()
       self.success(self.hosts_file + ' updated')
       
    def git_clone(self, site):

        # parse args:
        parser = argparse.ArgumentParser(description="Add new dev site.", prog="newpro.py", epilog="Read head of file for more info.")
        parser.add_argument("--git_suffix", help="Git repo suffix", default=self.git_suffix)
        parser.add_argument("--git", help="Name git *-dev abbreviation, if different.", default=self.git_suffix)
        parser.add_argument("site", help="Name of the new dev site", default=site)
        parser.add_argument("--origin", help="Git Server", default=self.origin)
        parser.add_argument("--path", help="Remote repository path", default=self.remote_repo_path)
        parser.add_argument("-s", help="Set up SSL", default=False, action='store_true')

        # parse args and store filtered values:
        args = parser.parse_args()
        git_suffix = args.git_suffix
        if args.git == git_suffix:
            git = args.site + git_suffix
        else:
            git = args.git + git_suffix
        site = args.site.replace(".dev","") # idiot-proof
        origin = args.origin
        remote_repo_path = args.path

        try: 
            os.mkdir(os.path.join(self.webserver_site_root, site + self.vhost_suffix))
            os.system("chmod 777 " + os.path.join(self.webserver_site_root, site + self.vhost_suffix))
        except OSError: #directory already exists, why not ignore?
            pass

        try: 
            os.chdir(os.path.join(self.webserver_site_root, site + self.vhost_suffix))
            if args.git.lower() != "none":
                os.system("git clone "+ origin +":"+ remote_repo_path + git + " . ")
        except:
            self.error(str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + traceback.print_tb(sys.exc_info()[2]))

        self.success('repo has been cloned')

                
