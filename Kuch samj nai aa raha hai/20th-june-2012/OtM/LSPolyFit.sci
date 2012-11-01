function p = LSPolyFit(x,y,deg)
  //fit a polynomial 'p' of degree 'deg'
  //given the obs. n x 1 vector 'y' at
  //location vector 'x' (of same size)
  
  X = []
  for i = 0:1:deg
    X = [X x^i];
  end
  XX = X' * X;
  Y = X' * y;
  coefficients = inv(XX) * Y;
  p = poly(coefficients,'x',"coeff");
  
endfunction