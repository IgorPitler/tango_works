from typing import Sequence

from sardana.pool.controller import PseudoMotorController

class Sample_pseudo_motor_controller(PseudoMotorController):
    # slit
    pseudo_motor_position = 0

    mot_top_postion=0 # 0
    mot_bottom_postion=0 # 1

    motor_roles = "mot_top", "mot_bottom"

    def __init__(self, inst, props, *args, **kwargs):
        PseudoMotorController.__init__(self, inst, props, *args, **kwargs)

    def CalcPseudo(self, axis: int, physical_pos: Sequence[float], curr_pseudo_pos: Sequence[float]) -> float:
        self.pseudo_motor_position = physical_pos[0]+physical_pos[1]
        return self.pseudo_motor_position

    def CalcPhysical(self, axis: int, pseudo_pos: Sequence[float], curr_physical_pos: Sequence[float]) -> float:
        half_gap = pseudo_pos[0] / 2
        if axis == 0 : # top
            self.mot_top_postion = half_gap
            return self.mot_top_postion
        if axis == 1 : # bottom
            self.mot_bottom_postion = half_gap
            return self.mot_bottom_postion
        return 0



