# -*- coding: UTF-8 -*-

import unittest
import os
import subprocess
import time
import datetime


class TestDhcpdUpdate(unittest.TestCase):

    DHCPD_UPDATE_DIR = '/etc/dhcp/dhcpd_update'

    def test_have_dhcpd_update_files(self):
        self.assertTrue(os.path.isdir(self.DHCPD_UPDATE_DIR))
        self.assertTrue(len(os.listdir(self.DHCPD_UPDATE_DIR)) > 0)


class TestCtiConfFile(unittest.TestCase):

    CTI_INI_FILE = '/etc/pf-xivo/web-interface/cti.ini'
    CTI_INI_CONTENT_RESULT = """\
; XIVO: FILE AUTOMATICALLY GENERATED BY THE XIVO CONFIGURATION SUBSYSTEM
[general]
datastorage = "postgresql://xivo:proformatique@localhost/xivo?encoding=utf8"

[queuelogger]
datastorage = "postgresql://asterisk:proformatique@localhost/asterisk?charset=utf8"

"""

    def test_cti_conf_generation(self):
        with open(self.CTI_INI_FILE) as fobj:
            cti_ini_content = fobj.read()
        self.assertEqual(cti_ini_content, self.CTI_INI_CONTENT_RESULT)


class TestAsteriskCommand(unittest.TestCase):

    def test_core_reload(self):
        retcode = subprocess.call(['asterisk', '-rx', 'core reload'])
        self.assertEqual(retcode, 0)


class TestAsteriskRestart(unittest.TestCase):

    WAIT_SECS = 10
    NB_TRIES = 15
    ASTERISK_PIDFILE = '/var/run/asterisk/asterisk.pid'
    CTI_PIDFILE = '/var/run/xivo-ctid.pid'
    DAEMON_LOGFILE = '/var/log/daemon.log'
    XIVO_RESTART_LINE = "start: /usr/bin/xivo-service"
    DATE_FORMAT = "%b %d %H:%M:%S"

    def test_asterisk_and_cti_restart(self):

        self._stop_asterisk()

        # Check that asterisk and CTI are not running
        self.assertFalse(
            self._is_process_running(self.ASTERISK_PIDFILE),
            "asterisk is still running after stopping service")

        self.assertFalse(
            self._is_process_running(self.CTI_PIDFILE),
            "ctid is still running after stopping asterisk")

        # Wait and check that asterisk is back up
        self._wait_service_restart(self.ASTERISK_PIDFILE, self.NB_TRIES)

        self.assertTrue(
            self._is_process_running(self.ASTERISK_PIDFILE),
            "asterisk did not restart after stopping service")

        # Wait and check that  CTI is back up
        self._wait_service_restart(self.CTI_PIDFILE, self.NB_TRIES)

        self.assertTrue(
            self._is_process_running(self.CTI_PIDFILE),
            "ctid did not restart after stopping service")

    def test_monit_restarts_xivo_services(self):
        min_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=self.WAIT_SECS * self.NB_TRIES)

        monit_restarted = False
        loglines = self._read_last_log_lines(self.DAEMON_LOGFILE, min_timestamp)
        for line in loglines:
            if self.XIVO_RESTART_LINE in line:
                monit_restarted = True

        self.assertTrue(monit_restarted, "monit did not restart xivo-services")

    def _wait_service_restart(self, pidfile, maxtries):

        nbtries = 0
        restarted = self._is_process_running(pidfile)
        while nbtries < maxtries and not restarted:
            time.sleep(self.WAIT_SECS)
            restarted = self._is_process_running(pidfile)
            nbtries += 1

        return restarted

    def _stop_asterisk(self):
        retcode = subprocess.call(['service', 'asterisk', 'stop'])
        self.assertEqual(retcode, 0)
        time.sleep(1)

    def _is_process_running(self, pidfile):

        if not os.path.exists(pidfile):
            return False

        pid = open(pidfile).read().strip()

        return os.path.exists("/proc/%s" % pid)

    def _read_last_log_lines(self, log_filepath, min_timestamp):

        current_year = datetime.datetime.now().year

        lines = []
        for line in open(log_filepath):
            datetext = line[0:15]

            timestamp = datetime.datetime.strptime(datetext, self.DATE_FORMAT)
            # Needed so that the timestamp has the right year
            timestamp = datetime.datetime(
                year=current_year,
                month=timestamp.month,
                day=timestamp.day,
                hour=timestamp.hour,
                minute=timestamp.minute,
                second=timestamp.second)

            if timestamp >= min_timestamp:
                lines.append(line)

        return lines
