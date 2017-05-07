#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Rudolf Sandbox
# version = 0.1
# author = felicitychou
# email = felicitychou@hotmail.com

import os
import time
import random
from configparser import ConfigParser

import paramiko
import pexpect


class DynamicAnalyzer(object):

    def __init__(self,filepath,filetype,result_path,sandbox_id,logger,conf):
        self.filepath = filepath
        self.filetype = filetype
        self.result_path = result_path
        self.sandbox_id = sandbox_id
        self.logger = logger
        self.conf = conf
        self.run()

    def _get_qemu_conf(self):
        config = ConfigParser()
        config.read_file(open('rudolf.cfg'))
        return config['qemu-%s-%s'% (self.platform,self.sandbox_id)]

    def _identify_platform(self):
        '''
        :return self.platform
        '''
        filetype = self.filetype
        self.platform = None
        if "ELF 32-bit" in filetype:
            if "ARM" in filetype:
                self.platform = "arm"
            elif "80386" in filetype:
                self.platform = "x86"
            elif ("MIPS" in filetype) and ("MSB" in filetype):
                self.platform = "mips"
            elif "MIPS" in filetype:
                self.platform = "mipsel"
            elif "PowerPC" in filetype:
                self.platform = "powerpc"
            else:
                self.platform = None
        elif "ELF 64-bit" in filetype:
            if "x86-64" in filetype:
                self.platform = "x86-64"
            else:
                self.platform = None
        else:
            self.platform = None



    def run(self):
        # get platform
        self._identify_platform()
        if not self.platform:
            return

        # get qemu conf
        qemu_conf = self._get_qemu_conf()
        host = qemu_conf['ip']
        port = int(qemu_conf['port'])
        user = qemu_conf['user']
        password = qemu_conf['password']
        macaddr = qemu_conf['macaddr']


        # A randomly generated sandbox filename
        dst_binary_filepath = "/tmp/" + ("".join(chr(random.choice(range(97,123))) for _ in range(random.choice(range(6,12)))))

        # start machine
        qemu_command = self.qemu_commands()

        qemu_command += " -net nic,macaddr=%s -net tap -monitor stdio" % (macaddr,)
        self.logger.info(qemu_command)
        qemu = pexpect.spawn(qemu_command)
        try:
            qemu.expect("(qemu).*")
            qemu.sendline("info network")
            qemu.expect("(qemu).*")
            ifname =  qemu.before.decode().split("ifname=", 1)[1].split(",", 1)[0]
            qemu.sendline("loadvm init")
            qemu.expect("(qemu).*")
            # copy sample
            self.scp(host=host, port=port, user=user, password=password, src_file = self.filepath, dst_file = dst_binary_filepath, mode = 'put')
            # Pre binary execution commands
            pre_exec = self.ssh_execute(host=host, port=port, user=user, password=password,commands = ["chmod +x %s" % (dst_binary_filepath,)])
            # Start Packet Capture
            pcap_command = "/usr/bin/dumpcap -i %s -P -w %s -f 'not ((tcp dst port %d and ip dst host %s) or (tcp src port %d and ip src host %s))'"
            pcap_filepath = os.path.join(self.result_path, "pcap")
            pcapture = pexpect.spawn(pcap_command % (ifname, pcap_filepath, port, host, port, host))

            # wait for pcapture to start and then Execute the binary
            time.sleep(5)
            stace_log = '/tmp/strace.log'
            command_to_exec = "strace -ttt -x -o %s -f %s" % (stace_log,dst_binary_filepath)
            print("Executing %s" % (command_to_exec,))
            exec_ssh = self.ssh_execute(host, port, user, password, command_to_exec, True, False)

            starttime = time.time()
            while time.time() < starttime + int(self.conf['Timeout']):
                if not qemu.isalive():
                    exec_time = 0
            if qemu.isalive():
                # Post binary execution commands
                post_exec = self.ssh_execute(host, port, user, password, ["ps aux"])
                strace_logpath = os.path.join(self.result_path,'strace.log')
                self.scp(host = host, port = port, user = user, password = password, src_file = stace_log, dst_file = strace_logpath, mode = 'get')
                try:
                    if exec_ssh != None:
                        exec_ssh.close()
                except Exception as e:
                    self.logger.info("Error while logging out exec_ssh: %s" % (e,))
                qemu.sendline("q")

            # Stop Packet Capture
            if pcapture.isalive():
                pcapture.close()

            endtime = time.time()
            #result = {'start_time': sandbox_starttime, 'end_time': sandbox_endtime, 'pcap_filepath': pcap_filepath}
            #result['post_exec_result'] = post_exec

        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))
            if qemu.isalive():
                qemu.close()
            return {}

        #return result

    def output(self):
        return None

    def qemu_commands(self):
        platform = self.platform
        sandbox_id = self.sandbox_id
        if platform == "x86":
            return "sudo qemu-system-i386 -hda qemu/x86/%s/debian_wheezy_i386_standard.qcow2 -vnc 127.0.0.1:1%s" % (sandbox_id, sandbox_id, )
        if platform == "x86-64":
            return "sudo qemu-system-x86_64 -hda qemu/x86-64/%s/debian_wheezy_amd64_standard.qcow2 -vnc 127.0.0.1:2%s" % (sandbox_id, sandbox_id,)
        if platform == "mips":
            return 'sudo qemu-system-mips -M malta -kernel qemu/mips/%s/vmlinux-3.2.0-4-4kc-malta -hda qemu/mips/%s/debian_wheezy_mips_standard.qcow2 -append "root=/dev/sda1 console=tty0" -vnc 127.0.0.1:3%s'  % (sandbox_id, sandbox_id, sandbox_id,)
        if platform == "mipsel":
            return 'sudo qemu-system-mipsel -M malta -kernel qemu/mipsel/%s/vmlinux-3.2.0-4-4kc-malta -hda qemu/mipsel/%s/debian_wheezy_mipsel_standard.qcow2 -append "root=/dev/sda1 console=tty0" -vnc 127.0.0.1:4%s'  % (sandbox_id, sandbox_id, sandbox_id, )
        if platform == "arm":
            return 'sudo qemu-system-arm -M versatilepb -kernel qemu/arm/%s/vmlinuz-3.2.0-4-versatile -initrd qemu/arm/%s/initrd.img-3.2.0-4-versatile -hda qemu/arm/%s/debian_wheezy_armel_standard.qcow2 -append "root=/dev/sda1" -vnc 127.0.0.1:5%s'  % (sandbox_id, sandbox_id, sandbox_id, sandbox_id,)
        return None


    def ssh_execute(self, host, port, user, password, commands, noprompt = False, logout = True):
        result = None
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port = port, username = user, password = password)
            if type(commands) == type(str()):
                stdin, stdout, stderr = ssh.exec_command(commands, timeout = 10)
                if noprompt == False:
                    result = "".join(stdout.readlines())
            if type(commands) == type(list()):
                result = {}
                for command in commands:
                    stdin, stdout, stderr = ssh.exec_command(command, timeout = 10)
                    result[command] = "".join(stdout.readlines())
            if logout:
                ssh.close()
            else:
                return ssh  # Return SSH object to logout later
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))
        return result


    def scp(self, host, port, user, password, src_file, dst_file, mode):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port = port, username = user, password = password)
            sftp = ssh.open_sftp()
            getattr(sftp,mode)(src_file, dst_file)
            #sftp.put(src_file, dst_file)
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))
