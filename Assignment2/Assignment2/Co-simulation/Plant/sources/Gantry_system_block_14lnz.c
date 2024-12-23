/* Linearization */
#include "Gantry_system_block_model.h"
#if defined(__cplusplus)
extern "C" {
#endif
const char *Gantry_system_block_linear_model_frame()
{
  return "model linearized_model \"Gantry_system_block\"\n"
  "  parameter Integer n = 4 \"number of states\";\n"
  "  parameter Integer m = 1 \"number of inputs\";\n"
  "  parameter Integer p = 2 \"number of outputs\";\n"
  "  parameter Real x0[n] = %s;\n"
  "  parameter Real u0[m] = %s;\n"
  "\n"
  "  parameter Real A[n, n] =\n\t[%s];\n\n"
  "  parameter Real B[n, m] =\n\t[%s];\n\n"
  "  parameter Real C[p, n] =\n\t[%s];\n\n"
  "  parameter Real D[p, m] =\n\t[%s];\n\n"
  "\n"
  "  Real x[n](start=x0);\n"
  "  input Real u[m](start=u0);\n"
  "  output Real y[p];\n"
  "\n"
  "  Real 'x_theta' = x[1];\n"
  "  Real 'x_v' = x[2];\n"
  "  Real 'x_w' = x[3];\n"
  "  Real 'x_x' = x[4];\n"
  "  Real 'u_input_con' = u[1];\n"
  "  Real 'y_out_angular_disp' = y[1];\n"
  "  Real 'y_output_con' = y[2];\n"
  "equation\n"
  "  der(x) = A * x + B * u;\n"
  "  y = C * x + D * u;\n"
  "end linearized_model;\n";
}
const char *Gantry_system_block_linear_model_datarecovery_frame()
{
  return "model linearized_model \"Gantry_system_block\"\n"
  "  parameter Integer n = 4 \"number of states\";\n"
  "  parameter Integer m = 1 \"number of inputs\";\n"
  "  parameter Integer p = 2 \"number of outputs\";\n"
  "  parameter Integer nz = 5 \"data recovery variables\";\n"
  "  parameter Real x0[4] = %s;\n"
  "  parameter Real u0[1] = %s;\n"
  "  parameter Real z0[5] = %s;\n"
  "\n"
  "  parameter Real A[n, n] =\n\t[%s];\n\n"
  "  parameter Real B[n, m] =\n\t[%s];\n\n"
  "  parameter Real C[p, n] =\n\t[%s];\n\n"
  "  parameter Real D[p, m] =\n\t[%s];\n\n"
  "  parameter Real Cz[nz, n] =\n\t[%s];\n\n"
  "  parameter Real Dz[nz, m] =\n\t[%s];\n\n"
  "\n"
  "  Real x[n](start=x0);\n"
  "  input Real u[m](start=u0);\n"
  "  output Real y[p];\n"
  "  output Real z[nz];\n"
  "\n"
  "  Real 'x_theta' = x[1];\n"
  "  Real 'x_v' = x[2];\n"
  "  Real 'x_w' = x[3];\n"
  "  Real 'x_x' = x[4];\n"
  "  Real 'u_input_con' = u[1];\n"
  "  Real 'y_out_angular_disp' = y[1];\n"
  "  Real 'y_output_con' = y[2];\n"
  "  Real 'z_$cse1' = z[1];\n"
  "  Real 'z_$cse2' = z[2];\n"
  "  Real 'z_input_con' = z[3];\n"
  "  Real 'z_out_angular_disp' = z[4];\n"
  "  Real 'z_output_con' = z[5];\n"
  "equation\n"
  "  der(x) = A * x + B * u;\n"
  "  y = C * x + D * u;\n"
  "  z = Cz * x + Dz * u;\n"
  "end linearized_model;\n";
}
#if defined(__cplusplus)
}
#endif

