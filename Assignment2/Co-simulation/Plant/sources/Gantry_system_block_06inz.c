/* Initialization */
#include "Gantry_system_block_model.h"
#include "Gantry_system_block_11mix.h"
#include "Gantry_system_block_12jac.h"
#if defined(__cplusplus)
extern "C" {
#endif

void Gantry_system_block_functionInitialEquations_0(DATA *data, threadData_t *threadData);

/*
equation index: 1
type: SIMPLE_ASSIGN
w = 0.0
*/
void Gantry_system_block_eqFunction_1(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,1};
  (data->localData[0]->realVars[2] /* w STATE(1) */) = 0.0;
  TRACE_POP
}
extern void Gantry_system_block_eqFunction_11(DATA *data, threadData_t *threadData);


/*
equation index: 3
type: SIMPLE_ASSIGN
theta = 0.0
*/
void Gantry_system_block_eqFunction_3(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,3};
  (data->localData[0]->realVars[0] /* theta STATE(1,w) */) = 0.0;
  TRACE_POP
}
extern void Gantry_system_block_eqFunction_13(DATA *data, threadData_t *threadData);


/*
equation index: 5
type: SIMPLE_ASSIGN
v = 0.0
*/
void Gantry_system_block_eqFunction_5(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,5};
  (data->localData[0]->realVars[1] /* v STATE(1) */) = 0.0;
  TRACE_POP
}
extern void Gantry_system_block_eqFunction_12(DATA *data, threadData_t *threadData);


/*
equation index: 7
type: SIMPLE_ASSIGN
$DER.v = (r * (dc * v + (-m) * (g * cos(theta) + r * w ^ 2.0) * sin(theta) - input_con) - dp * cos(theta) * w) / ((-r) * (M + m * sin(theta) ^ 2.0))
*/
void Gantry_system_block_eqFunction_7(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,7};
  modelica_real tmp0;
  modelica_real tmp1;
  tmp0 = (data->localData[0]->realVars[2] /* w STATE(1) */);
  tmp1 = sin((data->localData[0]->realVars[0] /* theta STATE(1,w) */));
  (data->localData[0]->realVars[5] /* der(v) STATE_DER */) = DIVISION_SIM(((data->simulationInfo->realParameter[5] /* r PARAM */)) * (((data->simulationInfo->realParameter[1] /* dc PARAM */)) * ((data->localData[0]->realVars[1] /* v STATE(1) */)) + ((-(data->simulationInfo->realParameter[4] /* m PARAM */))) * ((((data->simulationInfo->realParameter[3] /* g PARAM */)) * (cos((data->localData[0]->realVars[0] /* theta STATE(1,w) */))) + ((data->simulationInfo->realParameter[5] /* r PARAM */)) * ((tmp0 * tmp0))) * (sin((data->localData[0]->realVars[0] /* theta STATE(1,w) */)))) - (data->localData[0]->realVars[10] /* input_con variable */)) - (((data->simulationInfo->realParameter[2] /* dp PARAM */)) * ((cos((data->localData[0]->realVars[0] /* theta STATE(1,w) */))) * ((data->localData[0]->realVars[2] /* w STATE(1) */)))),((-(data->simulationInfo->realParameter[5] /* r PARAM */))) * ((data->simulationInfo->realParameter[0] /* M PARAM */) + ((data->simulationInfo->realParameter[4] /* m PARAM */)) * ((tmp1 * tmp1))),"(-r) * (M + m * sin(theta) ^ 2.0)",equationIndexes);
  TRACE_POP
}

