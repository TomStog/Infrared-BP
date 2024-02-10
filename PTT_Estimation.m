clear;
clc;
close all;
format short

person_subfolders = ['01\';'03\';'04\';'05\';'06\';'07\';'08\';'10\';'11\';'12\';'13\';'14\';'15\';'16\';'17\'];
person_len = size(person_subfolders, 1);
gt_bp = [107 72;138 79;139 71;105 59;122 79;127 78;159 86;134 72;153 76;127 66;118 67;113 62;107 57;142 84;136 79];
M = [];
N = [];

for k=1:person_len

    vpath = '..\Forehead_Amp\Forehead\Day1\';
    mypath1 = [vpath person_subfolders(k, :)];    
    info1 = dir(mypath1);

    vpath = '..\Hand_Amp\Hand\Day1\';
    mypath2 = [vpath person_subfolders(k, :)];    
    info2 = dir(mypath2);
    
    M_temp = [];
    N_temp = [];

    for i = 1:length(info1)-2

        str1 = string(mypath1);
        str2 = string(info1(i+2).name);
        str = strcat(str1,str2);
        vidObj1 = VideoReader(str);
        allFrames1 = read(vidObj1);
        var1 = vidObj1.Duration*vidObj1.FrameRate;

        str1 = string(mypath2);
        str2 = string(info2(i+2).name);
        str = strcat(str1,str2);
        vidObj2 = VideoReader(str);
        allFrames2 = read(vidObj2);
        var2 = vidObj2.Duration*vidObj2.FrameRate;

        varm1 = min([var1,var2]);  

        for j=1:varm1
            G1 = rgb2gray(allFrames1(:,:,:,j));
            G2 = rgb2gray(allFrames2(:,:,:,j));
            
            G1 = im2double(G1);
            G2 = im2double(G2);           
            
            meanG1(j) = mean(G1(:));
            meanG2(j) = mean(G2(:));
            
            meanG3(j) = std(G1(:));
            meanG4(j) = std(G2(:));
        end      
        
        meanG1 = bandpass(meanG1,[0.4 4],vidObj1.FrameRate);
        meanG2 = bandpass(meanG2,[0.4 4],vidObj2.FrameRate);
        
        meanG3 = bandpass(meanG3,[0.4 4],vidObj1.FrameRate);
        meanG4 = bandpass(meanG4,[0.4 4],vidObj2.FrameRate);
        
        pks_G1 = findpeaks(meanG1,vidObj1.FrameRate);
        [~, pks_ind1] = ismember(pks_G1, meanG1);
        pks_ind1 = pks_ind1(pks_ind1 ~= 0);
        
        pks_G2 = findpeaks(meanG2,vidObj2.FrameRate);
        [~, pks_ind2] = ismember(pks_G2, meanG2);
        pks_ind2 = pks_ind2(pks_ind2 ~= 0);
        
        pks_G3 = findpeaks(meanG3,vidObj1.FrameRate);
        [~, pks_ind3] = ismember(pks_G3, meanG3);
        pks_ind3 = pks_ind3(pks_ind3 ~= 0);
        
        pks_G4 = findpeaks(meanG4,vidObj2.FrameRate);
        [~, pks_ind4] = ismember(pks_G4, meanG4);
        pks_ind4 = pks_ind4(pks_ind4 ~= 0);
        
        [matchedPeaks1, matchedPeaks2] = matchAndExcludePeaks(pks_ind1, pks_ind2);
        [matchedPeaks1, matchedPeaks2] = keepsmalldif(matchedPeaks1, matchedPeaks2);
        
        [matchedPeaks3, matchedPeaks4] = matchAndExcludePeaks(pks_ind3, pks_ind4);
        [matchedPeaks3, matchedPeaks4] = keepsmalldif(matchedPeaks3, matchedPeaks4);

        % Code for plotting the PTTs
        %figure,        
        %p1 = plot(meanG1(1:50));
        %hold on
        %p3 = scatter(matchedPeaks1(1:6),meanG1(matchedPeaks1(1:6)),'ro');
        %hold on,
        %p2 = plot(meanG2(1:50));
        %hold on
        %scatter(matchedPeaks2(1:6),meanG2(matchedPeaks2(1:6)),'ro');
        %xlabel('Frames') 
        %ylabel('Magnitude')
        %title('Pulse Transit Time Graph')
        %legend([p1 p2 p3],{'Forehead Signal','Upper Palm Signal','Local Peak'},'Location','southeast')
        %hold off
        
        test1 = median(abs(matchedPeaks1-matchedPeaks2))*1000/vidObj2.FrameRate;
        test2 = median(abs(matchedPeaks3-matchedPeaks4))*1000/vidObj2.FrameRate;
        M_temp = [M_temp;test1];
        N_temp = [N_temp;test2];
    end    
    M = [M;mean(M_temp) mean(N_temp) gt_bp(k,1) gt_bp(k,2)];
end

xlswrite('blood_pressure_mean_std.xlsx',M)
