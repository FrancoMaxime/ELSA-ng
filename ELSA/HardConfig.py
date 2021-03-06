# -*- coding: utf-8 -*-
import ConfigParser
import socket
import traceback
import os
import codecs
import sys

HARDdirectory = os.path.normpath('~/akuino/hardware')

def get_config_file_path(config_file, hostname):
    if config_file is not None:
        return os.path.normpath(config_file)
    else:
        # Test if hostname is correctly initialized
        if not hostname.startswith(u'akuino'):
            print(hostname+": hostname should begin with akuino")
        return os.path.expanduser(os.path.join(HARDdirectory,
                                               hostname+'.ini'))

class HardConfig():
    config = None
    idDefinitions = {}
    hostname = "UNKNOWN"
    RUNdirectory = "/run/akuino"
    model = '3'
    i2c_bus = 1
    spi_channel = 0
    pcb = None
    ela = None
    ela_bauds = 9600
    ela_reset = '[9C5E01]'
    bluetooth = None
    wifi = None
    owfs = None
    oled = None
    oled_address = 0x3C
    oled_channel = 1
    oled_reset = None
    battery = None
    battery_breakout_volt = 10.0
    battery_address = 0x69
    battery_channel = 0
    battery_port = 1
    battery_RV = 45000
    battery_RG = 5000
    battery_divider = 10.0
    battery_shutdown = 'sudo shutdown now "Batterie faible !"'
    shutdown = None
    running = None
    keypad = None
    keypad_r = [0, 0, 0, 0]
    keypad_c = [0, 0, 0, 0]
    devices = {}
    inputs = {}
    outputs = {}
    mail_user = u''
    mail_password = u''
    mail_server = u'UNKNOWN_SMTP'
    mail_port = 587
    sms_user = u''
    sms_password = u''
    sms_server = u'UNKNOWN_SMTP'
    sms_port = 587
    sensor_polling = 60   # 60 seconds between sensors polling...

    def parse_section_system(self):
        if self.config.has_section('system'):
            if u'system' in self.config.sections():
                for anItem in self.config.items(u'system'):
                    if anItem[0].lower() == u'rundirectory':
                        self.rundirectory = unicode(anItem[1]).strip()
                        try:
                            if not os.path.exists(self.rundirectory):
                                os.makedirs(self.rundirectory)
                        except OSError:
                            print('Impossible de creer le dossier '
                                  + self.rundirectory + '.')
                            sys.exit()
                    elif anItem[0].lower() == u'model':
                        self.model = anItem[1]

    def parse_section_I2C(self):
        if u'I2C' in self.config.sections():
            for anItem in self.config.items(u'I2C'):
                if anItem[0].lower() == u'bus':
                    try:
                        self.i2c_bus = int(anItem[1])
                    except:
                        print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

    def __init__(self, config_file):
        self.hostname = socket.gethostname()
        config_file = get_config_file_path(config_file, self.hostname)
        self.config = ConfigParser.RawConfigParser()
        try:
            self.config.readfp(codecs.open(config_file, 'r', 'utf8'))
        except IOError:
            new_path = os.path.join(HARDdirectory, 'DEFAULT.ini')
            print(config_file+' not found. Using ' + new_path)
            try:
                self.config.readfp(codecs.open(os.path.expanduser(new_path),
                                               'r',
                                               'utf8'))
            except IOError:
                print("No valid hardware configuration file found. \
                       Using defaults...")
                return
    
        self.parse_section_system()
        self.parse_section_I2C()
