/* update bound parameters and variable attributes (start, nominal, min, max) */
#include "Gantry_system_block_model.h"
#if defined(__cplusplus)
extern "C" {
#endif

OMC_DISABLE_OPT
int Gantry_system_block_updateBoundVariableAttributes(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  /* min ******************************************************** */
  infoStreamPrint(LOG_INIT, 1, "updating min-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* max ******************************************************** */
  infoStreamPrint(LOG_INIT, 1, "updating max-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* nominal **************************************************** */
  infoStreamPrint(LOG_INIT, 1, "updating nominal-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* start ****************************************************** */
  infoStreamPrint(LOG_INIT, 1, "updating primary start-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  TRACE_POP
  return 0;
}

void Gantry_system_block_updateBoundParameters_0(DATA *data, threadData_t *threadData);

/*
equation index: 19
type: ALGORITHM

  assert(M >= 0.0, "Variable violating min constraint: 0.0 <= M, has value: " + String(M, "g"));
*/
OMC_DISABLE_OPT
static void Gantry_system_block_eqFunction_19(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,19};
  modelica_boolean tmp0;
  static const MMC_DEFSTRINGLIT(tmp1,56,"Variable violating min constraint: 0.0 <= M, has value: ");
  modelica_string tmp2;
  modelica_metatype tmpMeta3;
  static int tmp4 = 0;
  if(!tmp4)
  {
    tmp0 = GreaterEq((data->simulationInfo->realParameter[0] /* M PARAM */),0.0);
    if(!tmp0)
    {
      tmp2 = modelica_real_to_modelica_string_format((data->simulationInfo->realParameter[0] /* M PARAM */), (modelica_string) mmc_strings_len1[103]);
      tmpMeta3 = stringAppend(MMC_REFSTRINGLIT(tmp1),tmp2);
      {
        const char* assert_cond = "(M >= 0.0)";
        if (data->simulationInfo->noThrowAsserts) {
          FILE_INFO info = {"/home/steen/Documents/Local projects/MoSIS_Assignments/Assignment1/Assignment1.mo",12,5,12,83,0};
          infoStreamPrintWithEquationIndexes(LOG_ASSERT, info, 0, equationIndexes, "The following assertion has been violated %sat time %f\n(%s) --> \"%s\"", initial() ? "during initialization " : "", data->localData[0]->timeValue, assert_cond, MMC_STRINGDATA(tmpMeta3));
        } else {
          FILE_INFO info = {"/home/steen/Documents/Local projects/MoSIS_Assignments/Assignment1/Assignment1.mo",12,5,12,83,0};
          omc_assert_warning_withEquationIndexes(info, equationIndexes, "The following assertion has been violated %sat time %f\n(%s) --> \"%s\"", initial() ? "during initialization " : "", data->localData[0]->timeValue, assert_cond, MMC_STRINGDATA(tmpMeta3));
        }
      }
      tmp4 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 20
type: ALGORITHM

  assert(m >= 0.0, "Variable violating min constraint: 0.0 <= m, has value: " + String(m, "g"));
*/
OMC_DISABLE_OPT
static void Gantry_system_block_eqFunction_20(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,20};
  modelica_boolean tmp5;
  static const MMC_DEFSTRINGLIT(tmp6,56,"Variable violating min constraint: 0.0 <= m, has value: ");
  modelica_string tmp7;
  modelica_metatype tmpMeta8;
  static int tmp9 = 0;
  if(!tmp9)
  {
    tmp5 = GreaterEq((data->simulationInfo->realParameter[4] /* m PARAM */),0.0);
    if(!tmp5)
    {
      tmp7 = modelica_real_to_modelica_string_format((data->simulationInfo->realParameter[4] /* m PARAM */), (modelica_string) mmc_strings_len1[103]);
      tmpMeta8 = stringAppend(MMC_REFSTRINGLIT(tmp6),tmp7);
      {
        const char* assert_cond = "(m >= 0.0)";
        if (data->simulationInfo->noThrowAsserts) {
          FILE_INFO info = {"/home/steen/Documents/Local projects/MoSIS_Assignments/Assignment1/Assignment1.mo",11,5,11,94,0};
          infoStreamPrintWithEquationIndexes(LOG_ASSERT, info, 0, equationIndexes, "The following assertion has been violated %sat time %f\n(%s) --> \"%s\"", initial() ? "during initialization " : "", data->localData[0]->timeValue, assert_cond, MMC_STRINGDATA(tmpMeta8));
        } else {
          FILE_INFO info = {"/home/steen/Documents/Local projects/MoSIS_Assignments/Assignment1/Assignment1.mo",11,5,11,94,0};
          omc_assert_warning_withEquationIndexes(info, equationIndexes, "The following assertion has been violated %sat time %f\n(%s) --> \"%s\"", initial() ? "during initialization " : "", data->localData[0]->timeValue, assert_cond, MMC_STRINGDATA(tmpMeta8));
        }
      }
      tmp9 = 1;
    }
  }
  TRACE_POP
}
OMC_DISABLE_OPT
void Gantry_system_block_updateBoundParameters_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  Gantry_system_block_eqFunction_19(data, threadData);
  Gantry_system_block_eqFunction_20(data, threadData);
  TRACE_POP
}
OMC_DISABLE_OPT
int Gantry_system_block_updateBoundParameters(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  Gantry_system_block_updateBoundParameters_0(data, threadData);
  TRACE_POP
  return 0;
}

#if defined(__cplusplus)
}
#endif

