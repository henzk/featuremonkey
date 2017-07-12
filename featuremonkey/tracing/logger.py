from __future__ import print_function
import copy


OPERATION_LOG = list()


class NullOperationLogger(object):
    """
    Base class for logging the composer operations. Implement this and set it
    in your environment as COMPOSITION_TRACER for real tracing.
    To make the log accessible, use the OPERATION_LOG as your classes log attribute:
        self.operation_log = OPERATION_LOG
    """
    operation_log = OPERATION_LOG

    def log(self, operation=dict(), new_value="", old_value=""):
        pass

    def log_new_value(self, operation=dict(), new_value=""):
        pass

    def log_old_value(self, operation=dict(), old_value=""):
        pass


class OperationLogger(NullOperationLogger):
    operation_log = OPERATION_LOG

    def log(self, operation=dict(), new_value="", old_value=""):
        operation['new_value'] = copy.deepcopy(new_value)
        operation['old_value'] = copy.deepcopy(old_value)
        self.operation_log.append(operation)

    def log_new_value(self, operation=dict(), new_value=""):
        self.operation_log[self.operation_log.index(operation)]['new_value'] = copy.deepcopy(new_value)

    def log_old_value(self, operation=dict(), old_value=""):
        self.operation_log[self.operation_log.index(operation)]['old_value'] = copy.deepcopy(old_value)
