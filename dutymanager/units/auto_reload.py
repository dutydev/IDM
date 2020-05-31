import os
import sys

from module.utils import logger

_startup_cwd = os.getcwd()


def restart():
    """
    Author: https://github.com/cherrypy/cherrypy/blob/0857fa81eb0ab647c7b59a019338bab057f7748b/cherrypy/process/wspbus.py#L305
    Этот метод работает только на OC Linux & MacOS, Windows отпадает.
    :return:
    """
    args = sys.argv[:]
    logger.debug("Restarting: %s" % " ".join(args))
    args.insert(0, sys.executable)
    if sys.platform == "win32":
        args = ['"%s"' % arg for arg in args]

    os.chdir(_startup_cwd)
    os.execv(sys.executable, args)