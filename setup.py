from setuptools import setup

######################################################################################################
################ You May Remove All the Comments Once You Finish Modifying the Script ################
######################################################################################################

setup(
    '''
    This name will be used when people try to do pip install. And it is CASE SENSITIVE. 
    You should create an unique name. Search on pypi.org to see if the name is taken or not.
    '''
    name = 'StraPy', 
    
    '''
    The version number of your package consists of three integers "Major.Minor.Patch".
    Typically, when you fix a bug, that will lead to a patch release. (e.g. 0.1.1 --> 0.1.2)
    If you add a new feature to your package, that will lead to a minor release. (e.g. 0.1.0 --> 0.2.0)
    If a major change that will affect many users happened, you will want to make it as a major release (e.g. 0.1.0 --> 1.0.0)
    '''
    version = '0.1.0-alpha',
    
    '''
    This is the short description will show on the top of the webpage of your package on pypi.org
    '''
    description = 'A package for macroscopic transportation assignment.',
    
    '''
    This is the name of your main module file. No need to include the .py at the end.

    package_dir = {'':'StraPy'},
    
    '''
    If you have many modules included in your package, you want to use the following parameter instead of py_modules.
    '''
#     packages = ['osmnx',
#                 'pandas',
#                 'numpy'
#  ],
    
    '''
    Change the author name(s) and email(s) here.
    '''
    author = 'Aulia Rahman',
    author_email = 'rahmancs02@gmail.com',
    
    '''
    Leave the following as default. It will show the readme and changelog on the main page of your package.
    '''
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type = "text/markdown",
    
    '''
    The url to where your package is stored for public view. Normally, it will be the github url to the repository you just forked.
    '''
    url='https://github.com/Ultios/StraPy',
    
    '''
    Leave it as deafult.
    '''
    include_package_data=True,
    
    '''
    This is not a enssential part. It will not affect your package uploading process. 
    But it may affect the discoverability of your package on pypi.org
    Also, it serves as a meta description written by authors for users.
    Here is a full list of what you can put here:
    
    https://pypi.org/classifiers/
    
    '''
    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Tranportation',
        'Operating System :: OS Independent',
    ],
    
    
    '''
    This part specifies all the dependencies of your package. 
    "~=" means the users will need a minimum version number of the dependecies to run the package.
    If you specify all the dependencies here, you do not need to write a requirements.txt separately like many others do.
    '''
    install_requires = [
        'osmnx ~= 1.3.0',
        'pandas ~= 1.2.4',
    ],
    
    
    
    '''
    The keywords of your package. It will help users to find your package on pypi.org
    '''
    keywords = ['Traffic Assignment', 'Transportation Planning', 'Macroscopic Transportation Planning'],
    
)
