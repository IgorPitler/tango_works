from sardana.macroserver.macro import macro

@macro()
def hello_world(self):
    self.output("Hello, World!")