import sys
import importlib

class ImportHookBase(object):
    """
    base class for import hooks

    provides utility methods to install and
    remove the hook
    """
    _hook=None

    @classmethod
    def _insert_hook(cls):
        '''
        appends the hook to sys.meta_path

        subclasses may override this method
        to prepend the hook instead of appending it or
        to install the hook in sys.path_hooks instead
        '''
        sys.meta_path.append(cls._hook)

    @classmethod
    def _install(cls):
        """
        install the hook if not already done
        """
        if not cls._hook:
            cls._hook = cls()
            cls._insert_hook()

    @classmethod
    def _uninstall(cls):
        """
        uninstall the hook if installed
        """
        if cls._hook:
            sys.meta_path.remove(cls._hook)
            cls._hook = None


class LazyComposerHook(ImportHookBase):
    """
    Import Hook required for compose_later to work.

    if fsts are queued for composition
    they are superimposed on the target module right
    after it is imported
    """
    _to_compose = dict()

    @classmethod
    def add(cls, module_name, fsts, composer):
        '''
        add a couple of fsts to be superimposed on the module given
        by module_name as soon as it is imported.

        internal - use featuremonkey.compose_later
        '''
        cls._to_compose.setdefault(module_name, [])
        cls._to_compose[module_name].append(
            (list(fsts), composer)
        )
        cls._install()


    def find_module(self, fullname, path=None):
        if fullname in self._to_compose:
            return self


    def load_module(self, module_name):
        layers = self._to_compose.pop(module_name)
        module = importlib.import_module(module_name)
        for fsts, composer in layers:
            fsts.append(module)
            composer.compose(*fsts)
        if not self._to_compose:
            self._uninstall()
        return module
