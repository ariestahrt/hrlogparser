from setuptools import setup

setup(name='hrlogparser',
      version='0.0.1',
      description='Human-readable log parser',
      long_description='Automatic log parser for text classification',
      keywords='log parser, log forensic',
      url='https://github.com/ariestahrt/hrlogparser',
      author='I Kadek Agus Ariesta Putra, Riki Mi\'roj Achmad',
      author_email='ikadekagusariestaputra@gmail.com',
      license='Apache',
      packages=['hrlogparser'],
      entry_points = {
          'console_scripts': [
                'hrlogparser = hrlogparser.__main__:main'
          ]
      },
      install_requires=[
          'pandas',
          'logparser3'
      ],
    zip_safe=False,
    include_package_data=True,
)