# TODO:Finish copying sections to functions
       
        if u'SPI' in self.config.sections():
            for anItem in self.config.items(u'SPI'):
                if anItem[0].lower() == u'channel':
                    try:
                        self.spi_channel = int(anItem[1])
                    except:
                        print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

        if u'PCB' in self.config.sections():
            for anItem in self.config.items(u'PCB'):
                if anItem[0].lower() == u'installed':
                    self.pcb = anItem[1]
                    if not self.pcb:
                        self.pcb = None
                    elif self.pcb.lower().startswith(u'no'):
                        self.pcb = None
                    elif self.pcb.startswith(u'0'):
                        self.oled_reset = 5
                        self.pcb = '0'
                    elif self.pcb.startswith(u'1'):
                        self.oled_reset = 25
                        self.pcb = '1'
                    else:
                        self.oled_reset = None

        if u'ELA' in self.config.sections():
            for anItem in self.config.items(u'ELA'):
                if anItem[0].lower() == u'installed':
                    self.ela = anItem[1]
                    if not self.ela:
                        self.ela = None
                    elif self.ela.lower().startswith(u'no'):
                        self.ela = None

                elif anItem[0].lower() == u'bauds':
                    try:
                        self.ela_bauds = int(anItem[1])
                    except:
                        print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

                elif anItem[0].lower() == u'reset':
                    self.ela_reset = anItem[1]

        if u'bluetooth' in self.config.sections():
            for anItem in self.config.items(u'bluetooth'):
                if anItem[0].lower() == u'installed':
                    self.bluetooth = anItem[1]
                    if not self.bluetooth:
                        self.bluetooth = None
                    elif self.bluetooth.lower().startswith(u'no'):
                        self.bluetooth = None

        if u'wifi' in self.config.sections():
            for anItem in self.config.items(u'wifi'):
                if anItem[0].lower() == u'installed':
                    self.wifi = anItem[1]
                    if not self.wifi:
                        self.wifi = None
                    elif self.wifi.lower().startswith(u'no'):
                        self.wifi = None

        if u'owfs' in self.config.sections():
            for anItem in self.config.items(u'owfs'):
                if anItem[0].lower() == u'installed':
                    self.owfs = anItem[1]
                    if not self.owfs:
                        self.owfs = None
                    elif self.owfs.lower().startswith(u'no'):
                        self.owfs = None

        if u'sensors' in self.config.sections():
            for anItem in self.config.items(u'sensors'):
                if anItem[0].lower() == u'polling':
                    try:
                        self.sensor_polling = int(anItem[1])
                    except:
                        print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

        if u'OLED' in self.config.sections():
            for anItem in self.config.items(u'OLED'):
                if anItem[0].lower() == u'installed':
                    self.oled = anItem[1]
                    if not self.oled:
                        self.oled = None
                    elif self.oled.lower().startswith(u'no'):
                        self.oled = None

                elif anItem[0].lower() == u'i2c':
                    try:
                        self.oled_address = int(anItem[1], 16)
                    except:
                        print(anItem[0] + '='
                                        + anItem[1]
                                        + ' is not in hexadecimal')

                elif anItem[0].lower() == u'spi':
                    try:
                        self.oled_channel = int(anItem[1])
                    except:
                        print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

                elif anItem[0].lower() == u'reset':
                    try:
                        self.oled_reset = int(anItem[1])
                    except:
                        print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

        if u'battery' in self.config.sections():
            for anItem in self.config.items(u'battery'):
                if anItem[0].lower() == u'installed':
                    self.battery = anItem[1]
                    if not self.battery \
                            or self.battery.lower().startswith(u'no'):
                        self.battery = None
                    elif self.battery.lower().startswith(u'spi'):
                        self.battery = 'SPI'
                    else:  # Anything else than SPI is I2C !
                        self.battery = 'I2C'

                elif anItem[0].lower() == u'shutdown':
                    a_command = anItem[1]
                    if a_command and (a_command.lower() != u'no'):
                        self.battery_shutdown = a_command

                elif anItem[0].lower() == u'breakout_volt':
                    try:
                        self.battery_breakout_volt = float(anItem[1])
                    except:
                        print (anItem[0]+': '+anItem[1]+' is not decimal.')

                elif anItem[0].lower() == u'i2c':
                    try:
                        self.battery_address = int(anItem[1], 16)
                    except ValueError:
                        print(anItem[0] + '='
                                        + anItem[1]
                                        + ' is not in hexadecimal')
                        raise
                elif anItem[0].lower() == u'spi':
                    try:
                        self.battery_channel = int(anItem[1])
                    except:
                        print (anItem[0]+': '+anItem[1]+' is not decimal.')

                elif anItem[0].lower() == u'port':
                    try:
                        self.battery_port = int(anItem[1])
                    except:
                        print (anItem[0]+': '+anItem[1]+' is not decimal.')

                elif anItem[0].lower() == u'rv':
                    try:
                        self.battery_rv = int(anItem[1])
                    except:
                        print (anItem[0]+': '+anItem[1]+' is not decimal.')

                elif anItem[0].lower() == u'rg':
                    try:
                        self.battery_rg = int(anItem[1])
                    except:
                        print (anItem[0]+': '+anItem[1]+' is not decimal.')

        if self.battery:
            self.battery_divider = (float(self.battery_rv)
                                    + float(self.battery_rg))/float(self.battery_rg)
            print("Battery voltage divider="+str(self.battery_divider))

        if u'shutdown' in self.config.sections():
            for anItem in self.config.items(u'shutdown'):
                if anItem[0].lower() == u'installed':
                    self.shutdown = anItem[1]
                    if not self.shutdown:
                        self.shutdown = None
                    elif self.shutdown.lower().startswith(u'no'):
                        self.shutdown = None
                    else:
                        try:
                            self.shutdown = int(self.shutdown)
                        except:
                            print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

        if u'running' in self.config.sections():
            for anItem in self.config.items(u'running'):
                if anItem[0].lower() == u'installed':
                    self.running = anItem[1]
                    if not self.running:
                        self.running = None
                    elif self.running.lower().startswith(u'no'):
                        self.running = None
                    else:
                        try:
                            self.running = int(self.running)
                        except:
                            print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

        if u'mail' in self.config.sections():
            for anItem in self.config.items(u'mail'):
                if anItem[0].lower() == u'user':
                    self.mail_user = anItem[1]
                elif anItem[0].lower() == u'password':
                    self.mail_password = anItem[1]
                elif anItem[0].lower() == u'server':
                    self.mail_server = anItem[1]
                elif anItem[0].lower() == u'port':
                    self.mail_port = anItem[1]
                    if not self.mail_port:
                        self.mail_port = 587
                    else:
                        try:
                            self.mail_port = int(self.mail_port)
                        except:
                            print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')

        if u'sms' in self.config.sections():
            for anItem in self.config.items(u'sms'):
                if anItem[0].lower() == u'user':
                    self.sms_user = anItem[1]
                elif anItem[0].lower() == u'password':
                    self.sms_password = anItem[1]
                elif anItem[0].lower() == u'server':
                    self.sms_server = anItem[1]
                elif anItem[0].lower() == u'port':
                    self.sms_port = anItem[1]

        if u'keypad' in self.config.sections():
            for anItem in self.config.items(u'keypad'):
                if anItem[0].lower() == u'installed':
                    self.keypad = anItem[1]
                    if not self.keypad:
                        self.keypad = None
                    elif self.keypad.lower().startswith(u'no'):
                        self.keypad = None
                    elif self.pcb == '0':
                        self.keypad_r = [18, 23, 24, 25]
                        self.keypad_c = [4, 17, 22, 0]
                    elif self.pcb == '1':
                        self.keypad_r = [26, 12, 20, 21]
                        self.keypad_r = [5, 6, 13, 19]
                elif anItem[0][0].lower == 'r':
                    try:
                        x = int(anItem[0][1])
                        try:
                            self.keypad_r[x] = int(anItem[1])
                        except:
                            print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')
                    except:
                        pass
                elif anItem[0][0].lower == 'c':
                    try:
                        x = int(anItem[0][1])
                        try:
                            self.keypad_c[x] = int(anItem[1])
                        except:
                            print (anItem[0] + ': ' + anItem[1] + ' is not decimal.')
                    except:
                        pass
        
        for section_string in (j for j in self.config.sections() if '.' in j):
            name = section_string.split('.')[1]
            section = self.config.items(section_string)
            if section_string.startswith('device'):
                self.devices[name] = self.parse_one_subsection(section,
                                                               name,
                                                               'device')
            elif section_string.startswith('input'):
                self.inputs[name] = self.parse_one_subsection(section,
                                                              name,
                                                              'input')
            elif section_string.startswith('output'):
                self.outputs[name] = self.parse_one_subsection(section,
                                                               name,
                                                               'output')

    def parse_one_subsection(self, section, name, type):
        output = {}
        REQUIRED_ITEMS = {}
        REQUIRED_ITEMS['device'] = ['install']
        REQUIRED_ITEMS['input'] = []
        REQUIRED_ITEMS['output'] = ['device']
        VALID_ITEMS = {}
        VALID_ITEMS['device'] = REQUIRED_ITEMS['device'] + ['amplification',
                                                            'i2c']
        VALID_ITEMS['input'] = REQUIRED_ITEMS['input'] + ['device',
                                                          'channel',
                                                          'resolution',
                                                          'poweroutput',
                                                          'delayms',
                                                          'serialport',
                                                          'sdiaddress']
        VALID_ITEMS['output'] = REQUIRED_ITEMS['output'] + ['channel', 'invert']
        
        for i in section:
            if i[0] in VALID_ITEMS[type]:
                output[i[0]] = i[1]
            else:
                raise ValueError('Unknown configuration item "' + i[0]
                                                                + '" for '
                                                                + type
                                                                + ' "'
                                                                + name
                                                                + '"')
        for i in REQUIRED_ITEMS[type]:
            if i not in output:
                raise KeyError('Missing configuration item "' + i
                                                              + '" for '
                                                              + type
                                                              + ' "'
                                                              + name
                                                              + '"')
        return output
