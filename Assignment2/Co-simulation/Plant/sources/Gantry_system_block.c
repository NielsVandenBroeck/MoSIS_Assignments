/* Main Simulation File */

#if defined(__cplusplus)
extern "C" {
#endif

#include "Gantry_system_block_model.h"
#include "simulation/solver/events.h"



/* dummy VARINFO and FILEINFO */
const VAR_INFO dummyVAR_INFO = omc_dummyVarInfo;

int Gantry_system_block_input_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  (data->localData[0]->realVars[10] /* input_con variable */) = data->simulationInfo->inputVars[0];
  
  TRACE_POP
  return 0;
}

int Gantry_system_block_input_function_init(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->inputVars[0] = data->modelData->realVarsData[10].attribute.start;
  
  TRACE_POP
  return 0;
}

int Gantry_system_block_input_function_updateStartValues(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->modelData->realVarsData[10].attribute.start = data->simulationInfo->inputVars[0];
  
  TRACE_POP
  return 0;
}

int Gantry_system_block_inputNames(DATA *data, char ** names){
  TRACE_PUSH

  names[0] = (char *) data->modelData->realVarsData[10].info.name;
  
  TRACE_POP
  return 0;
}

int Gantry_system_block_data_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  TRACE_POP
  return 0;
}

int Gantry_system_block_dataReconciliationInputNames(DATA *data, char ** names){
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int Gantry_system_block_dataReconciliationUnmeasuredVariables(DATA *data, char ** names)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int Gantry_system_block_output_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->outputVars[0] = (data->localData[0]->realVars[11] /* out_angular_disp variable */);
  data->simulationInfo->outputVars[1] = (data->localData[0]->realVars[12] /* output_con variable */);
  
  TRACE_POP
  return 0;
}

