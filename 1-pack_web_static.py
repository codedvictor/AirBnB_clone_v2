#!/usr/bin/python3
"""a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack."""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generate a .tgz archive from the content of
    web_satic folder"""
    try:
        if not os.path.exists('versions'):
            local('mkdir versions')
        date = datetime.now()
        fmt = "%Y%m%d%H%M%S"
        path = 'versions/web_static_{}.tgz'.format(date.strftime(fmt))
        local('tar -cvzf {} web_static'.format(path))
        return path
    except Exception:
        return None
