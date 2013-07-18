from interface import BaseVMException


class VMException(BaseVMException):

    def __init__(self, message):
        super(VMException, self).__init__(message)
        self.message = message


class VMManipulatorException(BaseVMException):

    def __init__(self, message):
        super(VMManipulatorException, self).__init__(message)
        self.message = message


class SchedulerException(BaseVMException):

    def __init(self, message):
        super(VMManipulatorException, self).__init__(message)
        self.message = message
