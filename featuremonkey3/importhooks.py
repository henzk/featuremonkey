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
        sys.meta_path.insert(0, cls._hook)

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


def load_fsts(fst_list):
    from featuremonkey3 import CompositionError
    result = []
    for elem in fst_list:
        if isinstance(elem, str):
            try:
                elem = importlib.import_module(elem)
            except ImportError:
                raise CompositionError(
                    'FST "%s" cannot be imported!' % elem
                )
        result.append(elem)
    return result


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

        internal - use featuremonkey3.compose_later
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
            fsts = load_fsts(fsts)
            fsts.append(module)
            composer.compose(*fsts)
        if not self._to_compose:
            self._uninstall()
        return module


class ImportGuard(ImportError): pass

class ImportGuardHook(ImportHookBase):
    """
    Import Hook to implement import guards.

    In Python imports can have side-effects and import order may be relevant.
    When using featuremonkey, it is important to compose the product before
    making references to it. Otherwise, you could end up with a reference
    to a module/class/object that has only been composed partially.
    This may introduce subtle bugs that are hard to debug.

    Using an import guard, you can enforce that a module cannot be imported until
    the import guard on that module is dropped again.
    Importing a guarded module results in an ImportGuard exception being thrown.
    Usually, you don`t want to catch these:
    better fail during the composition phase than continuing to run a miscomposed
    program.

    The existance of the import hook is considered an implementation detail.
    The public API to import guards are ``featuremonkey3.add_import_guard``
    and ``featuremonkey3.remove_import_guard``.
    """
    _guards = dict()
    _num_entries = 0

    @classmethod
    def _insert_hook(cls):
        #the guard hook needs to be first
        sys.meta_path.insert(0, cls._hook)

    @classmethod
    def add(cls, module_name, msg=''):
        '''
        Until the guard is dropped again,
        disallow imports of the module given by ``module_name``.

        If the module is imported while the guard is in place
        an ``ImportGuard`` is raised. An additional message on why
        the module cannot be imported can optionally be specified
        using the parameter ``msg``.

        If multiple guards are placed on the same module, all these guards
        have to be dropped before the module can be imported again.
        '''
        if module_name in sys.modules:
            raise ImportGuard(
                'Module to guard has already been imported: '
                + module_name
            )
        cls._guards.setdefault(module_name,  [])
        cls._guards[module_name].append(msg)
        cls._num_entries += 1
        cls._install()

    @classmethod
    def remove(cls, module_name):
        """
        drop a previously created guard on ``module_name``
        if the module is not guarded, then this is a no-op.
        """
        module_guards = cls._guards.get(module_name, False)
        if module_guards:
            module_guards.pop()
            cls._num_entries -= 1
            if cls._num_entries < 1:
                if cls._num_entries < 0:
                    raise Exception(
                        'Bug: ImportGuardHook._num_entries became negative!'
                    )
                cls._uninstall()

    def find_module(self, fullname, path=None):
        if self._guards.get(fullname, False):
            return self

    def load_module(self, module_name):
        raise ImportGuard(
            'Import while import guard in place: '
            #msg of latest guard that has been placed on module
            + (self._guards[module_name][-1] or module_name)
        )
