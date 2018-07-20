import os
import subprocess
from subprocess import call
import shutil

if __name__ == '__main__':
    """
    Running `python setup.py` will generate a cryptoprice.zip file which can
    be uploaded to the AWS Lambda website and be used as a fully functioning
    lambda function.
    """

    # Place our resources into zip_folder
    print("Adding contents to zip folder")
    os.mkdir('zip_folder')
    call(['cp', 'cryptoprice.py', 'zip_folder/'])
    call(['cp', 'skill.py', 'zip_folder/'])
    call(['cp', '-rf', 'data/', 'zip_folder/data/'])
    FNULL = open(os.devnull, 'w')
    call(['pip', 'install', 'requests', '-t', 'zip_folder'], stdout=FNULL, stderr=subprocess.STDOUT)

    # Zip contents of zip_folder
    print("Zipping contents")
    shutil.make_archive('cryptoprice', 'zip', 'zip_folder')

    # Remove folders used to create zip
    print("Removing unneeded files")
    call(['rm', '-rf', 'zip_folder'])

    print("Build success")
