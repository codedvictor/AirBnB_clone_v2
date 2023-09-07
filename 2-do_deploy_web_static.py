#!/usr/bin/python3

from fabric.api import *
import os
from datetime import datetime
import shlex


env.user = "ubuntu"
env.hosts = ['54.162.106.171', '54.90.38.102']


def do_deploy(archive_path):
    """distributes an archive to your web servers"""

    if not os.path.exists(archive_path):
        return False
    try:
        paths = archive_path.replace('/', ' ')
        paths = shlex.split(paths)
        file_name = paths[-1]

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
