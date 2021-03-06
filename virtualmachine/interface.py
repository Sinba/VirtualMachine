import abc


class BaseVMException(Exception):
    """Base class for VM exceptions."""
    pass


class BaseVirtualMachine(object):
    """Represents virtual machine."""

    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name,
                 uuid=None,
                 vcpu=None,
                 ram=None,
                 libvirt_url=None,
                 status=None):
        pass

    @abc.abstractproperty
    def uuid(self):
        pass

    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def vcpu(self):
        pass

    @abc.abstractproperty
    def ram(self):
        pass

    @abc.abstractproperty
    def libvirt_url(self):
        pass

    @abc.abstractproperty
    def status(self):
        pass


class BaseVMManager(object):
    """
    Base class fot VM Manager.
    Contains methods for VMs management.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self,
               name,
               vcpu_num,
               ram,
               disk,
               domain_type='qemu',
               emulator='/usr/bin/kvm'):
        """
        Creates VM.

        :param name: VM name
        :type name: str

        :param vcpu_num: number of virtual CPU
        :type vcpu_num: int

        :param ram: amount of RAM in megabytes
        :type ram: int

        :param disk: path to a disk image
        :type disk: str

        :param domain_type: domain type
        :type domain_type: str

        :param emulator: path to the emulator
        :type emulator: str

        :returns: created vm
        :rtype: BaseVirtualMachine
        """
        pass

    @abc.abstractmethod
    def start(self, vm):
        """
        Starts VM.

        :param vm: virtual machine object
        :type vm: BaseVirtualMachine

        :raises: BaseVMException if errors occur
        """
        pass

    @abc.abstractmethod
    def reboot(self, vm):
        """
        Reboots VM.

        :param vm: virtual machine object
        :type vm: BaseVirtualMachine

        :raises: BaseVMException if errors occur
        """
        pass

    @abc.abstractmethod
    def shutdown(self, vm):
        """
        Shutdowns VM.

        :param vm: virtual machine object
        :type vm: BaseVirtualMachine

        :raises: BaseVMException if errors occur
        """
        pass

    @abc.abstractmethod
    def delete(self, vm):
        """
        Deletes VM.

        :param vm: virtual machine object
        :type vm: BaseVirtualMachine

        :raises: BaseVMException if errors occur
        """
        pass

    @abc.abstractmethod
    def list(self):
        """
        List VMs launched ont the libvirt host..

        :raises: BaseVMException if errors occur

        :returns: list of BaseVirtualMachine objects
        """
        pass


class BaseDBDriver(object):
    """Base class for abstraction layer for the DB."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_vm_by_uuid(self, uuid):
        """
        Returns VM with specified uuid.

        :param uuid: VM uuid
        :type name: str

        :raises: BaseVMException if VM not found

        :returns: VM with specified uuid
        :rtype: BaseVirtualMachine
         """
        pass

    @abc.abstractmethod
    def get_vm_by_name(self, name):
        """
        Returns VM with specified name.

        :param uuid: VM uuid
        :type name: str

        :raises: BaseVMException if VM not found

        :returns: VM with specifiedname
        :rtype: BaseVirtualMachine
         """
        pass

    @abc.abstractmethod
    def get_vm_list(self):
        """
        Returns list of VMs.

        :returns: list of VMs
        :rtype: list
        """
        pass

    @abc.abstractmethod
    def update_vm(self, vm, values={} ):
        """
        Updates VM recorn in the DB. Return updated VM.

        ::Examle::

            vm = db_driver.update_vm(vm,
                                     {'status': 'SHUTDOWN',
                                      'name': 'new_name'})

        :param vm: VM to update
        :type vm: BaseVirtualMachine

        :param values: dict of values
        :type values: dict

        :raises: BaseVMException if VM not found

        :returns: updated VM
        :rtype: BaseVirtualMachine
        """
        pass
        
    @abc.abstractmethod
    def delete_vm(self, vm):
        """
        Deletes record about specified VM from the DB.

        :param vm: VM to delete
        :type vm: BaseVirtualMachine

        :raises: BaseVMException if VM not found
        """
        pass


class BaseImage(object):
    """Represents image."""

    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 uuid=None,
                 name=None,
                 url=None,
                 description=None):
        pass

    @abc.abstractproperty
    def uuid(self):
        pass

    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def url(self):
        pass

    @abc.abstractproperty
    def description(self):
        pass

    @abc.abstractmethod
    def download_to(self, file_name):
        """
        Downloads image to the specified place.

        :param file_name: filename for savingo with full path
        :type file_name: str

        :raises: BaseVirtualMachine if errors while downloading occure
        """
        pass

class BaseScheduler(object):
    """Base class for schedulers."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def schedule(self):
        """
        Return libvirt_url of host for VM starting.

        :returns: libvirt url
        :rtype: str
        """
        pass
