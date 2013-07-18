import random

import libvirt

import config
from interface import BaseScheduler
from allvmexception import SchedulerException


class ChanceScheduler(BaseScheduler):

    def schedule(self):
        try:
            return random.choice(config.LIBVIRT_URLS)
        except IndexError:
            raise SchedulerException('config.LIBVIRT_URLS is empty!')


class UtilisationScheduler(BaseScheduler):

    def schedule(self):
        try:
            if len(config.LIBVIRT_URLS) <= 0:
                raise SchedulerException('config.LIBVIRT_URLS is empty!')
        except AttributeError:
            raise SchedulerException('Not exist list '\
                                            'LIBVIRT_URLS in config.py')

        libvirt_url = ''
        memory_size = 0
        for host in config.LIBVIRT_URLS:
            url = 'qemu+ssh://{0}/system'.format(host)
            conn = libvirt.open(url)
            if memory_size < conn.getFreeMemory():
                memory_size = conn.getFreeMemory()
                libvirt_url = host

        return libvirt_url
