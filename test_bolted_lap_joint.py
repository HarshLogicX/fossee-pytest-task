import pytest
from bolted_lap_joint_design import design_lap_joint

@pytest.mark.parametrize("P", range(0, 101, 10))
@pytest.mark.parametrize("t1", [6, 8, 10, 12, 16, 20, 24])
@pytest.mark.parametrize("t2", [6, 8, 10, 12, 16, 20, 24])
def test_minimum_two_bolts(P, t1, t2):
    w = 150
    try:
        design = design_lap_joint(P, w, t1, t2)
        assert design["number_of_bolts"] >= 2
    except ValueError:
        assert P == 0
