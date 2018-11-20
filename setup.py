import os


def main():
    from setuptools import setup, find_packages

    # from nipype setup.py file
    ldict = locals()
    curr_path = os.path.dirname(__file__)
    ver_file = os.path.join(curr_path, 'urial', 'info.py')
    with open(ver_file) as infofile:
        exec(infofile.read(), globals(), ldict)

    setup(
        name=ldict['NAME'],
        version=ldict['VERSION'],
        description=ldict['DESCRIPTION'],
        long_description=ldict['LONG_DESCRIPTION'],
        maintainer=ldict['MAINTAINER'],
        maintainer_email=ldict['EMAIL'],
        url=ldict['URL'],
        download_url=ldict['DOWNLOAD_URL'],
        install_requires=ldict['INSTALL_REQUIRES'],
        packages=find_packages(),
        package_data=ldict['PACKAGE_DATA'],
        license=ldict['LICENSE'],
    )


if __name__ == '__main__':
    main()
