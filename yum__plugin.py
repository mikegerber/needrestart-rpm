# -*- coding: utf-8 -*-
from yum.plugins import TYPE_CORE
import os
import sys
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


requires_api_version = '2.3'
plugin_type = (TYPE_CORE)

check_needed = False
assumeyes = False

def posttrans_hook(conduit):
    global check_needed, assumeyes

    check_needed = True

    opts, args = conduit.getCmdLine()
    if not opts:
      # if not interractive, like when called by yum-cron
      assumeyes = True
    else:
      assumeyes = opts.assumeyes

# acting in posttrans_hook is too early, we need to be sure the RPMDB is closed to avoid things like:
# « Rpmdb changed underneath us » followed by failure to open the database on the next YUM call
def close_hook(conduit):
    global check_needed, assumeyes

    if assumeyes:
        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'

    if not check_needed:
        return
    try:
        subprocess.call(['needrestart'])
    except OSError:
        # this tool is being removed
        pass
    except BaseException as e:
        print "Error running needrestart: {}".format(str(e))

