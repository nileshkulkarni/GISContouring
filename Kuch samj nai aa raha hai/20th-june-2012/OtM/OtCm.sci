function [x,y,z] = OtCm()
  //Observation points data is converted to Contour map
  
  obs_data_file = input("Enter the observation data file path: ","string");
  save_contour_map_file = input("Enter the path of the contour map jpeg file to be created: ","string");
  
  M = read(obs_data_file,-1,3);
  p = M(:,1:2);  //observation points (Lat-Longs)
  q = M(:,3);    //observation values
  
  default_no_of_cols = 25;
  default_no_of_rows = 25;
  
  [x,y,z] = GridKriging(p,q,default_no_of_cols,default_no_of_rows);
//  disp('x'); disp(x); disp('y'); disp(y); disp('z'); disp(z);
//  plot3d(linspace(1,25,25),linspace(1,25,25),grand(25,25,'nor',5,2));
  //plot3d(x,y,grand(25,25,'nor',5,2));//,flag = [0 2 4]);
  
  
  //CL = vector of contouring levels
  s = input("Specific contour levels required? (Y or N):","string");
  if(s=="Y" | s=="y")
    cl_str = input("Enter the row vector of required contour levels:","string");
    cl_str = stripblanks(cl_str);
    CL = strtod(strsplit(cl_str,strindex(cl_str,' ')));
    N = size(CL,1);
  else
    s = input("Specific number of contour levels required(Y or N):","string");
    if(s=="Y" | s=="y")
      N = input("Enter the number of contour level required:");
      CL = linspace(min(z),max(z),N+2);
      CL = CL(2:N+1);
    else
      min_z = min(z);
      max_z = max(z);
      disp("min z is:"); disp(min_z);
      disp("max z is:"); disp(max_z);
      d = input("Enter the level difference at which contours need to be drawn:");
      l = min_z;
      CL = [];
      while(l<max_z)
        CL = [CL; l+d];
        l = l + d;
      end
      N = size(CL,1);
    end
  end
  
  total_xv = [];
  total_yv = [];
  num_pos_x = [];
  num_pos_y = [];
  num = [];
  
  for i = 1:1:N
    [xv,yv] = Contour(x,y,z,CL(i));
    comps = ContourComponents(xv,yv);
    total_xv = [total_xv, xv];
    total_yv = [total_yv, yv];
    
    for j = 1:1:size(comps,1)
      comp_size = size(comps(j).entries,2);
      num_pos_x = [num_pos_x, comps(j).entries(1,ceil(comp_size/2))];
      num_pos_y = [num_pos_y, comps(j).entries(2,ceil(comp_size/2))];
      num = [num, CL(i)];
    end
  end
  
  x_margin = (x($)-x(1))/11;
  y_margin = (y($)-y(1))/11;
  
  a = gca();
  a.axes_visible = "on";
  a.x_location = "top";
  a.data_bounds = [x(1)-x_margin/2, y(1)-y_margin/2; x($)+x_margin/2, y($)+y_margin/2];
  a.tight_limits = "on";
  
  xsegs(total_xv,total_yv);
  num_str = string(floor(num));
  xstring(num_pos_x,num_pos_y,num_str);
  
  xs2jpg(gcf(),save_contour_map_file);
  
endfunction