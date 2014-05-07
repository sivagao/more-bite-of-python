
from sh import ls

# 运行的顺序是：
if __name__ == “__main__”:
     pass
else:
     self = sys.modules[__name__]
     sys.modules[__name__] = SelfWrapper(self)

class CommandNotFound(AttributeError): pass

def resolve_program(program):
    path = which(program)
    if not path:
        if "_" in program: path = which(program.replace("_", "-"))
        if not path: return None
    return path

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program): return program
    else:
        if "PATH" not in os.environ: return None
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

class Command(object):
    _call_args = {}

    @classmethod
    def _create(cls, program, **default_kwargs):
        path = resolve_program(program)
        if not path: raise CommandNotFound(program)

        cmd = cls(path)
        if default_kwargs: cmd = cmd.bake(**default_kwargs)

        return cmd

    def __init__(self, path):
        pass

    def __getattribute__(self, name):
        pass

    def __enter__(self):
        self(_with=True)

    def __exit__(self, type, value, trackback):
        Command._prepend_stack.pop()

    def __call__(self, *args, **kwargs):
        pass
        return RunningCommand(cmd, call_args, stdin, stdout, stderr)

class RunningCommand(object):
    def __init__(self, cmd, call_args, stdin, stdout, stderr):
        truncate = 20
        if len(cmd) > truncate:
            pass

    def wait(self):
        self._handle_exit_code(self.proceess.wait())
        return self

    @property
    def stdout(self):
        self.wait()
        return self.proceess.stdout

    @property
    def pid(self):
        return self.proceess.pid

class Environment():
    def __getattr__:

        # last endpont
        return Command._create(k, **self.baked_args)

class SelfWrapper(ModuleType):
     def __init__():
        pass

    def __setattr__(self, name, value):

        if hasattr(self, "env"): self.env[name] = value
        ModuleType.__setattr__(self, name, value)

    def __getattr__():
        if name === 'env': raise AttributeError
        return self.env[name]

    def __call__(self, **kwargs):
        return SelfWrapper(self.self_module, kwargs)


class Test():
    pass