int Gantry_system_block_setc_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int Gantry_system_block_setb_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/*
equation index: 11
type: SIMPLE_ASSIGN
$DER.theta = w
*/
void Gantry_system_block_eqFunction_11(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,11};
  (data->localData[0]->realVars[4] /* der(theta) STATE_DER */) = (data->localData[0]->realVars[2] /* w STATE(1) */);
  TRACE_POP
}
/*
equation index: 12
type: SIMPLE_ASSIGN
$DER.x = v
*/
void Gantry_system_block_eqFunction_12(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,12};
  (data->localData[0]->realVars[7] /* der(x) STATE_DER */) = (data->localData[0]->realVars[1] /* v STATE(1) */);
  TRACE_POP
}
/*
equation index: 13
type: SIMPLE_ASSIGN
out_angular_disp = theta
*/
void Gantry_system_block_eqFunction_13(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,13};
  (data->localData[0]->realVars[11] /* out_angular_disp variable */) = (data->localData[0]->realVars[0] /* theta STATE(1,w) */);
  TRACE_POP
}
/*
equation index: 14
type: SIMPLE_ASSIGN
output_con = x
*/
void Gantry_system_block_eqFunction_14(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,14};
  (data->localData[0]->realVars[12] /* output_con variable */) = (data->localData[0]->realVars[3] /* x STATE(1,v) */);
  TRACE_POP
}
/*
equation index: 15
type: SIMPLE_ASSIGN
$cse2 = cos(theta)
*/
void Gantry_system_block_eqFunction_15(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,15};
  (data->localData[0]->realVars[9] /* $cse2 variable */) = cos((data->localData[0]->realVars[0] /* theta STATE(1,w) */));
  TRACE_POP
}
/*
equation index: 16
type: SIMPLE_ASSIGN
$cse1 = sin(theta)
*/
void Gantry_system_block_eqFunction_16(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,16};
  (data->localData[0]->realVars[8] /* $cse1 variable */) = sin((data->localData[0]->realVars[0] /* theta STATE(1,w) */));
  TRACE_POP
}
/*
equation index: 17
type: SIMPLE_ASSIGN
$DER.v = (r * (dc * v + (-m) * (g * $cse2 + r * w ^ 2.0) * $cse1 - input_con) - dp * $cse2 * w) / ((-r) * (M + m * $cse1 ^ 2.0))
*/
void Gantry_system_block_eqFunction_17(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,17};
  modelica_real tmp0;
  modelica_real tmp1;
  tmp0 = (data->localData[0]->realVars[2] /* w STATE(1) */);
  tmp1 = (data->localData[0]->realVars[8] /* $cse1 variable */);
  (data->localData[0]->realVars[5] /* der(v) STATE_DER */) = DIVISION_SIM(((data->simulationInfo->realParameter[5] /* r PARAM */)) * (((data->simulationInfo->realParameter[1] /* dc PARAM */)) * ((data->localData[0]->realVars[1] /* v STATE(1) */)) + ((-(data->simulationInfo->realParameter[4] /* m PARAM */))) * ((((data->simulationInfo->realParameter[3] /* g PARAM */)) * ((data->localData[0]->realVars[9] /* $cse2 variable */)) + ((data->simulationInfo->realParameter[5] /* r PARAM */)) * ((tmp0 * tmp0))) * ((data->localData[0]->realVars[8] /* $cse1 variable */))) - (data->localData[0]->realVars[10] /* input_con variable */)) - (((data->simulationInfo->realParameter[2] /* dp PARAM */)) * (((data->localData[0]->realVars[9] /* $cse2 variable */)) * ((data->localData[0]->realVars[2] /* w STATE(1) */)))),((-(data->simulationInfo->realParameter[5] /* r PARAM */))) * ((data->simulationInfo->realParameter[0] /* M PARAM */) + ((data->simulationInfo->realParameter[4] /* m PARAM */)) * ((tmp1 * tmp1))),"(-r) * (M + m * $cse1 ^ 2.0)",equationIndexes);
  TRACE_POP
}
/*
equation index: 18
type: SIMPLE_ASSIGN
$DER.w = (dp * w * (m + M) + (m * r) ^ 2.0 * $cse1 * $cse2 * w ^ 2.0 + m * r * (g * $cse1 * (m + M) + $cse2 * (input_con - dc * v))) / (r ^ 2.0 * (-m) * (M + m * $cse1 ^ 2.0))
*/
void Gantry_system_block_eqFunction_18(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,18};
  modelica_real tmp2;
  modelica_real tmp3;
  modelica_real tmp4;
  modelica_real tmp5;
  tmp2 = ((data->simulationInfo->realParameter[4] /* m PARAM */)) * ((data->simulationInfo->realParameter[5] /* r PARAM */));
  tmp3 = (data->localData[0]->realVars[2] /* w STATE(1) */);
  tmp4 = (data->simulationInfo->realParameter[5] /* r PARAM */);
  tmp5 = (data->localData[0]->realVars[8] /* $cse1 variable */);
  (data->localData[0]->realVars[6] /* der(w) STATE_DER */) = DIVISION_SIM(((data->simulationInfo->realParameter[2] /* dp PARAM */)) * (((data->localData[0]->realVars[2] /* w STATE(1) */)) * ((data->simulationInfo->realParameter[4] /* m PARAM */) + (data->simulationInfo->realParameter[0] /* M PARAM */))) + ((tmp2 * tmp2)) * (((data->localData[0]->realVars[8] /* $cse1 variable */)) * (((data->localData[0]->realVars[9] /* $cse2 variable */)) * ((tmp3 * tmp3)))) + ((data->simulationInfo->realParameter[4] /* m PARAM */)) * (((data->simulationInfo->realParameter[5] /* r PARAM */)) * (((data->simulationInfo->realParameter[3] /* g PARAM */)) * (((data->localData[0]->realVars[8] /* $cse1 variable */)) * ((data->simulationInfo->realParameter[4] /* m PARAM */) + (data->simulationInfo->realParameter[0] /* M PARAM */))) + ((data->localData[0]->realVars[9] /* $cse2 variable */)) * ((data->localData[0]->realVars[10] /* input_con variable */) - (((data->simulationInfo->realParameter[1] /* dc PARAM */)) * ((data->localData[0]->realVars[1] /* v STATE(1) */)))))),((tmp4 * tmp4)) * (((-(data->simulationInfo->realParameter[4] /* m PARAM */))) * ((data->simulationInfo->realParameter[0] /* M PARAM */) + ((data->simulationInfo->realParameter[4] /* m PARAM */)) * ((tmp5 * tmp5)))),"r ^ 2.0 * (-m) * (M + m * $cse1 ^ 2.0)",equationIndexes);
  TRACE_POP
}

