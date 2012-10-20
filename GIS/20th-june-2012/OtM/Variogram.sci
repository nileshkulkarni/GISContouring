function v = Variogram(x,y)
  //"intervalization" of the given
  //the "scatter-plot variogram" (x,y)
  //x,y are nx1 vectors
  
//  disp(x);
//  disp(y);
  N = size(x,1);
  k = 0;
  for i = 1:1:N
    for j = i+1:1:N
      k = k + 1;
//      disp('k');
//      disp(k);
//      disp('i,j'); disp(i); disp(j);
      temp_v(k,1) = norm(x(i,:)-x(j,:));
      temp_v(k,2) = 0.5 * (y(i)-y(j))^2;
    end
  end
//  disp(temp_v);
  
  d_min = min(temp_v(:,1));
  d_max = max(temp_v(:,1));
//  disp("d_min"); disp(d_min);
//  disp("d_max"); disp(d_max);
  
  total_range = d_max - d_min;
  X = cell(N,1);
  Y = cell(N,1);
  for i = 1:1:k
    if(temp_v(i,1)~=d_max)
      index = floor(((temp_v(i,1)-d_min)/total_range)*(N)) + 1;
//      disp(index);
    else
      index = N;
    end
    //    disp("index"); disp(index);
    X(index).entries = [X(index).entries; temp_v(i,1)];
    Y(index).entries = [Y(index).entries; temp_v(i,2)];
  end
//  disp(X);
  for i = 1:1:N
    if(X(i).entries==[])
      continue;
    else
      v(i,1) = mean(X(i).entries);
      v(i,2) = mean(Y(i).entries);
    end
  end
  
endfunction