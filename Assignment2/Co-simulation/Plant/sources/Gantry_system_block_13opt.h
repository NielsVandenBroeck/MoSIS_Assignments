#if defined(__cplusplus)
  extern "C" {
#endif
  int Gantry_system_block_mayer(DATA* data, modelica_real** res, short*);
  int Gantry_system_block_lagrange(DATA* data, modelica_real** res, short *, short *);
  int Gantry_system_block_pickUpBoundsForInputsInOptimization(DATA* data, modelica_real* min, modelica_real* max, modelica_real*nominal, modelica_boolean *useNominal, char ** name, modelica_real * start, modelica_real * startTimeOpt);
  int Gantry_system_block_setInputData(DATA *data, const modelica_boolean file);
  int Gantry_system_block_getTimeGrid(DATA *data, modelica_integer * nsi, modelica_real**t);
#if defined(__cplusplus)
}
#endif