OMC_DISABLE_OPT
int Gantry_system_block_functionDAE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  int equationIndexes[1] = {0};
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_DAE);
#endif

  data->simulationInfo->needToIterate = 0;
  data->simulationInfo->discreteCall = 1;
  Gantry_system_block_functionLocalKnownVars(data, threadData);
  Gantry_system_block_eqFunction_11(data, threadData);

  Gantry_system_block_eqFunction_12(data, threadData);

  Gantry_system_block_eqFunction_13(data, threadData);

  Gantry_system_block_eqFunction_14(data, threadData);

  Gantry_system_block_eqFunction_15(data, threadData);

  Gantry_system_block_eqFunction_16(data, threadData);

  Gantry_system_block_eqFunction_17(data, threadData);

  Gantry_system_block_eqFunction_18(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_DAE);
#endif
  TRACE_POP
  return 0;
}


int Gantry_system_block_functionLocalKnownVars(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/* forwarded equations */
extern void Gantry_system_block_eqFunction_11(DATA* data, threadData_t *threadData);
extern void Gantry_system_block_eqFunction_12(DATA* data, threadData_t *threadData);
extern void Gantry_system_block_eqFunction_15(DATA* data, threadData_t *threadData);
extern void Gantry_system_block_eqFunction_16(DATA* data, threadData_t *threadData);
extern void Gantry_system_block_eqFunction_17(DATA* data, threadData_t *threadData);
extern void Gantry_system_block_eqFunction_18(DATA* data, threadData_t *threadData);

static void functionODE_system0(DATA *data, threadData_t *threadData)
{
  {
    Gantry_system_block_eqFunction_11(data, threadData);
    threadData->lastEquationSolved = 11;
  }
  {
    Gantry_system_block_eqFunction_12(data, threadData);
    threadData->lastEquationSolved = 12;
  }
  {
    Gantry_system_block_eqFunction_15(data, threadData);
    threadData->lastEquationSolved = 15;
  }
  {
    Gantry_system_block_eqFunction_16(data, threadData);
    threadData->lastEquationSolved = 16;
  }
  {
    Gantry_system_block_eqFunction_17(data, threadData);
    threadData->lastEquationSolved = 17;
  }
  {
    Gantry_system_block_eqFunction_18(data, threadData);
    threadData->lastEquationSolved = 18;
  }
}

int Gantry_system_block_functionODE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_FUNCTION_ODE);
#endif

  
  data->simulationInfo->callStatistics.functionODE++;
  
  Gantry_system_block_functionLocalKnownVars(data, threadData);
  functionODE_system0(data, threadData);

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_FUNCTION_ODE);
#endif

  TRACE_POP
  return 0;
}

/* forward the main in the simulation runtime */
extern int _main_SimulationRuntime(int argc, char**argv, DATA *data, threadData_t *threadData);

#include "Gantry_system_block_12jac.h"
#include "Gantry_system_block_13opt.h"

