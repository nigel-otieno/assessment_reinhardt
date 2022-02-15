from setuptools import setup

setup(
    name="reinhardt",
    version="0.1a",
    author_email='devhelp@cce.ou.edu',
    description='A collection of Django tools created for ease of use and rapid development.',
    author='University of Oklahoma - College of Continuing Education - IT',
    license='BSD',
    install_requires=[
        "django-currentuser",
        "arrow",
        "openpyxl",
    ],
    classifiers=[
        'Development Status :: 0.1a',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    url='https://github.com/cceit/django-dx',
    packages=['reinhardt'],
    include_package_data=True,
    package_data={
        'reinhardt': [
            '*.py',
            'forms/*.py',
            'models/*.py',
            'utils/*.py',
            'views/*.py',
            'templates/*.html'
        ],
    },
    zip_safe=False,
)
