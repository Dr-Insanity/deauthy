from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError

class RequiredDependencies:

    def __init__(self) -> None:
        self.deps = [f"colorama", f"halo"]

    def install(self):
        for dep in self.deps:
            out = check_output(f"pip install {dep} --upgrade --user", shell=True)