struct OpenModelicaGeneratedFunctionCallbacks Gantry_system_block_callback = {
   NULL,    /* performSimulation */
   NULL,    /* performQSSSimulation */
   NULL,    /* updateContinuousSystem */
   Gantry_system_block_callExternalObjectDestructors,    /* callExternalObjectDestructors */
   NULL,    /* initialNonLinearSystem */
   NULL,    /* initialLinearSystem */
   NULL,    /* initialMixedSystem */
   #if !defined(OMC_NO_STATESELECTION)
   Gantry_system_block_initializeStateSets,
   #else
   NULL,
   #endif    /* initializeStateSets */
   Gantry_system_block_initializeDAEmodeData,
   Gantry_system_block_functionODE,
   Gantry_system_block_functionAlgebraics,
   Gantry_system_block_functionDAE,
   Gantry_system_block_functionLocalKnownVars,
   Gantry_system_block_input_function,
   Gantry_system_block_input_function_init,
   Gantry_system_block_input_function_updateStartValues,
   Gantry_system_block_data_function,
   Gantry_system_block_output_function,
   Gantry_system_block_setc_function,
   Gantry_system_block_setb_function,
   Gantry_system_block_function_storeDelayed,
   Gantry_system_block_function_storeSpatialDistribution,
   Gantry_system_block_function_initSpatialDistribution,
   Gantry_system_block_updateBoundVariableAttributes,
   Gantry_system_block_functionInitialEquations,
   1, /* useHomotopy - 0: local homotopy (equidistant lambda), 1: global homotopy (equidistant lambda), 2: new global homotopy approach (adaptive lambda), 3: new local homotopy approach (adaptive lambda)*/
   NULL,
   Gantry_system_block_functionRemovedInitialEquations,
   Gantry_system_block_updateBoundParameters,
   Gantry_system_block_checkForAsserts,
   Gantry_system_block_function_ZeroCrossingsEquations,
   Gantry_system_block_function_ZeroCrossings,
   Gantry_system_block_function_updateRelations,
   Gantry_system_block_zeroCrossingDescription,
   Gantry_system_block_relationDescription,
   Gantry_system_block_function_initSample,
   Gantry_system_block_INDEX_JAC_A,
   Gantry_system_block_INDEX_JAC_B,
   Gantry_system_block_INDEX_JAC_C,
   Gantry_system_block_INDEX_JAC_D,
   Gantry_system_block_INDEX_JAC_F,
   Gantry_system_block_INDEX_JAC_H,
   Gantry_system_block_initialAnalyticJacobianA,
   Gantry_system_block_initialAnalyticJacobianB,
   Gantry_system_block_initialAnalyticJacobianC,
   Gantry_system_block_initialAnalyticJacobianD,
   Gantry_system_block_initialAnalyticJacobianF,
   Gantry_system_block_initialAnalyticJacobianH,
   Gantry_system_block_functionJacA_column,
   Gantry_system_block_functionJacB_column,
   Gantry_system_block_functionJacC_column,
   Gantry_system_block_functionJacD_column,
   Gantry_system_block_functionJacF_column,
   Gantry_system_block_functionJacH_column,
   Gantry_system_block_linear_model_frame,
   Gantry_system_block_linear_model_datarecovery_frame,
   Gantry_system_block_mayer,
   Gantry_system_block_lagrange,
   Gantry_system_block_pickUpBoundsForInputsInOptimization,
   Gantry_system_block_setInputData,
   Gantry_system_block_getTimeGrid,
   Gantry_system_block_symbolicInlineSystem,
   Gantry_system_block_function_initSynchronous,
   Gantry_system_block_function_updateSynchronous,
   Gantry_system_block_function_equationsSynchronous,
   Gantry_system_block_inputNames,
   Gantry_system_block_dataReconciliationInputNames,
   Gantry_system_block_dataReconciliationUnmeasuredVariables,
   Gantry_system_block_read_simulation_info,
   Gantry_system_block_read_input_fmu,
   NULL,
   NULL,
   -1,
   NULL,
   NULL,
   -1

};

#define _OMC_LIT_RESOURCE_0_name_data "Assignment1"
#define _OMC_LIT_RESOURCE_0_dir_data "/home/steen/Documents/Local projects/MoSIS_Assignments/Assignment1"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_name,11,_OMC_LIT_RESOURCE_0_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir,66,_OMC_LIT_RESOURCE_0_dir_data);

#define _OMC_LIT_RESOURCE_1_name_data "Complex"
#define _OMC_LIT_RESOURCE_1_dir_data "/home/steen/.openmodelica/libraries/Complex 4.0.0+maint.om"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_name,7,_OMC_LIT_RESOURCE_1_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir,58,_OMC_LIT_RESOURCE_1_dir_data);

#define _OMC_LIT_RESOURCE_2_name_data "Modelica"
#define _OMC_LIT_RESOURCE_2_dir_data "/home/steen/.openmodelica/libraries/Modelica 4.0.0+maint.om"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_name,8,_OMC_LIT_RESOURCE_2_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir,59,_OMC_LIT_RESOURCE_2_dir_data);

