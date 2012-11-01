function [xv,yv] = Contour(x,y,z,z_val)
  //x is nx1, y is mx1, z is mxn
  // x and y in strict increasing order
  //num_x and num_y are positions where level values are to be printed on the contour map  
  //cutting the surface with a blade
  //from left to right at level z_val
  
  //pfz = sufficiently small value
  //to perturb any value in the given data
  //from zero without affecting accuracy
  //of computation
  
  if(min(x) <= 0)
    translate_x = abs(min(x))+1;
  else
    translate_x = 0;
  end
  if(min(y) <= 0)
    translate_y = abs(min(y))+1;
  else
    translate_y = 0;
  end

  
  x = x + translate_x;
  y = y + translate_y;
  //  disp(x,'x');  disp(y,'y');
  
  max_x = max(x);
  max_y = max(y);

  m = size(z,1);
  n = size(z,2);
//  disp(n,'n',m,'m');
  
//  return;
  
  //some temp variables
  X = ones(m,1) * x';
  Y = y * ones(1,n);
  xx = ones(m,1)*(x(2:$)-x(1:$-1))';
  yy = (y(2:$)-y(1:$-1))*ones(1,n);
  zzc = z(2:$,:)-z(1:$-1,:);
  zzr = z(:,2:$)-z(:,1:$-1);
  //avoiding division by zero
//  zzc = zzc + 10^-7;
//  zzr = zzr + 10^-7;
  
//  disp(yy,"yy",xx,"xx",zzr,"zzr",zzc,"zzc");
//  return;
    
  //lepc = linearly extrapoled points
  //having z_val along columns
  //similarly for lepr
  lepc = zeros(m-1,n);
  for i = 1:1:m-1
    for j = 1:1:n
      if(zzc(i,j)~=0)
        lepc(i,j) = Y(i,j) + (z_val-z(i,j))/zzc(i,j)*yy(i,j);
      end
    end
  end

  lepr = zeros(m,n-1);
  for i = 1:1:m
    for j = 1:1:n-1
      if(zzr(i,j)~=0)
        lepr(i,j) = X(i,j) + (z_val-z(i,j))/zzr(i,j)*xx(i,j);
      end
    end
  end
  
  //  disp(lepr,"lepr",lepc,"lepc");
//  return;
  //wrc = boolean matrix
  //representing points of lepc
  //within corresponding range
  //similarly for wrr

  wrc = (lepc>Y(1:$-1,:))&(lepc<Y(2:$,:));
  wrr = (lepr>X(:,1:$-1))&(lepr<X(:,2:$));
  
//  disp(yy,"yy");
//  disp(z,"z");
//  disp(zzc,"zzc");
//  disp(lepc,"lepc");
//  disp(wrc,"wrc");
  
//  disp(xx,"xx");
//  disp(z,"z");
//  disp(zzr,"zzr");
//  disp(lepr,"lepr");
//  disp(wrr,"wrr");

//  disp(wrr,"wrr",z,"z");
  //pac = points along columns having z_val
  //similarly for par
  pac = lepc .* wrc;
  par = lepr .* wrr;
//  disp(pac,"pac");
//  disp(par,"par");
  //eq = grid points with z_val
  eq = (z == z_val);
  eqc = eq .* Y;
  eqr = eq .* X;
//  disp(z,"z");
//  disp(eq,"eq");
//  disp(eqc,"eqc");
//  disp(eqr,"eqr");
//  return;

  //note that the same entry of pac(r)
  //and eqc(r) cannot be non-zero
  //at the same time.
  
//  join_pts(wrc,wrr,eq);
  
  [xv,yv] = join_pts(pac,par,eqc,eqr);
  
endfunction

function [xv,yv] = join_pts(pac,par,eqc,eqr)
  
  //apc = all points along columns
  //similarly for apr
  apc = [pac; zeros(1,n)] + eqc;
  apr = [par, zeros(m,1)] + eqr;
//  disp(apc,"apc");
//  disp(apr,"apr");

  //cfcp = connections from column points
  cfcp = cell(1,7);
  
  //[ (0,0)-(0,1) ) to [ (0,0)-(1,0) )
  cfcp(1).entries = [[sign(apc(1:$-1,1:$-1)) .* apr(1:$-1,1:$-1), zeros(m-1,1)]; zeros(1,n)];
