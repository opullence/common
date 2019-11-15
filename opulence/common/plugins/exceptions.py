class PluginError(Exception):
    def __init__(self, value=None):
        self.value = value or ""


class PluginVerifyError(PluginError):
    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return "Plugin additional verification failed: ({})".format(self.value)


class PluginFormatError(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Plugin format error: ({})".format(self.value)


class PluginRuntimeError(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Plugin runtime error: ({})".format(self.value)


class DependencyMissing(PluginError):
    def __init__(self, value=None, dependency=None):
        super(DependencyMissing, self).__init__(value)
        self.dependency = None or dependency

    def __str__(self):
        return "Missing dependency ({}): {}".format(
            type(self.dependency).__name__, self.dependency)


class ModuleDependencyMissing(DependencyMissing):
    pass


class BinaryDependencyMissing(DependencyMissing):
    pass


class FileDependencyMissing(DependencyMissing):
    pass
