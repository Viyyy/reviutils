"""
# 打包命令
python setup.py sdist bdist_wheel
# 上传命令
twine upload dist/* --verbose
"""

import os, shutil
from setuptools import setup


name = "reviutils"
version = "1.4.2"
packages = [
    "reviutils.common",
    "reviutils.noisepollution",
    "reviutils.audio",
    "reviutils.api",
    "reviutils.api.amap",
    "reviutils.gis",
    "reviutils.omap",
    "reviutils.omap.samples",
    "reviutils.omap.constants",
]


def del_setuptools_pycache():
    # 删除setup.py文件构建的build, dist, viutils.egg-info文件夹
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("reviutils.egg-info"):
        shutil.rmtree("reviutils.egg-info")


def del_pycache(path):
    # 递归删除每个子文件夹的__pycache__
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))
            else:
                del_pycache(os.path.join(root, dir))


def main():
    del_setuptools_pycache()
    with open("requirements.txt", "r", encoding="utf-8") as f:
        install_requires = [
            l
            for l in f.read().splitlines()
            if not l.startswith("#") and l.strip() != ""
        ]

    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

    del_pycache(name)  # 删除reviutils下的每个子文件夹的__pycache__文件夹

    setup(
        name=name,
        version=version,
        long_description=long_description,
        long_description_content_type="text/markdown",
        description="A common library frequently used on python",
        url="https://github.com/Viyyy/viutils",
        author="Re.VI",
        author_email="reviy-top@outlook.com",
        license="Apache License 2.0",
        packages=packages,
        install_requires=install_requires,
        extras_require={
            "audio": [
                "librosa",
                "soundfile",
                "torch",
                "torchaudio",
                "pydub",
                "starlette",
            ]
        },
        zip_safe=False,
    )

if __name__=="__main__":
    main()
    print("打包成功！")