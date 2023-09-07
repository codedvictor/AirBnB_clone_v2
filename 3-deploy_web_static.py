#!/usr/bin/python3
from fabric.api import *
from datetime import datetime
import os
import shlex


env.user = "ubuntu"
env.hosts = ['54.162.106.171', '54.90.38.102']


def do_pack():
    """Generates a .tgz archive from the conten of web_static"""

    dt = datetime.now()
    fmt = "%Y%m%d%H%M%S"
    fil = 'versions/web_static_{}.tgz'.format(dt.strftime(fmt))

    try:
        if not os.path.isdir("versions"):
            local("mkdir -p versions")
        print("Packing web_static to {}".format(fil))
        local('tar -cvzf {} web_static'.format(fil))
        print("web_static packed: {} -> {}Bytes".
              format(fil, os.stat(fil).st_size))
        return fil
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the webserver"""

    if not os.path.isfile(archive_path):
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
        fil = do_pack()
    except Exception:
        return False
    return do_deploy(fil)
