function [sent_orig, sent_cond, sent_id] = sentence_length(subj, prepost, data_folder)

if (gt(subj,40) && lt(subj,61)) || (gt(subj,0) && lt(subj,21))
    version = 1; % for subj1-20, 41-60
elseif (gt(subj,20) && lt(subj,41)) || (gt(subj,60) && lt(subj,81))
    version = 2; % for subj21-40, 61-80
end 

cd(strcat (data_folder, 'para', num2str(subj)));

if strcmp(prepost, 'pre')
    %[NUM, TXT] = xlsread('pre.xlsx');
    TXT = readtable(strcat('para',num2str(subj),'-pre.txt'));
elseif strcmp(prepost, 'post')
    %[NUM, TXT] = xlsread('post.xlsx');
    TXT = readtable(strcat('para',num2str(subj),'-post.txt'));
end

% if gt(subj, 50) && lt(subj,61)
%     B(:,1)=str2double(TXT(:,7)); B(:,2)=str2double(TXT(:,9)); B(:,3)=str2double(TXT(:,11)); 
% else
%     B(:,1)=NUM(:,3); B(:,2)=NUM(:,5); B(:,3)=NUM(:,7);
% end
% 
% b = regexp(TXT(:,3),'\d+(\.)?(\d+)?','match');
% B(:,4) = str2double([b{:}])'; 


    b=regexp(table2array(TXT(:,3)),'\d+(\.)?(\d+)?','match');
    B(:,1)=table2array(TXT(:,7));B(:,2)=table2array(TXT(:,9));
    B(:,3)=table2array(TXT(:,11));B(:,4)= str2double([b{:}])'; 



if version == 1 
    if strcmp(prepost, 'pre')
        load prelength
        len = prelength; clear prelength
    elseif strcmp(prepost, 'post')
        load postlength
        len = postlength; clear postlength
    end
elseif version == 2 
    if strcmp(prepost, 'pre')
        load postlength
        len = postlength; clear postlength
    elseif strcmp(prepost, 'post')
        load prelength
        len = prelength; clear prelength
    end
end

for i = 1:size(B,1)
    B(i,5) = len(find(B(i,4) == len(:,2)),1);
end

if subj==36 || subj==1 % left-handed
    F = B(:,4:5);  
    B(:,4:5) = [];   
    B(find(B==1)) = 10;
    B(find(B==2)) = 9; 
    B(find(B==3)) = 8; 
    B(find(B==4)) = 7; 
    B(find(B==5)) = 6; 
    B=[B F]; clear F        
elseif subj~=36 && subj~=1 % right-handed          
    F = B(:,4:5);  
    B(:,4:5) = [];   
    B(find(B==7)) = 10; %transform 0 to 10
    B(find(B==8)) = 7; %transform 0 to 10
    B(find(B==9)) = 8; %transform 0 to 10
    B(find(B==0)) = 9; %transform 0 to 10
    B=[B F]; clear F
end 

sent_orig = B;
sent_id = sortrows(B, 4);
sent_cond = sortrows(B, 1);

end
