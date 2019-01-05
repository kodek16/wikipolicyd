import setuptools

setuptools.setup(
    name='wikipolicyd',
    version='0.1',
    author='Pavel Senchanka',
    author_email='pavel.senchanka@gmail.com',
    description='Simple daemon for controlling WikiLink traffic policy',
    url='https://github.com/kodek16/wikipolicyd',
    license='MIT',

    packages=setuptools.find_packages(),

    install_requires=[
        'requests~=2.19.0',
        'toml~=0.10.0',
    ],

    entry_points={
        'console_scripts': [
            'wikipolicyd = wikipolicyd.__main__:main'
        ],
    },
)
