from setuptools import setup

packageName = "pyPm"
projectName = "pyProjectManager"
initFile = "./%s/__init__.py" % packageName
version = None
with open(initFile) as fd:
    exec(fd.read())
    version = __version__

with open("README.md", encoding="utf-8") as fd:
    readmeData = fd.read()

with open("LICENSE") as fd:
    licenseData = fd.read()

setup(
    name=packageName,
    description="Python project manager",
    version=version,
    packages=[
        packageName,
    ],
    install_requires=[
        "Click"
    ],
    license="GNU GENERAL PUBLIC LICENSE",
    long_description_content_type='text/markdown',
    long_description=readmeData,
    author="Sunil Kumar Nerella",
    author_email="sunil.nerella39@gmail.com",
    data_files=[
        "./README.md",
        "./LICENSE"
    ],
    entry_points={
        'console_scripts': [
            'pyPm=pyPm.__main__:cli'
        ],
    },
)
