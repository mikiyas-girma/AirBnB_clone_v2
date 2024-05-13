#!/usr/bin/python3
"""
script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers
"""
from fabric.api import env, put, run

env.hosts = ['54.175.89.74', '35.153.83.42']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Upload the archive to the /tmp/ directory of the web server
    Uncompress the archive to the folder /data/web_static/releases/\
        <archive filename without extension> on the web server
    Delete the archive from the web server
    Delete the symbolic link /data/web_static/current from the web server
    Create a new the symbolic link /data/web_static/current on the web server,
    linked to the new version of your code (/data/web_static/releases/<archive
    filename without extension>)
    """
    try:
        file = archive_path.split('/')[-1]
        name = file.split('.')[0]

        put(local_path=archive_path,
            remote_path='/tmp/{}'.format(file))
        run('mkdir -p /data/web_static/releases/{}/'.format(name))
        run('tar -xzf /tmp/{} -C \
            /data/web_static/releases/{}/'.format(file, name))
        run('rm /tmp/{}'.format(file))
        run('rm /data/web_static/current')
        run('ln -sf /data/web_static/releases/{}/ \
            /data/web_static/current'.format(name))
        return True
    except:
        return False
