#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime
from os import path


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static folder
    """

    local("mkdir -p versions")
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(time)
    local("tar -cvzf {} web_static".format(file))
    if path.exists(file):
        return file
    return None
