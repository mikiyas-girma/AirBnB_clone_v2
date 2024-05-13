#!/usr/bin/python3
"""
full deployment of the web_static content
"""
from fabric.api import local, env, put, run
from datetime import datetime
from os import path
from os import getenv

env.hosts = ['54.175.89.74', '35.153.83.42']
env.user = 'ubuntu'
env.key_filename = getenv('PRIVATE_KEY_PATH')


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
    if not path.exists(archive_path):
        print("Archive file not found:", archive_path)
        return False
    filename = archive_path.split('/')[-1]
    foldername = filename.split('.')[0]

    print("Uploading archive...")
    if put(archive_path, "/tmp/{}".format(filename)).failed:
        print("Failed to upload archive to server")
        return False

    print("Removing old release directory...")
    if run("rm -rf /data/web_static/releases/{}/".
            format(foldername)).failed:
        print("Failed to remove old release directory")
        return False

    print("Creating new release directory...")
    if run("mkdir -p /data/web_static/releases/{}/".
            format(foldername)).failed:
        print("Failed to create new release directory")
        return False

    print("Extracting archive...")
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(filename, foldername)).failed:
        print("Failed to extract archive")
        return False

    print("Removing archive from server...")
    if run("rm /tmp/{}".format(filename)).failed:
        print("Failed to remove archive from server")
        return False

    print("Moving files to correct location...")
    if run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".
            format(foldername, foldername)).failed:
        print("Failed to move files to correct location")
        return False

    print("Removing old web_static directory...")
    if run("rm -rf /data/web_static/releases/{}/web_static".
            format(foldername)).failed:
        print("Failed to remove old web_static directory")
        return False

    print("Removing old current symlink...")
    if run("rm -f /data/web_static/current").failed:
        print("Failed to remove old current symlink")
        return False

    print("Creating new current symlink...")
    if run("ln -sf /data/web_static/releases/{}/ /data/web_static/current".
            format(foldername)).failed:
        print("Failed to create new current symlink")
        return False

    print("Deployment successful")
    return True


def deploy():
    """
    creates and distribute an archive to a web server
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
