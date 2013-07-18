import argparse

from virtualmachine.allvmexception import VMManipulatorException, VMException
from virtualmachine.vmmanipulator import VMManipulator, VirtualMachine


def init_argparser():
    try:
        parser = argparse.ArgumentParser(description='Works with virtual '\
                                                         'machines (VM)')
        parser.add_argument('operation', help='name of operation: create, ' \
                         ' start, shutdown, delete, reboot, info', nargs='?')
        parser.add_argument('--name', help='name of VM')
        parser.add_argument('--vcpu', help='size vcpu for VM', default=1)
        parser.add_argument('--ram', help='size ram for VM', default=393816)
        parser.add_argument('--disk', help='source device for VM',
                                                         default='/dev/sr0')
        return parser.parse_args()
    except ValueError:
        raise VMException('Bad value for parameters')


def custom_menu():
    state = "-1"
    while state != "0":
        state = raw_input("Enter 0 - exit, 1 - create, "
           "2 - shutdown, 3 - delete, 4 - start, 5 - reboot, 6 - info\n")
        vm_manipulator = VMManipulator()

        if state == "1":
            name = raw_input("Enter name of VM\n")
            vcpu = raw_input("Enter number vcpu\n")
            ram = raw_input("Enter number of ram\n")
            disk = raw_input("Enter source device\n")

            vm = VMManipulator()
            vm.create(name, vcpu, ram, disk)
            print("VM is running\n")

        elif state == "2":
            name = raw_input("Enter name of VM\n")
            vm_manipulator.shutdown(VirtualMachine(name, None, None,
                                                         None, None, None))
            print("VM was stopped\n")

        elif state == "3":
            name = raw_input("Enter name of VM\n")
            vm_manipulator.delete(VirtualMachine(name, None, None,
                                                         None,  None, None))
            print("VM was deleted")

        elif state == "4":
            name = raw_input("Enter name of VM\n")
            vm_manipulator.start(VirtualMachine(name, None, None,
                                                         None, None, None))
            print('VM was launched')
        elif state == "5":
            name = raw_input("Enter name of VM\n")
            vm_manipulator.reboot(VirtualMachine(name, None, None,
                                                         None, None, None))
            print('VM was reboot')
        elif state == "6":
            vm_manipulator.info()


def console_menu(args):
    if args.operation == 'create':
            vm = VMManipulator()
            vm.create(args.name, args.vcpu, args.ram, args.disk)
            print("VM is running\n")

    elif args.operation == 'shutdown':
        vm_manipulator = VMManipulator()
        vm_manipulator.shutdown(VirtualMachine(args.name, None,
                                                     None, None,  None))
        print("VM was stopped\n")

    elif args.operation == 'delete':
        vm_manipulator = VMManipulator()
        vm_manipulator.delete(VirtualMachine(args.name, None,
                                                     None, None,  None))
        print("VM was deleted")

    elif args.operation == 'start':
        vm_manipulator = VMManipulator()
        vm_manipulator.start(VirtualMachine(args.name, None,
                                                     None, None,  None))
        print("VM was launched")

    elif args.operation == 'reboot':
        vm_manipulator = VMManipulator()
        vm_manipulator.reboot(VirtualMachine(args.name, None,
                                                     None, None,  None))

    elif args.operation == 'info':
        vm_manipulator = VMManipulator()
        vm_manipulator.info()


if  __name__ == '__main__':
    try:
        args = init_argparser()

        if args.operation is None:
            custom_menu()
        else:
            console_menu(args)
    except VMManipulatorException as e:
        print(e.message)
    except VMException as e:
        print(e.message)
    except Exception as e:
        print(e.message)
