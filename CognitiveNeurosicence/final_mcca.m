%%% This script calculates MCCA-part in Lankinen et al. 2018 article.
% Kaisu Lankinen 07.07.2020
clc; clear; close all;

%addpath(genpath('C:\Users\joona\Desktop\summer-project\mcca\scripts\mcca-modified\'))
addpath ('\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\mcca')
data_load_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects_pre_results_2\';
%'Z:\nbe\socialneurocognition_1\processed_data\41-50\';
pca_save_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects_pre_results_2\pca_Joonas\';
%'Z:\nbe\socialneurocognition_1\processed_data\mcca\subj41-50\pca\';
%mcca_save_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects_pre_results_2\mcca_Joonas\';
%%
mcca_save_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects_pre_results_2\mcca_41_60\';
%'Z:\nbe\socialneurocognition_1\processed_data\mcca\subj41-50';

%% Subject names:

subjects = {41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60};
%subjects = {51,52,53,54,55,56,57,58,59,60};
prepost = 'post';   

%%

pca_comps = 50;

% Indices for cross validation: (here 3-fold cross validation, i.e. divide the data into 3 parts)
kfold = 3;
if strcmp(prepost, 'pre')
    data_len = 101304;
elseif strcmp(prepost, 'post')
    data_len = 104922;
end 
block = floor(data_len/3);
last = 3*block;

train_indices(1,:) = [1:2*block]; % For the first train set, take 2/3 of the data from the beginning, leave the last third to the test set
train_indices(2,:) = [(block+1):last];   
train_indices(3,:) = [(1:block), ((2*block+1):last)];

test_indices(1,:) = [(2*block+1):last];
test_indices(2,:) = [1:block];
test_indices(3,:) = [(block+1):(2*block)];

      
%% Calculate pca:

for subj = 1:length(subjects)
    
    cd(data_load_path);
    load(['filtered-', num2str(subjects{subj}), '-', prepost, '.mat']);

    % 0-mean the data:
    data_0m = bsxfun(@minus, filtered, mean(filtered));

    % Calculate PCA:
    [coeff, score, latent] = pca(data_0m);

    % Save covariances(to be used later in activation map
    % calculations):
    for xval = 1:kfold
        data_te = data_0m(test_indices(xval,:),:); % to be used later in activation map calculations
        covx{xval} = cov(data_te);
    end
    
    cd(pca_save_path);
    save(['data_pca_', num2str(subjects{subj}), '-', prepost,  '.mat'], 'coeff', 'score', 'covx');

end

%% Calculate mcca:


for xval = 1:kfold % 
    
    clear Xtr
    clear Xte

    % Combine all subjects' data to be used as an input to mcca: 
    cd(pca_save_path);
    for subj = 1:length(subjects)
       load(['data_pca_', num2str(subjects{subj}), '-', prepost,  '.mat']);
       Xtr(:,:,subj) = score(train_indices(xval,:),1:pca_comps)';
       Xte(:,:,subj) = score(test_indices(xval,:),1:pca_comps)';
    end
    
    cd(mcca_save_path);
    
    [W] = mcca(Xtr,pca_comps,'maxvar');
    
    save(['W_xval', num2str(xval), '-', prepost, '.mat'], 'W');

    % projections U:
    for subj = 1:length(subjects)
        Utr(:,:,subj) = W(:,:,subj)*Xtr(:,:,subj);
        Ute(:,:,subj) = W(:,:,subj)*Xte(:,:,subj);
    end

    save(['U_xval', num2str(xval), '-', prepost, '.mat'], 'Utr', 'Ute');


%% Calculate pair-wise correlations between different subject pair combinations:

    for comp = 1:30    
         U_comp = squeeze(Utr(comp,:,:));
         corr_matrix = corr(U_comp); % calculate cross-correlation matrix
         tri = triu(corr_matrix,1); % take the upper triangle of the matrix
         ind = find(tri); % pick the non-zero elements
         correlation_tr(comp,:) =  tri(ind);
    end
   
    figure;boxplot(correlation_tr');
    xlabel('component number');
    ylabel('subject pair');
    title('Pair-wise correlations of projections (train data)');
    saveas(gcf,['corr_tr_xval', num2str(xval), '-', prepost, '.jpg'])

     for comp = 1:30
         U_comp = squeeze(Ute(comp,:,:));
         corr_matrix = corr(U_comp); % calculate cross-correlation matrix
         tri = triu(corr_matrix,1); % take the upper triangle of the matrix
         ind = find(tri); % pick the non-zero elements
         correlation_te(comp,:) =  tri(ind);  
    end

    figure;boxplot(correlation_te');
    xlabel('component number');
    ylabel('subject pair');
    title('Pair-wise correlations of projections (test data)');
    saveas(gcf,['corr_te_xval', num2str(xval), '-', prepost, '.jpg'])

    save(['correlations_xval', num2str(xval), '-', prepost, '.mat'], 'correlation_tr', 'correlation_te');

    
end