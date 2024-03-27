'''
# 打包命令
python setup.py sdist bdist_wheel
# 上传命令
twine upload dist/* --verbose
'''

from setuptools import setup
    
with open('requirements.txt','r',encoding='utf-8') as f:
    packages = [l for l in f.read().splitlines() if not l.startswith('#') and l.strip()!='']

with open('README.md','r',encoding='utf-8') as f:
    long_description = f.read()
    

import os
import shutil

# 递归删除每个子文件夹的__pycache__
def del_pycache(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))
            else:
                del_pycache(os.path.join(root, dir))

del_pycache('reviutils') # 删除reviutils下的每个子文件夹的__pycache__文件夹

setup(
    name='reviutils',
    version='1.3.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='A common library frequently used on python',
    url='https://github.com/Viyyy/viutils',
    author='Re.VI',
    author_email='reviy-top@outlook.com',
    license='Apache License 2.0',
    packages=['reviutils.common','reviutils.noisepollution','reviutils.audio','reviutils.api'],
    install_requires=packages,
    extras_require={
        'audio': ['librosa', 'soundfile','torch', 'torchaudio','pydub','starlette']
    },
    zip_safe=False
)


