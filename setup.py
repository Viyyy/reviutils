from setuptools import setup
    
with open('requirements.txt','r',encoding='utf-8') as f:
    packages = [l for l in f.read().splitlines() if not l.startswith('#') and l.strip()!='']

setup(
    name='reviutils',
    version='1.0.2',
    description='A common library frequently used on python',
    url='https://github.com/Viyyy/viutils',
    author='Re.VI',
    author_email='reviy-top@outlook.com',
    license='Apache License 2.0',
    packages=['reviutils.common','reviutils.noisepollution'],
    install_requires=packages,
    extras_require={
        'audio': ['librosa', 'soundfile','torch', 'torchaudio','pydub']
    },
    zip_safe=False
)
'''
# 打包命令
python setup.py sdist bdist_wheel 
# 上传命令
twine upload dist/* --verbose
'''