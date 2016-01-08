# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='py_event_publisher',
    version='0.1',
    description=u'Módulo de Eventos',
    author='Innvent',
    author_email='desenvolvimentobrmed@innvent.com.br',
    url='https://github.com/innvent/py-event-publisher',
    packages=find_packages(),
    test_suite='tests',
    include_package_data=True,
    install_requires=[
        "py-notify==0.3.2",
    ],
    dependency_links=[
        "git+ssh://git@github.com/berinhard/py-notify.git@0.3.2#egg=py-notify-0.3.2",
    ],
)
