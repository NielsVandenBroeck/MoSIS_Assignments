#include <string.h>
#include <stdio.h>

#include "fmi3Functions.h"

/* Inquire version numbers of header files */
const char* GetVersion() {
	return CONCAT(FMI_PREFIX, Version);
}

Status SetDebugLogging(Component c, Boolean loggingOn, size_t nCategories, const String categories[]) {
	return OK;
}


Component InstantiateModelExchange(String instanceName, String fmuGUID, String fmuResourceLocation,
									Boolean visible, Boolean loggingOn,
									fmi3InstanceEnvironment instanceEnvironment, fmi3LogMessageCallback logMessage) {
	CBD* cbd = NULL;

	cbd = (CBD*)malloc(sizeof(CBD));
	cbd->componentEnvironment = instanceEnvironment;
	cbd->instanceName = instanceName;
	cbd->guid = fmuGUID;
	cbd->resourceLoction = fmuResourceLocation;
	cbd->visible = visible;
	cbd->loggingOn = loggingOn;

	cbd->cbAllocateMemory = &malloc;
	cbd->cbFreeMemory = &free;

	initialEquations(cbd);
	return (Component) cbd;
}

Component InstantiateCoSimulation(String instanceName, String fmuGUID, String fmuResourceLocation,
									Boolean visible, Boolean loggingOn, Boolean eventModeUsed,
									Boolean earlyReturnAllowed, const ValueReference requiredIntermediateVars[],
									size_t nReqIntVars, fmi3InstanceEnvironment instanceEnvironment,
									fmi3LogMessageCallback logMessage, fmi3IntermediateUpdateCallback intUpdate) {
	return InstantiateModelExchange(instanceName, fmuGUID, fmuResourceLocation, visible, loggingOn,
									instanceEnvironment, logMessage);
}

void FreeInstance(Component c) {
	CBD* cbd = (CBD*) c;
	if(!cbd) return;

	cbd->cbFreeMemory(cbd);
}


/* Enter and exit initialization mode, terminate and reset */
Status SetupExperiment(Component c, Boolean toleranceDefined, Real tolerance,
								Real startTime, Boolean stopTimeDefined, Real stopTime) {
	CBD* cbd = (CBD*) c;
	cbd->time = startTime;
	cbd->time_last = startTime;
	return OK;
}

Status EnterInitializationMode(Component c, Boolean tolDef, Real tol, Real start, Boolean stopDef, Real stop) {
	CBD* cbd = (CBD*) c;
	return OK;
}

Status ExitInitializationMode(Component c) {
	CBD* cbd = (CBD*) c;

	// Currently only Model Exchange mode
	cbd->isNewEventIteration = False;

	return OK;
}

Status Terminate(Component c) {
	return OK;
}

Status Reset(Component c) {
	CBD* cbd = (CBD*) c;
	initialEquations(cbd);
	return OK;
}


/* Getting and setting variable values */
Status GetReal(Component c, const ValueReference vr[], size_t nvr, Real value[], size_t nValues) {
	CBD* cbd = (CBD*) c;
	calculateEquations(cbd);
	for(int i = 0; i < nvr; ++i) {
		value[i] = cbd->modelData[vr[i]];
	}
	return OK;
}

Status GetBoolean(Component c, const ValueReference vr[], size_t nvr, Boolean value[], size_t nValues) {
	// Booleans are implicitly converted to numbers in the CBD sim.
	return Error;
}

Status GetString(Component c, const ValueReference vr[], size_t nvr, String value[], size_t nValues) {
	// Strings can/should not be used as signals in CBDs!
	return Error;
}

Status SetReal(Component c, const ValueReference vr[], size_t nvr, const Real value[], size_t nValues) {
	CBD* cbd = (CBD*) c;
	for(int i = 0; i < nvr; ++i) {
		cbd->modelData[vr[i]] = value[i];
	}
	return OK;
}

Status SetInteger(Component c, const ValueReference vr[], size_t nvr, const Integer value[], size_t nValues) {
	// Integers are implicitly converted to numbers in the CBD sim.
	return Error;
}

Status SetBoolean(Component c, const ValueReference vr[], size_t nvr, const Boolean value[], size_t nValues) {
	// Booleans are implicitly converted to numbers in the CBD sim.
	return Error;
}

Status SetString(Component c, const ValueReference vr[], size_t nvr, const String  value[], size_t nValues) {
	// Strings can/should not be used as signals in CBDs!
	return Error;
}


/* Getting and setting the internal FMU state */
Status GetFMUstate(Component c, FMUstate* fmu_state) {
	CBD* cbd = (CBD*) c;
	Real data[M];
	for(int i = 0; i < M; ++i) {
		data[i] = cbd->modelData[i];
	}
	*fmu_state = data;
	return OK;
}

Status SetFMUstate(Component c, FMUstate fmu_state) {
	CBD* cbd = (CBD*) c;
	for(int i = 0; i < M; ++i) {
		cbd->modelData[i] = *(((Real*) fmu_state) + i);
	}
	return OK;
}

Status FreeFMUstate(Component c, FMUstate* fmu_state){
	CBD* cbd = (CBD*) c;
	cbd->cbFreeMemory(fmu_state);
	fmu_state = NULL;
	return OK;
}

