class PluginError(Exception):
    def __init__(self, value=None):
        self.value = value or ""


class PluginFormatError(PluginError):
    def __init__(self, value):
        super(PluginFormatError, self).__init__(value)

    def __str__(self):
        return f"Plugin format error: ({self.value})"


class PluginRuntimeError(PluginError):
    def __init__(self, value):
        super(PluginRuntimeError, self).__init__(value)

    def __str__(self):
        return f"Plugin runtime error: ({self.value})"


class PluginVerifyError(PluginError):
    def __init__(self, value=None):
        super(PluginVerifyError, self).__init__(value)

    def __str__(self):
        return f"Plugin additional verification failed: ({self.value})"


class NotInstanciable(PluginError):
    def __init__(self):
        super(NotInstanciable, self).__init__()

    def __str__(self):
        return f"Base class may not be instantiated"


class DependencyMissing(PluginError):
    def __init__(self, value=None, dependency=None):
        super(DependencyMissing, self).__init__(value)
        self.dependency = None or dependency

    def __str__(self):
        return f"Missing dependency ({type(self.dependency).__name__}): \
                {self.dependency.dependency_name}"


class ModuleDependencyMissing(DependencyMissing):
    pass


class BinaryDependencyMissing(DependencyMissing):
    pass


class FileDependencyMissing(DependencyMissing):
    pass
