package Assignment1
  model Plant
  
  parameter Modelica.Units.SI.Length x = 0 "displacement of the trolley/cart";
  parameter Modelica.Units.SI.Velocity v = 0 "velocity of the trolley/cart";
  parameter Modelica.Units.SI.Angle theta = 0 "Angular displacement of the pendulum w.r.t the trolley";
  parameter Modelica.Units.SI.AngularVelocity w = 0 "Angular velocity of the pendulum";
  parameter Real u = 0 "Control signal to move the trolley and pendulum";
  parameter Modelica.Units.SI.Mass m = 0 "Mass of pendulum bob/container";
  parameter Modelica.Units.SI.Mass M = 0 "Mass of trolley/cart";
  parameter Modelica.Units.SI.Length r = 0 "Length of the rope connecting the pendulum bob to the trolley";
  parameter Modelica.Units.SI.Damping dp = 0 "Damping factor swinging of pendulum";
  parameter Modelica.Units.SI.Damping dc = 0 "Damping factor for motion of cart";

  
  equation

  end Plant;
end Assignment1;