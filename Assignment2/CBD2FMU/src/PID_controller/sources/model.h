/*
 *  Main model file; contains the generated CBD model.
 */
#if FMI_VERSION > 2
#include "fmi3PlatformTypes.h"
#include "fmi3FunctionTypes.h"
#else
#include "fmi2TypesPlatform.h"
#include "fmi2FunctionTypes.h"
#endif


#define M 63     /* No of Variables */

// Variable References in-memory
#define _PID_controller_IN (cbd->modelData[0])
#define _PID_controller_OUT (cbd->modelData[1])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_93_OUT1 (cbd->modelData[2])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_95_OUT1 (cbd->modelData[3])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_97_OUT1 (cbd->modelData[4])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_105_OUT1 (cbd->modelData[5])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_108_IN1 (cbd->modelData[6])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_108_OUT1 (cbd->modelData[7])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_111_IN1 (cbd->modelData[8])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_111_IN2 (cbd->modelData[9])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_111_OUT1 (cbd->modelData[10])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_121_IN1 (cbd->modelData[11])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_121_IN2 (cbd->modelData[12])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_121_OUT1 (cbd->modelData[13])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_125_IN1 (cbd->modelData[14])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_125_IN2 (cbd->modelData[15])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_125_OUT1 (cbd->modelData[16])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_129_IN1 (cbd->modelData[17])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_129_IN2 (cbd->modelData[18])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_129_OUT1 (cbd->modelData[19])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_135_IN1 (cbd->modelData[20])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_135_IN2 (cbd->modelData[21])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_135_OUT1 (cbd->modelData[22])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_145_IN1 (cbd->modelData[23])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_145_IN2 (cbd->modelData[24])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_145_OUT1 (cbd->modelData[25])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_158_OUT1 (cbd->modelData[26])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_delta_t_OUT1 (cbd->modelData[27])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_multIc_IN1 (cbd->modelData[28])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_multIc_IN2 (cbd->modelData[29])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_multIc_OUT1 (cbd->modelData[30])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_neg1_IN1 (cbd->modelData[31])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_neg1_OUT1 (cbd->modelData[32])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_sum1_IN1 (cbd->modelData[33])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_sum1_IN2 (cbd->modelData[34])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_sum1_OUT1 (cbd->modelData[35])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_delay_IN1 (cbd->modelData[36])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_delay_IC (cbd->modelData[37])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_delay_OUT1 (cbd->modelData[38])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_neg2_IN1 (cbd->modelData[39])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_neg2_OUT1 (cbd->modelData[40])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_sum2_IN1 (cbd->modelData[41])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_sum2_IN2 (cbd->modelData[42])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_sum2_OUT1 (cbd->modelData[43])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_mult_IN1 (cbd->modelData[44])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_mult_IN2 (cbd->modelData[45])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_mult_OUT1 (cbd->modelData[46])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_inv_IN1 (cbd->modelData[47])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_117_inv_OUT1 (cbd->modelData[48])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_zero_OUT1 (cbd->modelData[49])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delta_t_OUT1 (cbd->modelData[50])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delayIn_IN1 (cbd->modelData[51])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delayIn_IC (cbd->modelData[52])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delayIn_OUT1 (cbd->modelData[53])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_multDelta_IN1 (cbd->modelData[54])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_multDelta_IN2 (cbd->modelData[55])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_multDelta_OUT1 (cbd->modelData[56])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delayState_IN1 (cbd->modelData[57])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delayState_IC (cbd->modelData[58])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_delayState_OUT1 (cbd->modelData[59])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_sumState_IN1 (cbd->modelData[60])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_sumState_IN2 (cbd->modelData[61])
#define _PID_controller_xFvxAx3d5TRpq_XM0aEQ_140_sumState_OUT1 (cbd->modelData[62])

#if FMI_VERSION > 2
typedef void* (*AllocateMemoryFnc)(size_t);
#else
typedef void* (*AllocateMemoryFnc)(size_t nobj, size_t size);
#endif
typedef void (*FreeMemoryFnc)(void*);

typedef struct {
	Real time;
	Real time_last;

	String instanceName;
//	Type type;
	String guid;
	String resourceLoction;
	Boolean visible;
	Boolean loggingOn;

	AllocateMemoryFnc cbAllocateMemory;
	FreeMemoryFnc cbFreeMemory;

	Real modelData[M];
	ComponentEnvironment componentEnvironment;

	// event info
	Boolean newDiscreteStatesNeeded;
	Boolean terminateSimulation;
	Boolean nominalsOfContinuousStatesChanged;
	Boolean valuesOfContinuousStatesChanged;
	Boolean nextEventTimeDefined;
	Real nextEventTime;

	Boolean isNewEventIteration;

} CBD;

void initialEquations(CBD* cbd);
void calculateEquations(CBD* cbd);

Status doStep(CBD* cbd, double t, double tNext);

void stateEvent(CBD* cbd);
void getContinuousStates(CBD* cbd, double x[], size_t nx);
void setContinuousStates(CBD* cbd, const double x[], size_t nx);
void getDerivatives(CBD* cbd, double dx[], size_t nx);
void getStateEvents(CBD* cbd, double z[], size_t nz);