Status SerializedFMUstateSize(Component c, FMUstate fmu_state, size_t* size) {
	*size = M * sizeof(Real);
	return OK;
}

Status SerializeFMUstate(Component c, FMUstate fmu_state, Byte serializedState[], size_t size) {
	// Not implemented yet
	return Error;
}

Status DeSerializeFMUstate(Component c, const Byte serializedState[], size_t size, FMUstate* fmu_state) {
	// Not implemented yet
	return Error;
}

/* Getting partial derivatives */
Status GetDirectionalDerivative(Component c, const ValueReference vUnknown_ref[], size_t nUnknown,
											const ValueReference vKnown_ref[], size_t nKnown,
											const Real seed[], size_t nSeed,
											Real sensitivity[], size_t nSensitivity) {
	// Not implemented/supported
	return Error;
}


/***************************************************
Types for Functions for FMI for Model Exchange
****************************************************/

typedef enum {
    fmi3EventFalse,
    fmi3EventTrue,
    fmi3EventUnknown
} fmi3EventQualifier;

/* Enter and exit the different modes */
Status EnterEventMode(Component c, fmi3EventQualifier stepEvent, fmi3EventQualifier stateEvent,
						const fmi3Int32 rootsFound[], size_t nEventIndicators, fmi3EventQualifier timeEvent) {
	CBD* cbd = (CBD*) c;
	cbd->isNewEventIteration = True;
	return OK;
}

Status NewDiscreteStates(Component c, Boolean* discreteStatesNeedUpdate, Boolean* terminateSimulation,
							Boolean* nominalsOfContinuousStatesChanged, Boolean* valuesOfContinuousStatesChanged,
							Boolean* nextEventTimeDefined, Real* nextEventTime) {
	CBD* cbd = (CBD*) c;
	cbd->newDiscreteStatesNeeded = False;
	cbd->terminateSimulation = False;
	cbd->nominalsOfContinuousStatesChanged = False;
	cbd->valuesOfContinuousStatesChanged = False;

	stateEvent(cbd);
	cbd->isNewEventIteration = False;

	// Update event information
	discreteStatesNeedUpdate = &cbd->newDiscreteStatesNeeded;
	terminateSimulation = &cbd->terminateSimulation;
	nominalsOfContinuousStatesChanged = &cbd->nominalsOfContinuousStatesChanged;
	valuesOfContinuousStatesChanged = &cbd->valuesOfContinuousStatesChanged;
	nextEventTimeDefined = &cbd->nextEventTimeDefined;
	nextEventTime = &cbd->nextEventTime;

	return OK;
}

Status EnterContinuousTimeMode(Component c) {
	CBD* cbd = (CBD*) c;
	return OK;
}

Status CompletedIntegratorStep(Component c, Boolean noSetFMUStatePriorToCurrentPoint, Boolean* enterEventMode,
										Boolean* terminateSimulation) {
	CBD* cbd = (CBD*) c;
	*enterEventMode = False;
	*terminateSimulation = False;
	return OK;
}

/* Providing independent variables and re-initialization of caching */
Status SetTime(Component c, Real time) {
	CBD* cbd = (CBD*) c;
	cbd->time = time;
	return OK;
}

Status SetContinuousStates(Component c, const Real x[], size_t nx) {
	CBD* cbd = (CBD*) c;
	setContinuousStates(cbd, x, nx);
	cbd->valuesOfContinuousStatesChanged = True;
	return OK;
}

/* Evaluation of the model equations */
Status GetDerivatives(Component c, Real derivatives[], size_t nx) {
	CBD* cbd = (CBD*) c;
	getDerivatives(cbd, derivatives, nx);
	return OK;
}

Status GetEventIndicators(Component c, Real eventIndicators[], size_t ni) {
	// State Event Location w.r.t. 0
	return OK;
}

Status GetContinuousStates(Component c, Real x[], size_t nx) {
	CBD* cbd = (CBD*) c;
	getContinuousStates(cbd, x, nx);
	return OK;
}

Status GetNominalsOfContinuousStates(Component c, Real x_nominal[], size_t nx) {
	for(int i = 0; i < nx; ++i) {
		x_nominal[i] = 1;
	}
	return OK;
}


/***************************************************
Types for Functions for FMI for Co-Simulation
****************************************************/

/* Simulating the slave */
Status SetRealInputDerivatives(Component c, const ValueReference vr[], size_t nvr,
										const Integer order[], const Real value[]) {
	// Cannot interpolate inputs
	return Error;
}

Status GetRealOutputDerivatives(Component c, const ValueReference vr[], size_t nvr,
										const Integer order[], Real value[]) {
	for(int i = 0; i < nvr; ++i) {
		value[i] = 0;
	}
	// Cannot compute output derivatives
	return Error;
}

Status DoStep(Component c, Real currentCommunicationPoint, Real communicationStepSize,
						Boolean noSetFMUStatePriorToCurrentPoint, Boolean* eventHandlingNeeded,
						Boolean* terminateSimulation, Boolean* earlyReturn, Real* lastSuccessfulTime) {
	CBD* cbd = (CBD*) c;
	if (communicationStepSize <= 0) {
		return Error;
	}
	return doStep(cbd, currentCommunicationPoint, currentCommunicationPoint + communicationStepSize);
}

Status CancelStep(Component c) {
	// Cannot cancel step
	return Error;
}
