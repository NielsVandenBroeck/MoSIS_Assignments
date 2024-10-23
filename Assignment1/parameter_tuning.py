import math
import os
from logging import warning

from pandas import read_csv
from scipy.cluster.hierarchy import maxdists


def CalibrateDc(dc, position_values):
    # Override variable
    simulationCommand='./Trolley_movement -override dc='+str(dc)

    os.chdir('Assignment1.Trolley_movement')

    os.system(simulationCommand)

    # Obtain the variable values by reading the MAT-file
    [names, simulated_data] = readMat('Trolley_movement_res.mat')

    squared_error = 0
    for x_simulated, x_real in zip(simulated_data[2], position_values):
        squared_error += math.pow(float(x_simulated) - x_real,2)

    os.chdir('../')

    return squared_error

def testDc(dc, position_values):
    # Override variable
    simulationCommand = './Trolley_movement -override dc=' + str(dc)

    os.chdir('Assignment1.Trolley_movement')

    os.system(simulationCommand)

    # Obtain the variable values by reading the MAT-file
    [names, simulated_data] = readMat('Trolley_movement_res.mat')

    pyplot.plot(simulated_data[0], position_values, label="real")
    pyplot.plot(simulated_data[0], simulated_data[2], label="simulated")
    pyplot.xlabel('time')
    pyplot.ylabel('displacement')
    pyplot.legend()
    pyplot.savefig('dc_displacement_error')

    os.chdir('../')

def testDp(dp, position_values):
    # Override variable
    simulationCommand = './Pendulum_swinging_motion -override dp=' + str(dp)

    os.chdir('Assignment1.Pendulum_swinging_motion')

    os.system(simulationCommand)

    # Obtain the variable values by reading the MAT-file
    [names, simulated_data] = readMat('Pendulum_swinging_motion_res.mat')
    pyplot.plot(simulated_data[0], position_values, label="real")
    pyplot.plot(simulated_data[0], simulated_data[1], label="simulated")
    pyplot.xlabel('time')
    pyplot.ylabel('angular displacement')
    pyplot.legend()
    pyplot.savefig('dp_displacement_error')

    os.chdir('../')

def CalibrateDp(dp, position_values):
    # Override variable
    simulationCommand='./Pendulum_swinging_motion -override dp='+str(dp)

    os.chdir('Assignment1.Pendulum_swinging_motion')

    os.system(simulationCommand)

    # Obtain the variable values by reading the MAT-file
    [names, simulated_data] = readMat('Pendulum_swinging_motion_res.mat')

    squared_error = 0
    for x_simulated, x_real in zip(simulated_data[1], position_values):
        squared_error += math.pow(float(x_simulated) - x_real,2)

    os.chdir('../')

    return squared_error


def testPID(kp, ki, kd, plot=True):
    simulationCommand = './PID_controller_block -override pID_block.kp=' + str(kp) + ',pID_block.ki=' + str(ki) + ',pID_block.kd=' + str(kd)
    os.chdir('Assignment1.PID_controller_block')
    os.system(simulationCommand)
    # Obtain the variable values by reading the MAT-file
    [names, simulated_data] = readMat('PID_controller_block_res.mat')

    dataLength = len(simulated_data[names.index('time')])

    if plot:
        figure, axis = pyplot.subplots()
        axis.plot(simulated_data[names.index('time')], simulated_data[names.index('x')])
        axis.plot(simulated_data[names.index('time')], [20]*dataLength)
        pyplot.xlabel('time (seconds)')
        pyplot.ylabel('distance (meters)')
        pyplot.show()

    os.chdir('../')

    return [names, simulated_data]

def costFunction(thetaMax, ttask):
    cost = 94 * thetaMax + 71 * ttask
    return cost

maxSwing = 0.174533
setpointDistance = 10
def costSimulation():
    minKp = math.inf
    minkd = math.inf
    minCost = math.inf
    for Kp in range(1, 41):
        for Kd in range(10, 510, 10):
            [names, simulated_data] = testPID(Kp,0 , Kd, False)
            thetaValues = simulated_data[names.index('gantry_system_block.theta')]
            distanceValues = simulated_data[names.index('x')]
            thetaMax = max(map(abs, thetaValues)) * 180.0 / math.pi # in degrees
            worstAngleTime = math.inf
            bestDistTime = math.inf
            for i, theta in reversed(list(enumerate(thetaValues))):
                if abs(theta) > maxSwing:
                    worstAngleTime = simulated_data[names.index('time')][i - 1]
                    break
            for i, dist in list(enumerate(distanceValues)):
                if abs(setpointDistance - dist) < 0.1:
                    bestDistTime = simulated_data[names.index('time')][i - 1]
                    break
            ttask = max(worstAngleTime, bestDistTime)

            print(worstAngleTime, ttask)
            cost = costFunction(thetaMax, ttask)
            if cost == math.inf:
                warning("simulation duration is not high enough for the trolley to reach the set-point")
                return
            print(Kp, Kd, ttask, thetaMax, cost, " | minimame cost: ", minCost, minKp, minkd)
            if cost < minCost:
                minKp = Kp
                minkd = Kd
                minCost = cost
                print("New minima!!!!", minCost)
    print("minimame cost: ", minCost, minKp, minkd)
    return minKp, minkd, minCost

