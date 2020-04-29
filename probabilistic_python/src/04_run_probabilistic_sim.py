# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# todo run each of the probabilistic sim .inp files, and save the results to a cohesive data frame

# setup
from pyswmm import Simulation
import os

# nsims
nsims = 5

# todo set up dataframe to receive the outputs from the simulations...below

# run swmm, for each sim
for i in range(1, nsims+1):
    simfolder = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm\input_' + str(i)
    print(simfolder)
    print(os.path.exists(simfolder))

    simfile = os.path.join(simfolder, "NPlesantCreek" + "." + "inp")
    print(simfile)

    sim = Simulation(simfile)
    sim.execute()

    # todo grab the desired output variable of interest, and store in dataframe (created above loop)

# --------------------------------------------------------
# the end
# --------------------------------------------------------