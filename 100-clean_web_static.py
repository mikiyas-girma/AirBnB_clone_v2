#!/usr/bin/python3
"""
deletes out-of-date archives, using the function do_clean
"""
import os
from fabric.api import env, local, lcd, cd, run

env.hosts = ['54.175.89.74', '35.153.83.42']


def do_clean(number=0):
    """
    deletes unnecessary archives in the versions folder locally and
    in the /data/web_static/releases folder in my servers
    """
    print("Starting do_clean")

    number = 1 if int(number) == 0 else int(number)
    print("Number of archives to keep:", number)

    print("Local archives:")
    local_archives = sorted(os.listdir("versions"))
    print(local_archives)

    [local_archives.pop() for i in range(number)]
    print("Archives to delete locally:")
    print(local_archives)

    with lcd("versions"):
        print("Deleting local archives:")
        [local("rm ./{}".format(a)) for a in local_archives]

    with cd("/data/web_static/releases"):
        print("Server archives:")
        server_archives = run("ls -tr").split()
        print(server_archives)

        server_archives = [a for a in server_archives if "web_static_" in a]
        print("Filtered server archives:")
        print(server_archives)

        [server_archives.pop() for i in range(number)]
        print("Archives to delete on server:")
        print(server_archives)

        print("Deleting server archives:")
        [run("sudo rm -rf ./{}".format(a)) for a in server_archives]

    print("do_clean completed")
