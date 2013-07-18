import uuid

import libvirt
from lxml import etree

import config
from interface import BaseVMManager
from virtualmachine import VirtualMachine
from scheduler import ChanceScheduler, UtilisationScheduler
from allvmexception import VMManipulatorException, VMException, SchedulerException


class VMManipulator(BaseVMManager):

    def __init__(self):
        self.xml = ""

    def __generate_xml(self, name, vcpu, ram, disk,
                                 domain_type, emulator, uuid):

        root = etree.Element("os")
        etree.SubElement(root, "type").text = "hvm"
        subroot = etree.Element("boot", dev='cdrom')
        root.append(subroot)
        sub_el = etree.tostring(root)

        root = etree.Element("domain", type=domain_type)
        etree.SubElement(root, "name").text = name
        etree.SubElement(root, "uuid").text = uuid
        etree.SubElement(root, "memory").text = ram
        etree.SubElement(root, "currentMemory").text = "393216"
        etree.SubElement(root, "vcpu").text = vcpu
        root.append(etree.XML(sub_el))

        subroot = etree.Element("clock", offset="utc")
        root.append(subroot)

        etree.SubElement(root, "on_poweroff").text = "destroy"
        etree.SubElement(root, "on_reboot").text = "restart"
        etree.SubElement(root, "on_crash").text = "destroy"

        subroot = etree.Element("devices")
        etree.SubElement(subroot, "emulator").text = emulator
        insubroot = etree.Element("disk", device='disk', type='block')
        insubroot.append(etree.Element("source", dev=disk))
        insubroot.append(etree.Element("target", dev='hda', bus='ide'))
        subroot.append(insubroot)

        subroot.append(etree.Element("input", type='tablet', bus='usb'))
        subroot.append(etree.Element("input", type='mouse', bus='ps2'))
        subroot.append(etree.Element("graphics", type='vnc',
                                           port='-1', listen='127.0.0.1'))

        root.append(subroot)

        return etree.tostring(root, pretty_print=True)

    def create(self,
               name,
               vcpu,
               ram,
               disk,
               domain_type='qemu',
               emulator='/usr/bin/kvm'):
        try:
            libvirt_url = ''

            if config.SCHEDULER_TYPE == 'ChanceScheduler':
                libvirt_url = ChanceScheduler().schedule()
            elif config.SCHEDULER_TYPE == 'UtilisationScheduler':
                libvirt_url = UtilisationScheduler().schedule()

            url = 'qemu+ssh://{0}/system'.format(libvirt_url)
            conn = libvirt.open(url)

            uu = str(uuid.uuid4())
            xml = self.__generate_xml(name, vcpu, ram,
                                        disk, domain_type, emulator, uu)
            conn.defineXML(xml)
            dom = conn.lookupByName(name)
            dom.create()

            return VirtualMachine(name, uu,  vcpu, ram, libvirt_url, None)
        except libvirt.libvirtError:
            raise VMManipulator('Is not possible to create a VM')    

    def start(self, vm):
        try:
            conn = libvirt.open('qemu+ssh://' + vm.libvirt_url + '/system')
            dom = conn.lookupByName(vm.name)
            if not dom.isActive():
                dom.create()
        except libvirt.libvirtError:
            raise VMManipulatorException('Is not possible to start a VM')

    def reboot(self, vm):
        try:
            conn = libvirt.open('qemu+ssh://' + vm.libvirt_url + '/system')
            dom = conn.lookupByName(vm.name)
            dom.reset(0)
        except libvirt.libvirtError:
            raise VMManipulatorException('Is not possible to reboot a VM')

    def shutdown(self, vm):
        try:
            conn = libvirt.open('qemu+ssh://' + vm.libvirt_url + '/system')
            dom = conn.lookupByName(vm.name)
            if dom.isActive():
                dom.destroy()
        except libvirt.libvirtError:
            raise VMManipulatorException('Is not possible to shutdown a VM')

    def delete(self, vm):
        try:
            conn = libvirt.open('qemu+ssh://' + vm.libvirt_url + '/system')
            dom = conn.lookupByName(vm.name)
            if dom.isActive():
                dom.destroy()
            dom.undefine()
        except libvirt.libvirtError:
            raise VMManipulatorException('Is not possible to shutdown a VM')

    def list(self):
        try:
            all_vm = ()
            conn = libvirt.open('qemu+ssh://' + vm.libvirt_url + '/system')
            for id in conn.listDomainID():
                dom = conn.lookupByID(id)
                all_vm.append(VirtualMachine(dom.name, None, None,
                                                         None, None, None))
            return all_vm
        except libvirt.libvirtError:
            raise VMManipulatorException('Is not possible get lauched VMs')

    def info(self):
        try:
            conn = libvirt.open('qemu+ssh://' + vm.libvirt_url + '/system')
            names = conn.listDefinedDomains()
            print ("Not launched virtual machines: ")
            print names
            print ("Launched virtual machines' details are:")
            print ("%4s %4s %8s %8s" % ("#:", "ID:", "Name:", "Memory:"))
            for i, id in enumerate(conn.listDomainsID()):
                dom = conn.lookupByID(id)
                infos = dom.info()
                print ("%4d %4d %8s %8s" % (i, id, dom.name(), infos[1]))
        except:
            raise VMManipulatorException('Is not possible '\
                                            'to get info about VM')