#define _OMC_LIT_RESOURCE_3_name_data "ModelicaServices"
#define _OMC_LIT_RESOURCE_3_dir_data "/home/steen/.openmodelica/libraries/ModelicaServices 4.0.0+maint.om"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_name,16,_OMC_LIT_RESOURCE_3_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir,67,_OMC_LIT_RESOURCE_3_dir_data);

static const MMC_DEFSTRUCTLIT(_OMC_LIT_RESOURCES,8,MMC_ARRAY_TAG) {MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir)}};
void Gantry_system_block_setupDataStruc(DATA *data, threadData_t *threadData)
{
  assertStreamPrint(threadData,0!=data, "Error while initialize Data");
  threadData->localRoots[LOCAL_ROOT_SIMULATION_DATA] = data;
  data->callback = &Gantry_system_block_callback;
  OpenModelica_updateUriMapping(threadData, MMC_REFSTRUCTLIT(_OMC_LIT_RESOURCES));
  data->modelData->modelName = "Assignment1.Gantry_system_block";
  data->modelData->modelFilePrefix = "Gantry_system_block";
  data->modelData->resultFileName = NULL;
  data->modelData->modelDir = "/home/steen/Documents/Local projects/MoSIS_Assignments/Assignment1";
  data->modelData->modelGUID = "{ca22aa08-1924-4fd8-b452-1a15ca174b79}";
  data->modelData->initXMLData = NULL;
  data->modelData->modelDataXml.infoXMLData = NULL;
  GC_asprintf(&data->modelData->modelDataXml.fileName, "%s/Gantry_system_block_info.json", data->modelData->resourcesDir);
  data->modelData->runTestsuite = 0;
  data->modelData->nStates = 4;
  data->modelData->nVariablesReal = 13;
  data->modelData->nDiscreteReal = 0;
  data->modelData->nVariablesInteger = 0;
  data->modelData->nVariablesBoolean = 0;
  data->modelData->nVariablesString = 0;
  data->modelData->nParametersReal = 6;
  data->modelData->nParametersInteger = 0;
  data->modelData->nParametersBoolean = 0;
  data->modelData->nParametersString = 0;
  data->modelData->nInputVars = 1;
  data->modelData->nOutputVars = 2;
  data->modelData->nAliasReal = 3;
  data->modelData->nAliasInteger = 0;
  data->modelData->nAliasBoolean = 0;
  data->modelData->nAliasString = 0;
  data->modelData->nZeroCrossings = 0;
  data->modelData->nSamples = 0;
  data->modelData->nRelations = 0;
  data->modelData->nMathEvents = 0;
  data->modelData->nExtObjs = 0;
  data->modelData->modelDataXml.modelInfoXmlLength = 0;
  data->modelData->modelDataXml.nFunctions = 0;
  data->modelData->modelDataXml.nProfileBlocks = 0;
  data->modelData->modelDataXml.nEquations = 21;
  data->modelData->nMixedSystems = 0;
  data->modelData->nLinearSystems = 0;
  data->modelData->nNonLinearSystems = 0;
  data->modelData->nStateSets = 0;
  data->modelData->nJacobians = 6;
  data->modelData->nOptimizeConstraints = 0;
  data->modelData->nOptimizeFinalConstraints = 0;
  data->modelData->nDelayExpressions = 0;
  data->modelData->nBaseClocks = 0;
  data->modelData->nSpatialDistributions = 0;
  data->modelData->nSensitivityVars = 0;
  data->modelData->nSensitivityParamVars = 0;
  data->modelData->nSetcVars = 0;
  data->modelData->ndataReconVars = 0;
  data->modelData->nSetbVars = 0;
  data->modelData->nRelatedBoundaryConditions = 0;
  data->modelData->linearizationDumpLanguage = OMC_LINEARIZE_DUMP_LANGUAGE_MODELICA;
}

static int rml_execution_failed()
{
  fflush(NULL);
  fprintf(stderr, "Execution failed!\n");
  fflush(NULL);
  return 1;
}

