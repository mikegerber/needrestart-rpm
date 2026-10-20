import dnf
import os
import subprocess


class NeedRestart(dnf.Plugin):
    name = 'needrestart'
    need_check = False

    def __init__(self, base, cli):
        super(NeedRestart, self).__init__(base, cli)
        self.base = base
        self.cli = cli

    def resolved(self):
        tx = self.base.transaction
        if tx.install_set or tx.remove_set:
            self.need_check = True

    def transaction(self):
        if self.base.conf.assumeyes:
            os.environ['DEBIAN_FRONTEND'] = 'noninteractive'

        if self.need_check:
            try:
                subprocess.call(['needrestart'])
            except OSError:
                # this tool is being removed
                pass

