"""Train the control signals of a robot to move by optimizing omega, phase, amplitude using GA:"""
from roboTraining.robot import *
from roboTraining.simulate import *
from roboTraining.training import *
from roboTraining.utils import *

# Create Robot, controller and environnement
env = HardEnvironment()
morph = SpringMorphology(noNodes=20 ,spring=100, noNeighbours=3, environment=env)
control = StepControl(morph, stepSize=0, stepTime=0)
robot = Robot(morph,control)

# Define simulation engine parameters
plotter = Plotter(movie=True, plot=True, movieName="a");
simulenv = SimulationEnvironment(1.0/200, simulationLength=600, plot=plotter)
simul = VerletSimulation(simulenv, robot)
score = simul.runSimulation()

# # Create training scheme
# trainscheme = TrainingScheme()
# trainscheme.createTrainVariable("omega", 0, 10)
# trainscheme.createTrainVariable("phase", 0, 2 * np.pi)
# trainscheme.createTrainVariable("amplitude", 0, 0.25)
# saver = Save(None, 'RobotData', 'CMATraining') 
# train = GeneticTraining(trainscheme, robot, simulenv, saver=saver, maxIter=10000)

# # Perform training and save all data and plots
# param, score, t_tot = train.run()
# print("Total training time: " + "{:.1f}".format(t_tot)  + " s")
# train.save()