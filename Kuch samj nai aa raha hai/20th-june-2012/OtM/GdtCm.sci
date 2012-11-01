function GdtCm()
  
  google_data_file = input('Enter the path of data file:','string');
  
  M = read(google_data_file,-1,3);
  
  x = M(:,1);
  y = M(:,2);
  in = find(x(1)==x);
  n = in(2)-1;
//  disp('n'); disp(n);
  X = x(1:n);
//  disp('X'); disp(X);
  Y = []
  for i = 1:1:size(y,1)
    if(Y($)==y(i))
      continue;
    else
      Y = [Y; y(i)];
    end
  end
//  disp('size(Y,1)'); disp(size(Y,1));
//  disp('Y'); disp(Y);
  z = M(:,3);
//  disp('size of z'); disp(size(z,1));
  Z = [];
  for i = 1:1:size(Y,1)
    for j = 1:1:n
      k = (i-1)*n + j;
      Z(i,j) = z(k);
    end
    //    disp(size(z,1));
    //    disp(i); disp(j); disp(Z(i,j));
  end
  
//  disp(Z);
  //  disp(z);
  
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
    [xv,yv] = Contour(X,Y,Z,CL(i));
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
  
  X_margin = (X($)-X(1))/11;
  Y_margin = (Y($)-Y(1))/11;
  
  a = gca();
  a.axes_visible = "on";
  a.x_location = "top";
  a.data_bounds = [X(1)-X_margin/2, Y(1)-Y_margin/2; X($)+X_margin/2, Y($)+Y_margin/2];
  a.tight_limits = "on";
  
  save_contour_map_file = input("Enter the path of the contour map jpeg file to be created: ","string");
  
  xsegs(total_xv,total_yv);
  num_str = string(floor(num));
  xstring(num_pos_x,num_pos_y,num_str);
  
  xs2jpg(gcf(),save_contour_map_file);
  
endfunction