# You need scipy package to read MAT-files
from scipy import io
# Reuse this exact function to read MAT-file data.
# matFileName is the name of the MAT-file generated on execution of a Modelica executable
# The output is [names, data] where names is an array of strings which are names of variables, data is an array of values of the associated variable in the same order
def readMat(matFileName):
    dataMat =  io.loadmat(matFileName)
    names = [''] * len(dataMat['name'][0])
    data = [None] * len(names)
    # Check if the matrix of metadatas are transposed.
    if dataMat['Aclass'][3] == 'binTrans':
        # If the matrix of  matadata needs to be transposed, the names nead to be read from each string
        for x in range(len(dataMat['name'])):
            for i in range(len(dataMat['name'][x])):
                if dataMat['name'][x][i] != '\x00':
                    names[i] = names[i] + dataMat['name'][x][i]
        # If the matrix of metadata needs to be transposed, the index of variable trace needs to be read in a transposed fashion
        for i in range(len(names)):
            # If it is a variable, read the whole array
            if (dataMat['dataInfo'][0][i] == 0) or (dataMat['dataInfo'][0][i] == 2):
                data[i] = dataMat['data_2'][dataMat['dataInfo'][1][i]-1]
            # If it is a parameter, read only the first value
            elif dataMat['dataInfo'][0][i] == 1:
                data[i] = dataMat['data_1'][dataMat['dataInfo'][1][i]-1][0]
    else:
        # If the matrix of metadata need not be transposed, the names can be read directly as individual strings
        names = dataMat['name']
        # If the matrix of metadata need not be transposed, the index of variable trace needs to be read directly
        for i in range(len(names)):
            # If it is a variable, read the whole array
            if (dataMat['dataInfo'][i][0] == 0) or (dataMat['dataInfo'][i][0] == 2):
                data[i] = dataMat['data_2'][dataMat['dataInfo'][i][1]-1]
            # If it is a parameter, read only the first value
            elif dataMat['dataInfo'][i][0] == 1:
                data[i] = dataMat['data_1'][dataMat['dataInfo'][i][1]-1][0]
    # Return the names of variables, and their corresponding values
    return [names,data]

# You need matplotlib to plot
from matplotlib import pyplot
# This function plots the data from the simulation.
# xdata is x-axis data
# ydata is corresponding y-axis data
# xLabel is the string label value to be displayed in the plot for the x axis
# yLabel is the string label value to be displayed in the plot for the y axis
def openDataPlot(xdata, ydata, xLabel, yLabel):
    figure, axis = pyplot.subplots()
    axis.plot(xdata, ydata)
    pyplot.xlabel(xLabel)
    pyplot.ylabel(yLabel)
    pyplot.show()

# "function" that calls the single simulation function from shell. In your code, this function call should be in a loop ove the combinations of parameters.
if __name__ == "__main__":
    real_positions_dc = read_csv('calibration_data_d_c.csv', usecols=['index', 'value'])['value'].values
    real_positions_dp = read_csv('calibration_data_d_p.csv', usecols=['index', 'value'])['value'].values
    #
    # testDc(4.79, real_positions_dc)
    # testDp(0.12, real_positions_dp)
    #
    # dc_min = 0
    # result_min = math.inf
    # dc_values = []
    # error_values = []
    # for x in range(0,500):
    #     dc = x/100
    #     test_result = CalibrateDc(dc, real_positions_dc)
    #     dc_values.append(dc)
    #     error_values.append(test_result)
    #     if test_result < result_min:
    #         result_min = test_result
    #         dc_min = dc
    # openDataPlot(dc_values, error_values, 'damping factor for motion of cart', 'Sum of squared errors')
    #
    #
    # dp_min = 0
    # result_min = math.inf
    # dp_values = []
    # error_values = []
    # for x in range(0,500):
    #     dp = x/100
    #     test_result = CalibrateDp(dp, real_positions_dp)
    #     dp_values.append(dp)
    #     error_values.append(test_result)
    #     if test_result < result_min:
    #         result_min = test_result
    #         dp_min = dp
    # openDataPlot(dp_values, error_values, 'Damping factor swinging of pendulum', 'Sum of squared errors')
    #
    # print(dc_min)
    # print(dp_min)

    testPID(1,10,1, True)
    # testPID(10,1,1)
    # testPID(1, 10, 1)
    # testPID(1, 1, 10)

    #costSimulation()



# The follwing function is an alternative way of executing/simulating the Modelica model using the OMPython package. This method is not recommended.
# from OMPython import OMCSessionZMQ, ModelicaSystem
# def singleSimulationOMPython(T_inf=298.15, T0=363.15, h=0.7, A=1.0, m=0.1, c_p=1.2):
#     omc = OMCSessionZMQ()
#     model = ModelicaSystem('example.mo','NewtonCoolingWithTypes')
#     model.buildModel('T')
#     print('Performing simulation: Ambient Temp.:',str(T_inf),
#                                ', Initial Temp.:',str(initTemp),
#                                ', Convection Coeff.:',str(h),
#                                ', Area:',str(A),
#                                ', Mass:',str(m),
#                                ', Specific Heat:',str(Cp))
#
#     model.setSimulationOptions(["stepSize=0.01",
#                                 "tolerance=1e-9",
#                                 "startTime=0",
#                                 "stopTime=10"])
#     model.setParameters(['T_inf='+str(T_inf),
#                          'T0='+str(T0),
#                          'h='+str(h),
#                          'A='+str(A),
#                          'm='+str(m),
#                          'c_p='+str(c_p)])
#     model.simulate()
#     samples = model.getSolutions(["time", "T"])
#     openDataPlot([samples[0]],[samples[1]],'time (seconds)','temperature (C)')

