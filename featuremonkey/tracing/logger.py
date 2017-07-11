from __future__ import print_function
import copy
from featuremonkey.composer import OPERATION_LOG, NullOperationLogger


class OperationLogger(NullOperationLogger):
    operation_log = OPERATION_LOG

    def log(self, operation=dict(), new_value="", old_value=""):
        operation['new_value'] = copy.deepcopy(new_value)
        operation['old_value'] = copy.deepcopy(old_value)
        self.operation_log.append(operation)
