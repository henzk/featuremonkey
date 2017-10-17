# coding: utf-8
from __future__ import print_function, unicode_literals
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

    def log(self, operation=None, new_value="", old_value=""):
        pass

    def log_old_value(self, operation=None, old_value=""):
        pass

    def log_new_value(self, operation=None, new_value=""):
        """
        Needed in case the old value must be logged before the new value is applied.
        This way both entries can be logged separately with their current values.
        :param operation:
        :param new_value:
        :return:
        """
        pass


class OperationLogger(NullOperationLogger):
    operation_log = OPERATION_LOG

    @staticmethod
    def _get_lazy_translation_value(value):
        """
        Special handling for top level (not nested in other data structures) lazy translation objects.
        This should prevent the translation process and so there is no import guard error.
        It should cover most cases of translation usage.
        :param value:
        :return:
        """
        if hasattr(value, '_proxy____args'):
            translation_args = getattr(value, '_proxy____args')
            return "".join(translation_args)

    def log(self, operation=None, new_value="", old_value=""):
        if operation is None:
            operation = dict()
        operation['new_value'] = copy.deepcopy(new_value)
        operation['old_value'] = copy.deepcopy(old_value)
        self.operation_log.append(operation)

    def log_new_value(self, operation=None, new_value=""):
        if operation is None:
            operation = dict()
        translation_value = self._get_lazy_translation_value(new_value)
        if translation_value:
            self.operation_log[self.operation_log.index(operation)]['new_value'] = translation_value
        else:
            self.operation_log[self.operation_log.index(operation)]['new_value'] = copy.deepcopy(new_value)
