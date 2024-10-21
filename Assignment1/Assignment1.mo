package Assignment1
  model Gantry_system
    // Variables
    Modelica.Units.SI.Length x "displacement of the trolley/cart expressed in m";
    Modelica.Units.SI.Velocity v "velocity of the trolley/cart expressed in m/s";
    Modelica.Units.SI.Angle theta "Angular displacement of the pendulum w.r.t the trolley expressed in rad";
    Modelica.Units.SI.AngularVelocity w "Angular velocity of the pendulum expressed in rad/s";
    Real u"Control signal to move the trolley and pendulum";
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
    Modelica.Blocks.Interfaces.RealInput input_con annotation(
      Placement(transformation(origin = {-100, 0}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Blocks.Interfaces.RealOutput output_con annotation(
      Placement(transformation(origin = {100, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}})));
  equation
    input_con = u;
    output_con = x;
  annotation(
      Icon(graphics = {Text(origin = {0, -1}, extent = {{-94, 19}, {94, -19}}, textString = "Gantry_system")}));
  end Gantry_system_block;

  block PID_controller_block
    extends Modelica.Blocks.Icons.Block;
  PID_block pID_block annotation(
      Placement(transformation(extent = {{-10, -10}, {10, 10}})));
  Gantry_system_block gantry_system_block annotation(
      Placement(transformation(origin = {50, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Interfaces.RealOutput x annotation(
      Placement(transformation(origin = {100, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Add add(k1 = +1, k2 = -1)  annotation(
      Placement(transformation(origin = {-50, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant setPoint(k = 20)  annotation(
      Placement(transformation(origin = {-84, 6}, extent = {{-10, -10}, {10, 10}})));
  equation
    connect(x, add.u2) annotation(
      Line(points = {{100, 0}, {68, 0}, {68, -20}, {-68, -20}, {-68, -6}, {-62, -6}}, color = {0, 0, 127}));
    connect(add.y, pID_block.e) annotation(
      Line(points = {{-38, 0}, {-9, 0}}, color = {0, 0, 127}));
    connect(pID_block.u, gantry_system_block.input_con) annotation(
      Line(points = {{12, 0}, {38, 0}}, color = {0, 0, 127}));
    connect(gantry_system_block.output_con, x) annotation(
      Line(points = {{62, 0}, {100, 0}}, color = {0, 0, 127}));
  connect(setPoint.y, add.u1) annotation(
      Line(points = {{-72, 6}, {-62, 6}}, color = {0, 0, 127}));
  end PID_controller_block;

  block PID_block
    extends Modelica.Blocks.Icons.Block;
    Modelica.Blocks.Interfaces.RealInput e annotation(
      Placement(transformation(origin = {-100, 0}, extent = {{-20, -20}, {20, 20}}), iconTransformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}})));
    Modelica.Blocks.Interfaces.RealOutput u annotation(
      Placement(transformation(origin = {100, 0}, extent = {{-10, -10}, {10, 10}}), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Add3 add3 annotation(
      Placement(transformation(origin = {60, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Integrator i(k = 1)  annotation(
      Placement(transformation(extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Derivative d(k = 1)  annotation(
      Placement(transformation(origin = {0, -32}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Gain p(k = 1)  annotation(
      Placement(transformation(origin = {0, 30}, extent = {{-10, -10}, {10, 10}})));
  equation
    connect(add3.y, u) annotation(
      Line(points = {{71, 0}, {100, 0}}, color = {0, 0, 127}));
    connect(i.y, add3.u2) annotation(
      Line(points = {{11, 0}, {48, 0}}, color = {0, 0, 127}));
    connect(d.y, add3.u3) annotation(
      Line(points = {{11, -32}, {20, -32}, {20, -8}, {48, -8}}, color = {0, 0, 127}));
  connect(e, p.u) annotation(
      Line(points = {{-100, 0}, {-20, 0}, {-20, 30}, {-12, 30}}, color = {0, 0, 127}));
  connect(p.y, add3.u1) annotation(
      Line(points = {{12, 30}, {20, 30}, {20, 8}, {48, 8}}, color = {0, 0, 127}));
  connect(e, i.u) annotation(
      Line(points = {{-100, 0}, {-12, 0}}, color = {0, 0, 127}));
  connect(e, d.u) annotation(
      Line(points = {{-100, 0}, {-20, 0}, {-20, -32}, {-12, -32}}, color = {0, 0, 127}));
  annotation(
      Icon(graphics = {Text(origin = {-2, 4}, extent = {{67, -37}, {-67, 37}}, textString = "PID")}));
  end PID_block;
  annotation(
    uses(Modelica(version = "4.0.0")));
end Assignment1;