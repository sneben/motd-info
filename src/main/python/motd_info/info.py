#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import os
import psutil
import datetime


class MotdInfo(object):
    """Class for gathering and displaying relevant system informations"""

    def __init__(self):
        self.users = None
        self.disks = {}
        self.mem_usage = None
        self.disk_usage = None

    def add_disks(self, disks):
        """Add a disk hash to the instanciated object"""
        self.disks = disks

    def set_memory_usage(self):
        """Gather memory informations and set the wished values in a hash"""
        # psutil >= 0.6.0
        if 'virtual_memory' in dir(psutil):
            mem_usage = psutil.virtual_memory()
        # psutil < 0.6.0
        else:
            mem_usage = psutil.phymem_usage()
        # The percent attribute seems to be broken, so calculate by myself
        amount = float(mem_usage.used-mem_usage.cached) / 1024 / 1024
        percent = float(mem_usage.used-mem_usage.cached) * 100 / mem_usage.total
        self.mem_usage = {
            'amount': '{0:.1f}M'.format(amount),
            'percent': percent
        }

    @staticmethod
    def dereference_device(device):
        """Delink devices if necessary"""
        if os.path.islink(device):
            device_link_source = os.readlink(device)
            if os.path.isabs(device_link_source):
                return device_link_source
            else:
                return os.path.abspath('{0}/{1}'.format(os.path.dirname(device),
                                                        device_link_source))
        else:
            return device

    def set_disk_usage(self):
        """Gather disk informations and set the wished values in a hash"""
        usage = {}
        partitions = psutil.disk_partitions()
        for disk in self.disks:
            for partition in partitions:
                if self.dereference_device(partition.device) == disk:
                    amount = int(psutil.disk_usage(partition.mountpoint).used)
                    percent = psutil.disk_usage(partition.mountpoint).percent
                    usage[disk] = {
                        'amount': self.get_human_readable_size(amount),
                        'percent': percent
                    }
        self.disk_usage = usage

    def set_users(self):
        """Gather informations of logged in users and store values in a hash"""
        # psutil < 2.0.0
        if 'get_users' in dir(psutil):
            users_set = psutil.get_users()
        # psutil >= 2.0.0
        else:
            users_set = psutil.users()
        users = []
        for user in users_set:
            time = datetime.datetime.fromtimestamp(
                int(user.started)).strftime('%Y-%m-%d %H:%M:%S')
            users.append({
                'name': user.name,
                'from': user.host,
                'time': time
            })
        self.users = users

    @staticmethod
    def get_human_readable_size(size):
        """Takes the size in byte and calculate to K-, M- or GByte format"""
        unit = ''
        if size > 1024:
            size = size/1024
            unit = 'K'
        if size > 1024:
            size = size/1024
            unit = 'M'
        if size > 1024:
            size = size/1024
            unit = 'G'
        return '{0:.1f}{1}'.format(size, unit)

    @staticmethod
    def draw_status_bar(name, amount, percent, barlen=80):
        """Draw a nice status bar for percental usage"""
        percent = percent / 100
        progress = ''
        filling_mode = False
        print('{0} ({1}):'.format(name, amount))
        for i in range(barlen):
            if i < int(barlen * percent):
                progress += '='
            else:
                if filling_mode:
                    progress += '.'
                else:
                    filling_mode = True
                    progress += '>.'
        print ("[%s] %.2f%%\n" % (progress, percent * 100))

    def print_disk_usage(self):
        """Print usage status bar for all current set disks"""
        self.set_disk_usage()
        for device, info in self.disk_usage.iteritems():
            self.draw_status_bar(device, info['amount'], info['percent'])

    def print_memory_usage(self):
        """Print a usage status for memory"""
        self.set_memory_usage()
        self.draw_status_bar('RAM',
                             self.mem_usage['amount'],
                             self.mem_usage['percent'])

    def print_active_users(self):
        """Print a small overview of currently logged in users"""
        self.set_users()
        print('{0:15}{1:23}{2}'.format('USERNAME', 'FROM', 'LOGIN@'))
        for user in self.users:
            format_string = '{0:15}{1:23}{2}'
            print(format_string.format(user['name'],
                                       user['from'],
                                       user['time']))
        print('')
