package Assignment1
  model Gantry_system
    // Variables
    Modelica.Units.SI.Length x "displacement of the trolley/cart expressed in m";
    Modelica.Units.SI.Velocity v "velocity of the trolley/cart expressed in m/s";
    Modelica.Units.SI.Angle theta "Angular displacement of the pendulum w.r.t the trolley expressed in rad";
    Modelica.Units.SI.AngularVelocity w "Angular velocity of the pendulum expressed in rad/s";
    Real u "Control signal to move the trolley and pendulum";
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2 "Mass of pendulum bob/container expressed in kg";
    parameter Modelica.Units.SI.Mass M = 10 "Mass of trolley/cart expressed in kg";
    parameter Modelica.Units.SI.Length r = 1 "Length of the rope connecting the pendulum bob to the trolley expressed in m";
    parameter Modelica.Units.SI.Damping dp = 0.12 "Damping factor swinging of pendulum expressed in s-1";
    parameter Modelica.Units.SI.Damping dc = 4.79 "Damping factor for motion of cart expressed in m/s^2";
    parameter Modelica.Units.SI.Acceleration g = Modelica.Constants.g_n;
    // Initial values for the variables
  initial equation
    x = 0;
    v = 0;
    theta = 0;
    w = 0;
  equation
    if time < 0.5 then
      u = 1000;
    else
      u = 0;
    end if;
    der(x) = v;
    der(theta) = w;
    der(v) = (r*(dc*v - m*(g*sin(theta)*cos(theta) + r*sin(theta)*w^2) - u) - (dp*cos(theta)*w))/(-r*(M + m*(sin(theta))^2));
    der(w) = ((dp*w*(m + M)) + (m^2*r^2*sin(theta)*cos(theta)*w^2) + m*r*((g*sin(theta)*(m + M)) + (cos(theta)*(u - dc*v))))/((m*r^2)*(-M - (m*sin(theta)^2)));
  end Gantry_system;

  model Trolley_movement
    // Variables
    Modelica.Units.SI.Length x "displacement of the trolley/cart expressed in m";
    Modelica.Units.SI.Velocity v "velocity of the trolley/cart expressed in m/s";
    // Parameters
    parameter Modelica.Units.SI.Mass M = 10 "Mass of trolley/cart expressed in kg";
    parameter Modelica.Units.SI.Damping dc = 0 "Damping factor for motion of cart expressed in s-1";
    // Initial values for the variables
  initial equation
    x = 0;
    v = 5;
  equation
    der(x) = v;
    der(v) = -(dc*v)/(M);
  end Trolley_movement;

  model Pendulum_swinging_motion
    // Variables
    Modelica.Units.SI.Angle theta "Angular displacement of the pendulum w.r.t the trolley expressed in rad";
    Modelica.Units.SI.AngularVelocity w "Angular velocity of the pendulum expressed in rad/s";
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2 "Mass of pendulum bob/container expressed in kg";
    parameter Modelica.Units.SI.Length r = 1 "Length of the rope connecting the pendulum bob to the trolley expressed in m";
    parameter Modelica.Units.SI.Damping dp = 0 "Damping factor swinging of pendulum expressed in s-1";
    parameter Modelica.Units.SI.Acceleration g = Modelica.Constants.g_n;
    // Initial values for the variables
  initial equation
    w = 0;
    theta = Modelica.Units.Conversions.from_deg(30);
  equation
    der(theta) = w;
    der(w) = -((dp*w) + (m*g*r*sin(theta)))/(m*(r^2));
  end Pendulum_swinging_motion;

  block Gantry_system_block
    extends Gantry_system;
    extends Modelica.Blocks.Icons.Block;
  //Modelica.Blocks.Interfaces.RealInput u_input "Input signal connector";
    //Modelica.Blocks.Interfaces.RealOutput x_output "Output signal connector";
    Modelica.Blocks.Interfaces.RealInput input_con annotation(
      Placement(transformation(origin = {-100, 0}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-94, -2}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealOutput output_con annotation(
      Placement(transformation(origin = {100, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {78, 0}, extent = {{-10, -10}, {10, 10}})));
  equation
    input_con = u;
    output_con = x;
  end Gantry_system_block;

  block PID_controller_block
    extends Modelica.Blocks.Icons.Block;
  PID_block pID_block annotation(
      Placement(transformation(origin = {20, 0}, extent = {{-10, -10}, {10, 10}})));
  Gantry_system_block gantry_system_block annotation(
      Placement(transformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealInput r annotation(
      Placement(transformation(origin = {-100, 0}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-94, -2}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealOutput x annotation(
      Placement(transformation(origin = {98, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {88, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Add add annotation(
      Placement(transformation(origin = {-50, 0}, extent = {{-10, -10}, {10, 10}})));
  equation
  connect(pID_block.u, gantry_system_block.input_con) annotation(
      Line(points = {{29, 0}, {34, 0}, {34, -0.2}, {47, -0.2}}, color = {0, 0, 127}));
  connect(gantry_system_block.output_con, x) annotation(
      Line(points = {{64, 0}, {98, 0}}, color = {0, 0, 127}));
  connect(r, add.u1) annotation(
      Line(points = {{-100, 0}, {-74, 0}, {-74, 6}, {-62, 6}}, color = {0, 0, 127}));
  connect(x, add.u2) annotation(
      Line(points = {{98, 0}, {78, 0}, {78, -40}, {-74, -40}, {-74, -6}, {-62, -6}}, color = {0, 0, 127}));
  connect(add.y, pID_block.e) annotation(
      Line(points = {{-38, 0}, {12, 0}}, color = {0, 0, 127}));
  end PID_controller_block;

  block PID_block
    extends Modelica.Blocks.Icons.Block;
    Modelica.Blocks.Interfaces.RealInput e annotation(
      Placement(transformation(origin = {-100, 0}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-86, 2}, extent = {{-20, -20}, {20, 20}})));
    Modelica.Blocks.Interfaces.RealOutput u annotation(
      Placement(transformation(origin = {100, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {90, -2}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Add3 add3 annotation(
      Placement(transformation(origin = {66, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product p annotation(
      Placement(transformation(origin = {-36, 64}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Integrator i annotation(
      Placement(transformation(origin = {-6, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Derivative d annotation(
      Placement(transformation(origin = {-4, -70}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product p1 annotation(
      Placement(transformation(origin = {-36, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product p11 annotation(
      Placement(transformation(origin = {-36, -70}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant kp annotation(
      Placement(transformation(origin = {-90, 70}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant ki annotation(
      Placement(transformation(origin = {-90, -28}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant kd annotation(
      Placement(transformation(origin = {-90, -76}, extent = {{-10, -10}, {10, 10}})));
  equation
    connect(add3.y, u) annotation(
      Line(points = {{78, 0}, {100, 0}}, color = {0, 0, 127}));
  connect(p.y, add3.u1) annotation(
      Line(points = {{-25, 64}, {20, 64}, {20, 8}, {54, 8}}, color = {0, 0, 127}));
  connect(e, p.u2) annotation(
      Line(points = {{-100, 0}, {-60, 0}, {-60, 58}, {-48, 58}}, color = {0, 0, 127}));
  connect(i.y, add3.u2) annotation(
      Line(points = {{5, 0}, {54, 0}}, color = {0, 0, 127}));
  connect(d.y, add3.u3) annotation(
      Line(points = {{7, -70}, {20, -70}, {20, -8}, {54, -8}}, color = {0, 0, 127}));
  connect(p1.y, i.u) annotation(
      Line(points = {{-25, 0}, {-19, 0}}, color = {0, 0, 127}));
  connect(p11.y, d.u) annotation(
      Line(points = {{-25, -70}, {-16, -70}}, color = {0, 0, 127}));
  connect(p11.u1, e) annotation(
      Line(points = {{-48, -64}, {-60, -64}, {-60, 0}, {-100, 0}}, color = {0, 0, 127}));
  connect(p1.u1, e) annotation(
      Line(points = {{-48, 6}, {-60, 6}, {-60, 0}, {-100, 0}}, color = {0, 0, 127}));
  connect(kp.y, p.u1) annotation(
      Line(points = {{-79, 70}, {-48, 70}}, color = {0, 0, 127}));
  connect(p11.u2, kd.y) annotation(
      Line(points = {{-48, -76}, {-78, -76}}, color = {0, 0, 127}));
  connect(p1.u2, ki.y) annotation(
      Line(points = {{-48, -6}, {-54, -6}, {-54, -28}, {-78, -28}}, color = {0, 0, 127}));
  end PID_block;
  annotation(
    uses(Modelica(version = "4.0.0")));
end Assignment1;