//  disp(cfcp.entries(1),"c1");

  //[ (0,0)-(0,1) ) to [ (1,0)-(1,1) )
  cfcp(2).entries = [sign(apc(:,1:$-1)) .* apc(:,2:$), zeros(m,1)];
//  disp(cfcp.entries(2),"c2");  

  //[ (0,0)-(0,1) ) to (1,1)
  cfcp(3).entries = [[sign(apc(1:$-1,1:$-1)) .* eqc(2:$,2:$), zeros(m-1,1)]; zeros(1,n)];
//  disp(cfcp.entries(3),"c3");

  //[ (0,0)-(0,1) ) to [ (0,1)-(1,1) )
  cfcp(4).entries = [[sign(apc(1:$-1,1:$-1)) .* apr(2:$,1:$-1), zeros(m-1,1)]; zeros(1,n)];
//  disp(cfcp.entries(4),"c4");

  //[ (0,0)-(0,1) ) to [ (-1,1)-(0,1) )
  cfcp(5).entries = [[zeros(m-1,1), sign(apc(1:$-1,2:$)) .* apr(2:$,1:$-1)]; zeros(1,n)];
//  disp(cfcp.entries(5),"c5");
  
  //[ (0,0)-(0,1) ) to [ (-1,0)-(0,0) )
  cfcp(6).entries = [[zeros(m-1,1), sign(apc(1:$-1,2:$)) .* apr(1:$-1,1:$-1)]; zeros(1,n)];
//  disp(cfcp.entries(6),"c6");

  
  //cbrp = connection between row points
  //( (0,0)-(1,0) ) to [ (0,1)-(1,1) )
  cbrp = [[sign(par(1:$-1,:)) .* apr(2:$,1:$-1), zeros(m-1,1)]; zeros(1,n)];
//  disp(cbrp,"cbrp");

  //gt11 = grid-pt to north-west row bar within range pt (about 11o'clock points)
  //(1,1) to ( (0,0)-(1,0) )
  gt11 = [[sign(eqr(2:$,2:$)) .* par(1:$-1,:), zeros(m-1,1)]; zeros(1,n)];
  //  disp(gt11,"gt11");
  
  [xv,yv] = draw_contour(apc,cfcp,cbrp,gt11);

endfunction


function [xv,yv] = draw_contour(apc,cfcp,cbrp,gt11)

  xv = [];
  yv = [];
  
  for i = 1:1:m
    for j = 1:1:n
      if(cfcp(1).entries(i,j)~=0)
        xv = [xv, [x(j);cfcp(1).entries(i,j)]];
        yv = [yv, [apc(i,j); y(i)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(cfcp(2).entries(i,j)~=0)
        xv = [xv, [x(j);x(j+1)]];
        yv = [yv, [apc(i,j); apc(i,j+1)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(cfcp(3).entries(i,j)~=0)
        xv = [xv, [x(j); x(j+1)]];
        yv = [yv, [apc(i,j); y(i+1)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(cfcp(4).entries(i,j)~=0)
        xv = [xv, [x(j); cfcp(4).entries(i,j)]];
        yv = [yv, [apc(i,j); y(i+1)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(cfcp(5).entries(i,j)~=0)
        xv = [xv, [x(j); cfcp(5).entries(i,j)]];
        yv = [yv, [apc(i,j); y(i+1)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(cfcp(6).entries(i,j)~=0)
        xv = [xv, [x(j); cfcp(6).entries(i,j)]];
        yv = [yv, [apc(i,j); y(i)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(cbrp(i,j)~=0)
        xv = [xv, [par(i,j); cbrp(i,j)]];
        yv = [yv, [y(i); y(i+1)]];
      end
    end
  end
  
  for i = 1:1:m
    for j = 1:1:n
      if(gt11(i,j)~=0)
        xv = [xv, [x(j); gt11(i,j)]];
        yv = [yv, [y(i); y(i-1)]];
      end
    end
  end
  
endfunction