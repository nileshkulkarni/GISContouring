function Z = GdtWfm()
  
  google_data_file = input('Enter the path of data file:','string');
  
  M = read(google_data_file,-1,3);
  
  x = M(:,1);
  y = M(:,2);
  in = find(x(1)==x);
  n = in(2)-1;
//  disp('n'); disp(n);
  X = x(1:n);
//  disp('X'); disp(X);
  Y = [];
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
      Z(j,i) = z(k);
    end
    //      disp(size(z,1));
    //      disp(i); disp(j); disp(Z(i,j));
  end
  //  disp(Z);
  //  disp(z);
  save_wireframe_map_file = input("Enter the path of the wireframe map jpeg file to be created: ","string");
  a = gca();
  a.cube_scaling = "on";
  plot3d(X,Y,Z);
  
  xs2jpg(gcf(),save_wireframe_map_file);
  
endfunction