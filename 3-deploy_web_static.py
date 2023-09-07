#!/usr/bin/python3
"""a Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy"""
from fabric.api import *
from datetime import datetime
import os
import shlex


env.user = "ubuntu"
env.hosts = ['54.144.249.223', '54.87.212.214']


def do_pack():
    """Generates a .tgz archive from the conten of web_static"""

    now_date = datetime.now()
    date_fmt = "%Y%m%d%H%M%S"
    c_file = 'versions/web_static_{}.tgz'.format(now_date.strftime(date_fmt))

    try:
        if not os.path.isdir("versions"):
            local("mkdir -p versions")
        print("Packing web_static to {}".format(c_file))
        local('tar -cvzf {} web_static'.format(c_file))
        print("web_static packed: {} -> {}Bytes".
              format(c_file, os.stat(c_file).st_size))
        return c_file
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the webserver"""

    if not os.path.isfile(archive_path):
        return False

    try:
        pathway = archive_path.replace('/', ' ')
        pathway = shlex.split(pathway)
        file_name = pathway[-1]

        file_ext = file_name.replace('.', ' ')
        file_ext = shlex.split(file_ext)
        f_name = file_ext[0]

        rel_path = '/data/web_static/releases/{}/'.format(f_name)
        tmp_path = '/tmp/{}'.format(file_name)

        put(archive_path, "/tmp/")
        run("rm -rf {}".format(rel_path))
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


def deploy():
    """Creates and distribute an archive to web server."""

    try:
        c_file = do_pack()
    except Exception:
        return False
    return do_deploy(c_file)
