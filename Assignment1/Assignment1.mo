package Assignment1
  model Plant
    // Variables
    Modelica.Units.SI.Length x "displacement of the trolley/cart";
    Modelica.Units.SI.Velocity v "velocity of the trolley/cart";
    Modelica.Units.SI.Angle theta "Angular displacement of the pendulum w.r.t the trolley";
    Modelica.Units.SI.AngularVelocity w "Angular velocity of the pendulum";
    
    // idk
    Real u "Control signal to move the trolley and pendulum";
    
    // Parameters
    parameter Modelica.Units.SI.Mass m = 10 "Mass of pendulum bob/container";
    parameter Modelica.Units.SI.Mass M = 100 "Mass of trolley/cart";
    parameter Modelica.Units.SI.Length r = 1 "Length of the rope connecting the pendulum bob to the trolley";
    parameter Modelica.Units.SI.Damping dp = 0.5 "Damping factor swinging of pendulum";
    parameter Modelica.Units.SI.Damping dc = 2 "Damping factor for motion of cart";
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
  der (x) = v;
  der (theta) = w;
  der (v) = (r * (dc * v - m * (g * sin(theta) * cos(theta) + r * sin(theta) * w^2) - u) - (dp * cos(theta) * w))/(-r * (M + m * (sin(theta))^2));
  der (w) = ((dp * w * (m + M)) + (m^2 * r^2 * sin(theta) * cos(theta) * w^2) + m * r * ((g * sin(theta) * (m + M)) + (cos(theta) * (u - dc * v))))/
  ((m * r^2) * (-M - (m * sin(theta)^2)));
  
    end Plant;
end Assignment1;