/*
equation index: 8
type: SIMPLE_ASSIGN
$DER.w = (dp * w * (m + M) + (m * r) ^ 2.0 * sin(theta) * cos(theta) * w ^ 2.0 + m * r * (g * sin(theta) * (m + M) + cos(theta) * (input_con - dc * v))) / (r ^ 2.0 * (-m) * (M + m * sin(theta) ^ 2.0))
*/
void Gantry_system_block_eqFunction_8(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,8};
  modelica_real tmp2;
  modelica_real tmp3;
  modelica_real tmp4;
  modelica_real tmp5;
  tmp2 = ((data->simulationInfo->realParameter[4] /* m PARAM */)) * ((data->simulationInfo->realParameter[5] /* r PARAM */));
  tmp3 = (data->localData[0]->realVars[2] /* w STATE(1) */);
  tmp4 = (data->simulationInfo->realParameter[5] /* r PARAM */);
  tmp5 = sin((data->localData[0]->realVars[0] /* theta STATE(1,w) */));
  (data->localData[0]->realVars[6] /* der(w) STATE_DER */) = DIVISION_SIM(((data->simulationInfo->realParameter[2] /* dp PARAM */)) * (((data->localData[0]->realVars[2] /* w STATE(1) */)) * ((data->simulationInfo->realParameter[4] /* m PARAM */) + (data->simulationInfo->realParameter[0] /* M PARAM */))) + ((tmp2 * tmp2)) * ((sin((data->localData[0]->realVars[0] /* theta STATE(1,w) */))) * ((cos((data->localData[0]->realVars[0] /* theta STATE(1,w) */))) * ((tmp3 * tmp3)))) + ((data->simulationInfo->realParameter[4] /* m PARAM */)) * (((data->simulationInfo->realParameter[5] /* r PARAM */)) * (((data->simulationInfo->realParameter[3] /* g PARAM */)) * ((sin((data->localData[0]->realVars[0] /* theta STATE(1,w) */))) * ((data->simulationInfo->realParameter[4] /* m PARAM */) + (data->simulationInfo->realParameter[0] /* M PARAM */))) + (cos((data->localData[0]->realVars[0] /* theta STATE(1,w) */))) * ((data->localData[0]->realVars[10] /* input_con variable */) - (((data->simulationInfo->realParameter[1] /* dc PARAM */)) * ((data->localData[0]->realVars[1] /* v STATE(1) */)))))),((tmp4 * tmp4)) * (((-(data->simulationInfo->realParameter[4] /* m PARAM */))) * ((data->simulationInfo->realParameter[0] /* M PARAM */) + ((data->simulationInfo->realParameter[4] /* m PARAM */)) * ((tmp5 * tmp5)))),"r ^ 2.0 * (-m) * (M + m * sin(theta) ^ 2.0)",equationIndexes);
  TRACE_POP
}

/*
equation index: 9
type: SIMPLE_ASSIGN
x = 0.0
*/
void Gantry_system_block_eqFunction_9(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,9};
  (data->localData[0]->realVars[3] /* x STATE(1,v) */) = 0.0;
  TRACE_POP
}
extern void Gantry_system_block_eqFunction_14(DATA *data, threadData_t *threadData);

OMC_DISABLE_OPT
void Gantry_system_block_functionInitialEquations_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  Gantry_system_block_eqFunction_1(data, threadData);
  Gantry_system_block_eqFunction_11(data, threadData);
  Gantry_system_block_eqFunction_3(data, threadData);
  Gantry_system_block_eqFunction_13(data, threadData);
  Gantry_system_block_eqFunction_5(data, threadData);
  Gantry_system_block_eqFunction_12(data, threadData);
  Gantry_system_block_eqFunction_7(data, threadData);
  Gantry_system_block_eqFunction_8(data, threadData);
  Gantry_system_block_eqFunction_9(data, threadData);
  Gantry_system_block_eqFunction_14(data, threadData);
  TRACE_POP
}

int Gantry_system_block_functionInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->discreteCall = 1;
  Gantry_system_block_functionInitialEquations_0(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
  TRACE_POP
  return 0;
}

/* No Gantry_system_block_functionInitialEquations_lambda0 function */

int Gantry_system_block_functionRemovedInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int *equationIndexes = NULL;
  double res = 0.0;

  
  TRACE_POP
  return 0;
}


#if defined(__cplusplus)
}
#endif

