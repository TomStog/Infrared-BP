function [matchedPeaks1, matchedPeaks2] = matchAndExcludePeaks(peaks1, peaks2)
    
    len1 = length(peaks1);
    len2 = length(peaks2);
    
    matchedPeaks1 = [];
    matchedPeaks2 = [];
    
    for i=1:len1
        for j=1:len2
           dist(i,j) = abs(peaks1(i) - peaks2(j)); 
        end
    end
    
    if len1>=len2
        %matchedPeaks2 = peaks2 ;
        count = 1;
        for i=1:len2
            if min(dist(:,i))<=5
                [row, ~] = find(dist(:,i) == min(dist(:,i)));
                matchedPeaks1(count) = peaks1(row(1));
                matchedPeaks2(count) = peaks2(i);
                count = count + 1 ;
            else
                continue
            end
        end        
    else
        %matchedPeaks1 = peaks1 ;
        count = 1;
        for i=1:len1
            if min(dist(i,:))<=5
                [~, column] = find(dist(i,:) == min(dist(i,:)));
                matchedPeaks1(count) = peaks1(i);
                matchedPeaks2(count) = peaks2(column(1));
                count = count + 1 ;
            else
                continue
            end
        end          
    end
end