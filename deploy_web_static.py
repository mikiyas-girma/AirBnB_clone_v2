#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers,
using the function deploy"""
import importlib.util

module1 = './1-pack_web_static'
module2 = './2-do_deploy_web_static'

pack_web_static = importlib.import_module('1-pack_web_static', module1)
do_deploy_web_static = importlib.import_module('2-do_deploy_web_static',
                                               module2)

do_pack = pack_web_static.do_pack
do_deploy = do_deploy_web_static.do_deploy


def deploy():
    """
    Call the do_pack() function and store the path of the created archive
    Return False if no archive has been created
    Call the do_deploy(archive_path) function, using the new path of the
    new archive
    Return the return value of do_deploy
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path) and print("New version deployed!")
