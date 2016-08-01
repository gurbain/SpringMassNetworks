#! /usr/bin/env python2

from roboTraining.hpc import *

if __name__ == "__main__":
	"""Start the experiment function with different parameters"""

	trainingIt = 10
	simTime = 0.5

	# Get MPI info
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	machine = platform.node()

	# Print machine info	
	print("\n == Initializing Robot Training Experiment == ")
	print("\n  Date: " + str(datetime.datetime.now()))
	print("  Machine: " + machine + " (" + str(rank+1) + "/" + str(size) + ")")
	print("  OS: " + str(platform.system()) + " version " + str(platform.release()))
	print("  Python version: " + str(platform.python_version ()))
	print("  Argument List: " +  str(sys.argv) + "\n")

	# Do experiment
	if len(sys.argv) > 1:

		#  Different couple of amplitude and omega to create a pareto curve
		if sys.argv[1].lower() == "pareto":

			# Get arg list and estimate iteration number and time
			arg_list = createParetoVal(3)
			fileName = "Machine-" + str(rank)
			n_iteration = int(math.ceil(len(arg_list)/float(size)))
			print(" == Running " +  str(len(arg_list)) + " experiments on " + str(size) + \
				" processors: " + str(n_iteration) + " optimizations expected in approximately " + \
				"{:.2f} hours == \n".format(float(simTime) / 20 * trainingIt * n_iteration / 3600))

			# Simulate multiple time if the number of cores does not correspond to number of points
			for i in range(n_iteration):
				index = i * size + rank
				if index < len(arg_list):
					print("-- " + machine + " (" + str(rank+1) + "/" + str(size) + ")" + \
						" -- Experiment " + str(index+1) + " with Omega=" + \
						str(arg_list[index][0]) + " and Amplitude=" + str(arg_list[index][1]))
					e = Experiment(fileName_=fileName, folderName_="Pareto", maxOmega_=arg_list[index][0], \
						simTime_=simTime, maxIter_=trainingIt,  maxAmplitude_=arg_list[index][1])
					e.run()

		#  Different couple of simulation time and optimization methods
		if sys.argv[1].lower() == "simtime":

			# Get arg list and estimate iteration number and time
			arg_list = createSimTimeVal()
			fileName = "Machine-" + str(rank)
			n_iteration = int(math.ceil(len(arg_list)/float(size)))
			time = 0
			for i in range(n_iteration):
				index = i * size + rank
				if index < len(arg_list):
					time += float(arg_list[index][0]) / 20 * trainingIt * n_iteration / 3600
					print("Time value: " + str(time))
			print(" == Running " +  str(len(arg_list)) + " experiments on " + str(size) + \
				" processors: " + str(n_iteration) + " optimizations expected in approximately " + \
				"{:.2f} hours == \n".format(time) )

			# Simulate multiple time if the number of cores does not correspond to number of points
			for i in range(n_iteration):
				index = i * size + rank
				if index < len(arg_list):
					print("-- " + machine + " (" + str(rank+1) + "/" + str(size) + ")" + \
						" -- Experiment " + str(index+1) + " with Omega=" + \
						str(arg_list[index][0]) + " and Amplitude=" + str(arg_list[index][1]))
					e = Experiment(fileName_=fileName, folderName_="SimTime", simTime_=arg_list[index][0],\
					maxIter_=trainingIt, optMethod_=arg_list[index][1])
					e.run()

	else:
		# Pool of CMA otpimization with the same argument list
		print(" == Running " +  str(size) + " experiments on " + str(size) + \
			" processors: 1 optimization expected in approximately " + \
			"{:.2f} hours == \n".format(float(simTime) / 20 * trainingIt / 3600))
		fileName = "Machine-" + str(rank)

		e = Experiment(fileName_=fileName, folderName_="CMA", simTime_=simTime, maxIter_=trainingIt)
		e.run()