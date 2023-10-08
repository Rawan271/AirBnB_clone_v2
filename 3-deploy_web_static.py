#!/usr/bin/python3
""" Creates and distributes an archive to web servers,
using created function deploy and pack"""
from fabric.api import *
import os
from datetime import datetime
from fabric.decorators import runs_once

# do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ['34.232.69.7', '18.209.179.17']


@runs_once
def do_pack():
    """Pack all the contents in the web_static directory
    as a tar archive"""

    try:
        local("mkdir -p versions")
        time = datetime.now()
        date_string = '%Y%m%d%H%M%S'
        date = time.strftime(date_string)

        file_path = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(file_path))
        return file_path

    except Exception:
        return None


def deploy():
    """Pack and deploy all file """
    file_path = do_pack()
    if not file_path:
        return False

    run_cmd = do_deploy(file_path)
    return run_cmd


def do_deploy(archive_path):
    """Archive distributor"""
    try:
        try:
            if os.path.exists(archive_path):
                arc_tgz = archive_path.split("/")
                arg_save = arc_tgz[1]
                arc_tgz = arc_tgz[1].split('.')
                arc_tgz = arc_tgz[0]

                """Upload archive to the server"""
                put(archive_path, '/tmp')

                """Save folder paths in variables"""
                uncomp_fold = '/data/web_static/releases/{}'.format(arc_tgz)
                tmp_location = '/tmp/{}'.format(arg_save)

                """Run remote commands on the server"""
                run('mkdir -p {}'.format(uncomp_fold))
                run('tar -xvzf {} -C {}'.format(tmp_location, uncomp_fold))
                run('rm {}'.format(tmp_location))
                run('mv {}/web_static/* {}'.format(uncomp_fold, uncomp_fold))
                run('rm -rf {}/web_static'.format(uncomp_fold))
                run('rm -rf /data/web_static/current')
                run('ln -sf {} /data/web_static/current'.format(uncomp_fold))
                run('sudo service nginx restart')
                return True
            else:
                print('File does not exist')
                return False
        except Exception as err:
            print(err)
            return False
    except Exception:
        print('Error')
        return False
