/* Algebraic */
#include "Gantry_system_block_model.h"

#ifdef __cplusplus
extern "C" {
#endif


/* forwarded equations */
extern void Gantry_system_block_eqFunction_13(DATA* data, threadData_t *threadData);
extern void Gantry_system_block_eqFunction_14(DATA* data, threadData_t *threadData);

static void functionAlg_system0(DATA *data, threadData_t *threadData)
{
  {
    Gantry_system_block_eqFunction_13(data, threadData);
    threadData->lastEquationSolved = 13;
  }
  {
    Gantry_system_block_eqFunction_14(data, threadData);
    threadData->lastEquationSolved = 14;
  }
}
/* for continuous time variables */
int Gantry_system_block_functionAlgebraics(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_ALGEBRAICS);
#endif
  data->simulationInfo->callStatistics.functionAlgebraics++;

  Gantry_system_block_function_savePreSynchronous(data, threadData);
  
  functionAlg_system0(data, threadData);

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_ALGEBRAICS);
#endif

  TRACE_POP
  return 0;
}

#ifdef __cplusplus
}
#endif
