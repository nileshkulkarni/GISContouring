function [X,Y,Z] = GridKriging(x,y,varargin)
  
  N = size(x,1);
  
  if(argn(2)~=2)
    cols = varargin(1);
    rows = varargin(2);
  else
    cols = input("Number of column lines for gridding:");
    rows = input("Number of row lines for gridding:");
  end
  
//  mprintf("Should the min and max values of col and row lines be determined from input vectors x and y OR you wish to input them seperately:");
//  s = input("Y(determine from x,y) or N(ask for seperate input)","string");
//  if(s=="Y" | s=="y")
//    disp(s);
    col_min = min(x(:,1)); //disp(col_min,"col_min");
    col_max = max(x(:,1)); //disp(col_max,"col_max");
    row_min = min(x(:,2)); //disp(row_min,"row_min");
    row_max = max(x(:,2)); //disp(row_max,"row_max");
//  else
//    disp(s);
//    mprintf("\n Enter the details of the required grid:");
//    col_min = input("\n Min value of a col. line:");
//    col_max = input("\n Max value of a col. line:");
//    row_min = input("\n Min value of a row line:");
//    row_max = input("\n Max value of a row line:");
//  end
  
  v_emp = Variogram(x,y);
  v_model = LSPolyFit(v_emp(:,1),v_emp(:,2),1);
  
  c = coeff(v_model);

  for i = 1:1:N
    for j = i:1:N
      K(i,j) = -(c(1) + c(2)*norm(x(i,:)-x(j,:)));
      K(j,i) = K(i,j);
    end
  end
  
  K(N+1,:) = 1;
  K(:,N+1) = 1;
  K(N+1,N+1) = 0;
  
  k = [y;0];
  
  eta = K\k;
//  disp("eta"); disp(eta);
    
  col_interval = (col_max-col_min)/cols;
  row_interval = (row_max-row_min)/rows;
//  disp(col_interval,"col_interval");
//  disp(row_interval,"row_interval");
  for i = 1:1:cols
    X(i) = col_min + (i-1)*col_interval;
  end
  for i = 1:1:rows
    Y(i) = row_min + (i-1)*row_interval;
  end
  
  for i = 1:1:cols
    for j = 1:1:rows
      dist_vec = [X(i)-x(:,1),Y(j)-x(:,2)];
      for s = 1:1:N
        norm_vec(s) = norm(dist_vec(s,:));
      end
//      disp("norm_vec"); disp(norm_vec);
      Vario = c(1) + c(2)*norm_vec;
      Vario = [-Vario; 1];
//      disp("Vario"); disp(Vario);
      Z(j,i) = eta'*Vario;
    end
  end
  
endfunction