from threading import local


class AAA:
    def a():
        """ree"""
        print(AAA.a.__doc__)

    def b():
        """reeee"""
        print(AAA.b.__doc__)

    def c():
        """reeeeee"""
        print(AAA.c.__doc__)

    def help():
        """Prints this page"""
        commands = [method for method in dir(AAA) if method.startswith('__') is False]
        for func in commands:
            a = getattr(AAA, func)
            print(f"""- {func} -- {a.__doc__}""")

AAA.help()