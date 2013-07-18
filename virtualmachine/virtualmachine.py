from interface import BaseVirtualMachine

class VirtualMachine(BaseVirtualMachine):

    uuid = None
    name = None
    vcpu = None
    ram = None
    status = None
    libvirt_url = None

    def __init__(self, name, uuid, vcpu, ram, libvirt_url, status):
        self.uuid = uuid
        self.name = name
        self.vcpu = vcpu
        self.ram = ram
        self.status = status
        self.libvirt_url = libvirt_url
