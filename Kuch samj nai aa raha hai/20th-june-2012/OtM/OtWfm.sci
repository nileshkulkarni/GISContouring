function [x,y,z] = OtWfm()
  //Observation points data is converted to Wireframe map
  
  obs_data_file = input("Enter the observation data file path: ","string");
  save_wireframe_map_file = input("Enter the path of the wireframe map jpeg file to be created: ","string");
  
  M = read(obs_data_file,-1,3);
  p = M(:,1:2);  //observation points (Lat-Longs)
  q = M(:,3);    //observation values
  
  cols = input("Enter the number of column-lines in the wireframe grid:");
  rows = input("Enter the number of row-lines in the wireframe grid:");
  
  [x,y,z] = GridKriging(p,q,cols,rows);
  
  a = gca();
  a.cube_scaling = "on";
  plot3d(x,y,z);
  
endfunction
