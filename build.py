#!/usr/bin/python2.7
# Roman Grekov
from optparse import OptionParser
import subprocess
import traceback
import os
import re
import shutil
import fcntl
import sys

parser = OptionParser();

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="Print bash stdout")

parser.add_option("-u", "--update", dest="update", action="store_true",
                  help="This flag update: configs, scripts, addons")

parser.add_option("-g", "--upgrade", dest="upgrade", action="append", type="string",
                  default=[], help="distro, addons")

parser.add_option("-b", "--build", dest="build", action="append", type="string",
                  default=[], help="openhab, mosquitto, mysql")

parser.add_option("-e", "--export", dest="export", action="append", type="string",
                  default=[], help="openhab, mosquitto, mysql")

parser.add_option("-i", "--import", dest="_import", action="append", type="string",
                  default=[], help="openhab, mosquitto, mysql")

parser.add_option("-r", "--run", dest="run", action="append", type="string",
                  default=[], help="openhab, mysql, mosquitto")

(options, args) = parser.parse_args()


def perform_bash(action):
    print action
    process = ProcessIterator(action)
    stdout_store = ""
    for stdout in process:
        if stdout:
            stdout_store += stdout
            if options.verbose:
                sys.stdout.write(stdout)
    retcode = process.get_retcode()
    if retcode:
        raise RuntimeError(process.get_stderr())
    return retcode, stdout_store, process.get_stderr()

class ProcessIterator():
    def __init__(self, action):
        self.pipe = subprocess.Popen(action, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=True)
        fl=fcntl.fcntl (self.pipe.stdout, fcntl.F_GETFL) # get flags for file desriptor
        fcntl.fcntl (self.pipe.stdout, fcntl.F_SETFL, fl|os.O_NONBLOCK) # set nonblocking on read

    def __iter__(self):
        return self

    def next(self):
        if self.pipe.poll() is None:
            try:
                return self.pipe.stdout.read()
            except:
                return ""
        raise StopIteration

    def get_retcode(self):
        return self.pipe.returncode

    def get_stderr(self):
        return self.pipe.stderr.read()

def exception_handler(description):
    def wrapper(f):
        def run(*args, **kwargs):
            try:
                print description
                res = f(*args, **kwargs)
                print "OK"
                return res
            except Exception:
                print str(traceback.format_exc())
        return run
    return wrapper

@exception_handler("Updating openhab configs")
def update_openhab_configs(configurations, distro):
    distro_configs = os.path.join(distro, "configurations")
    action = "rm -rf %s/*" % distro_configs
    perform_bash(action)
    action = "cp -r %s/* %s/" % (configurations, distro_configs)
    perform_bash(action)

@exception_handler("Updating openhab addons")
def update_openhab_addons(addons, distro):
    distro_addons = os.path.join(distro, "addons")
    action = "rm -rf %s/*" % distro_addons
    perform_bash(action)
    action = "cp -r %s/* %s/" % (addons, distro_addons)
    perform_bash(action)

@exception_handler("Updating openhab scripts")
def update_openhab_scripts(configs, distro):
    debug_script = os.path.join(configs, "start_debug.sh")
    action = "cp -r %s %s" % (debug_script, distro)
    perform_bash(action)

@exception_handler("Updating openhab distro")
def update_openhab_distro(openhab_distro, link):
    action = "rm -rf *runtime.zip"
    perform_bash(action)
    action = "rm -rf %s" % openhab_distro
    perform_bash(action)
    action = "wget %s" % link
    perform_bash(action)
    action = "unzip *runtime.zip -d %s" % openhab_distro
    perform_bash(action)

@exception_handler("Updating openhab addons")
def update_openhab_distro_addons(my_addons, openhab_addons, openhab_addons_link, needed):
    action = "rm -rf *addons.zip"
    perform_bash(action)
    action = "rm -rf %s" % openhab_addons
    perform_bash(action)
    action = "mkdir -p %s" % openhab_addons
    perform_bash(action)
    action = "wget %s" % openhab_addons_link
    perform_bash(action)
    action = "unzip *addons.zip -d %s" % openhab_addons
    perform_bash(action)
    for addon in os.listdir(openhab_addons):
        full_path = os.path.join(openhab_addons, addon)
        remove = True
        if os.path.isfile(full_path):
            for mask in needed:
                if re.findall(mask, addon):
                    for my_addon in os.listdir(my_addons):
                        if re.findall(mask, my_addon):
                            os.remove(full_path)
                            shutil.copy(os.path.join(my_addons, my_addon),
                                        openahb_addons)
                            break

                    remove = False
                    break
            if remove:
                os.remove(full_path)

@exception_handler("Build openhab")
def build_openhab(full_imaage_name):
    action = "cd openhab && sudo docker build --no-cache -t %s ." % full_imaage_name
    perform_bash(action)

