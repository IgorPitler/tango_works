from sardana.macroserver.macro import macro

@macro
def sample_macro1(self):
    self.output("test ok")