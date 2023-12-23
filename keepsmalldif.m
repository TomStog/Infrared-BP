function [temp_array1,temp_array2] = keepsmalldif(array1,array2)
    temp_array1 = array1;
    temp_array2 = array2;

    sliding_win=zeros(2,2);

    for i=1:length(array1)
       sliding_win(1,1) = sliding_win(1,2);
       sliding_win(2,1) = sliding_win(2,2);
       sliding_win(1,2) = array1(i);
       sliding_win(2,2) = array2(i);

       if ((sliding_win(1,1)==sliding_win(1,2))||(sliding_win(2,1)==sliding_win(2,2)))
           temp1 = abs(sliding_win(1,1)-sliding_win(2,1));
           temp2 = abs(sliding_win(1,2)-sliding_win(2,2));

           if temp1>temp2
               temp_array1(i-1)=0;
               temp_array2(i-1)=0;
           else
               temp_array1(i)=0;
               temp_array2(i)=0;
           end
       else
           continue
       end
    end
    
    temp_array1 = nonzeros(temp_array1)';
    temp_array2 = nonzeros(temp_array2)';
end