@exception_handler("Build mosquitto")
def build_mosquitto(full_imaage_name):
    action = "cd mosquitto && sudo docker build --no-cache -t %s ." % full_imaage_name
    perform_bash(action)

@exception_handler("Build mysql")
def build_mysql(full_imaage_name):
    action = "cd mysql && sudo docker build --no-cache -t %s ." % full_imaage_name
    perform_bash(action)

@exception_handler("Run openhab")
def run_openhab(full_imaage_name):
    action = "sudo docker run -d --name openhab --link mysql:mysql --link mosquitto:mosquitto -m 400m -p 443:8443 -p 8080:8080 %s" % full_imaage_name
    perform_bash(action)

@exception_handler("Run mosquitto")
def run_mosquitto(full_imaage_name):
    action = "sudo docker run --name mosquitto -m 100m -p 1883:1883 %s" % full_imaage_name
    perform_bash(action)

@exception_handler("Run mysql")
def run_mysql(full_imaage_name):
    action = "sudo docker run --name mysql -m 100m -p 3306:3306 %s" % full_imaage_name
    perform_bash(action)

@exception_handler("Export image")
def export(full_imaage_name, saved_image, path):
    action = "sudo docker save -o %s %s" % (os.path.join(path, saved_image),
                                            full_imaage_name)
    perform_bash(action)

@exception_handler("Import image")
def _import(saved_image, path):
    action = "sudo docker load -i %s" % os.path.join(path, saved_image)
    perform_bash(action)

def main():
    configs = "openhab/config"
    my_addons = os.path.join(configs, "my_addons")
    openhab_configs = os.path.join(configs, "openhab")
    openhab_configuration = os.path.join(openhab_configs, "configurations")
    openhab_addons = os.path.join(openhab_configs, "addons")
    openhab_distro = "openhab/openhab"

    images_path = "images"

    repo = "roman1grekov"
    openhab_image_name = "openhab"
    openhab_image_version = "v2.1"
    full_openhab_image_name = "%s/%s:%s" %(repo, openhab_image_name,
                                           openhab_image_version)
    openhab_saved_image = "%s_%s_%s" % (repo, openhab_image_name,
                                        openhab_image_version)

    mosquitto_image_name = "mosquitto"
    mosquitto_image_version = "v0.1"
    full_mosquitto_image_name="%s/%s:%s" %(repo, mosquitto_image_name,
                                         mosquitto_image_version)
    mosquitto_saved_image = "%s_%s_%s" % (repo, mosquitto_image_name,
                                          mosquitto_image_version)

    mysql_image_name = "mysql"
    mysql_image_version = "v0.1"
    full_mysql_image_name="%s/%s:%s" %(repo, mysql_image_name,
                                           mysql_image_version)
    mysql_saved_image = "%s_%s_%s" % (repo, mysql_image_name,
                                      mysql_image_version)

    openhab_distro_link = "https://github.com/openhab/openhab/releases/download/v1.6.2/distribution-1.6.2-runtime.zip"
    openhab_addons_link = "https://github.com/openhab/openhab/releases/download/v1.6.2/distribution-1.6.2-addons.zip "

    needed_addons = ["org.openhab.binding.http", "org.openhab.binding.mqtt-",
                     "org.openhab.binding.ntp", "org.openhab.persistence.mysql"]

    for option in options.upgrade:
        if option == "distro":
            update_openhab_distro(openhab_distro, openhab_distro_link)
        if option == "addons":
            update_openhab_distro_addons(my_addons, openhab_addons,
                                         openhab_addons_link, needed_addons)
    if options.update:
        update_openhab_configs(openhab_configuration, openhab_distro)
        update_openhab_addons(openhab_addons, openhab_distro)
        update_openhab_scripts(openhab_configs, openhab_distro)

    for option in options.build:
        if option == "openhab":
            build_openhab(full_openhab_image_name)
        if option == "mosquitto":
            build_mosquitto(full_mosquitto_image_name)
        if option == "mysql":
            build_mysql(full_mysql_image_name)

    for option in options.run:
        if option == "openhab":
            run_openhab(full_openhab_image_name)
        if option == "mosquitto":
            run_mosquitto(full_mosquitto_image_name)
        if option == "mysql":
            run_mysql(full_mysql_image_name)

    for option in options.export:
        if option == "openhab":
            export(full_openhab_image_name, openhab_saved_image, images_path)
        if option == "mosquitto":
            export(full_mosquitto_image_name, mosquitto_saved_image, images_path)
        if option == "mysql":
            export(full_mysql_image_name, mysql_saved_image, images_path)

    for option in options._import:
        if option == "openhab":
            _import(openhab_saved_image, images_path)
        if option == "mosquitto":
            _import(mosquitto_saved_image, images_path)
        if option == "mysql":
            _import(mysql_saved_image, images_path)

if __name__ == '__main__':
    main()


