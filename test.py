from base_classes.loading import *
from beam_classes.beam import Beam
from beam_classes.continuousbeam import ContinuousBeam

def main():
    b1 = Beam(1)
    udl_b1 = UdLoadFull(500, 3.5)
    # b1.setUdl(udl_b1)
    p1 = PointLoad(1000, 1.75)
    b1.addPointLoad(p1)
    b1.calc_aml_matrix()
    b1.calcFinalAml()
    print(b1)
    print("-"*20, "\n", "Shear Forces:")
    L1 = b1.getShearForces(0.1)
    for x, sf in L1:
        print(f"{x:.3f}: {sf:8.3f}")
    print("-"*20, "\n", "Bending Moments:")
    L2 = b1.getBendingMoments(0.1)
    for x, bm in L2:
        print(f"{x:.3f}: {bm:8.3f}")
    # cb = ContinuousBeam()

if __name__ == '__main__':
    main()


