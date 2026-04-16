from sardana.macroserver.macro import macro
from sardana.macroserver.msparameter import Type


@macro([["String", Type.String, None, "this is par1 - string"],
       ["Float", Type.Float, None, "this is par2 - float"]]  )
def sample_macro1(self, par1, par2):

    # call other macro
    self.wm("amot1")

    self.output(par1)
    self.output(par2)
    self.output("test ok!")