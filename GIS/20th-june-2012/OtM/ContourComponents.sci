function comps = ContourComponents(xv,yv)
  
  N = size(xv,2);
  comps = cell();  
  
  if(N==0)
    return;
  end
  
  from = [xv(1,:);yv(1,:)];
  to = [xv(2,:);yv(2,:)];
//  disp("from size"); disp(size(from));
  i = 0;
  while size(from,2)~=0
    i = i+1;
    comps(i).entries = [];
    next = [1];
    while next~=[]
      j = next(1);
      comps(i).entries = [comps(i).entries, from(:,j)];
      from = [from(:,1:j-1),from(:,j+1:$)];
      if(from~=[])
        next = vectorfind(from,to(:,j),'c');
      else
        break;
      end
      to = [to(:,1:j-1),to(:,j+1:$)];
    end
  end
  
endfunction