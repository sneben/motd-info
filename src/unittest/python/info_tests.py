#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test suite for testing the functionality of the MotdInfo class"""

from unittest2 import TestCase
from mock import patch
from motd_info import MotdInfo


class BackupBaseTests(TestCase):
    def setUp(self):
        self.motd = MotdInfo()

    def test_should_calculate_memory_usage(self):
        self.motd.set_memory_usage()

    def test_should_calculate_disk_usage(self):
        self.motd.set_disk_usage()

    def test_should_set_logged_in_users(self):
        self.motd.set_users()

    def test_should_get_human_readable_values(self):
        self.motd.get_human_readable_size(4096)
        self.motd.get_human_readable_size(4194304)
        self.motd.get_human_readable_size(4294967296)

    @patch('__builtin__.print')
    def test_should_draw_bar(self, mock_print):
        self.motd.draw_status_bar('testname', 'testvalue', 75)

    @patch('__builtin__.print')
    def test_should_print_active_users(self, mock_print):
        self.motd.print_active_users()
