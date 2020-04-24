# --------------------------------------------------
# run [practice/dummy] simulation
# --------------------------------------------------

# set up
from pyswmm import Simulation, Subcatchments


# load the model - no interaction
sim = Simulation('C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/input/swmm/NPlesantCreek.inp')
for step in sim:
    pass
sim.report()










