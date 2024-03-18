import os, shutil

# 删除setup.py文件构建的build, dist, viutils.egg-info文件夹

if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('reviutils.egg-info'):
    shutil.rmtree('reviutils.egg-info')