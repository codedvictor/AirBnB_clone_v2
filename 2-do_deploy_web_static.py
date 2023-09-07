#!/usr/bin/python3
"""a Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy"""
from fabric.api import *
import os
from datetime import datetime
import shlex


env.user = "ubuntu"
env.hosts = ['54.144.249.223', '54.87.212.214']


def do_deploy(archive_path):
    """distributes an archive to your web servers"""

    if not os.path.exists(archive_path):
        return False
    try:
        file_path = archive_path.replace('/', ' ')
        file_path = shlex.split(file_path)
        file_name = file_path[-1]

        file_ext = file_name.replace('.', ' ')
        file_ext = shlex.split(file_ext)
        f_name = file_ext[0]

        rel_path = '/data/web_static/releases/{}/'.format(f_name)
        tmp_path = '/tmp/{}'.format(file_name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(rel_path))
        run("tar -xzf {} -C {}".format(tmp_path, rel_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(rel_path, rel_path))
        run("rm -rf {}web_static".format(rel_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(rel_path))
        print("New version deployed")
        return True
    except Exception:
        return False
