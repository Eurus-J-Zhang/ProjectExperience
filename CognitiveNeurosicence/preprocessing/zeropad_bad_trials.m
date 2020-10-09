%% Track and zero-pad bad trials
% Kaisu Lankinen 04.07.2020

%% Subject names (here form y_<subjcode>.mat

subjects{1} = 704;
subjects{2} = 706;
subjects{3} = 712;

%% Go through data and zero-pad bad trials

m_c = 'c'; % mother ('m') or child ('c')
trial_length = 400; % 400 ms

for subj = 1:length(subjects)

    clear data
    clear code
    
    % load data:
    load(['y_', num2str(subjects{subj}), m_c, '.mat']);
    data = cleaned_data.trial;
    
    % load removed trials:
    load(['y_', num2str(subjects{subj}), '.mat']);
    bad = trial_info.bad_trials;
    
    % check if they match:
    if length(data) ~= (trial_info.num_of_all_trials - length(trial_info.bad_trials))
        disp(['Subject: ', num2str(subjects{subj}), m_c,  ', the number of removed trials does not match the cleaned data'])
        break;
    end
    
    
    i = 1;
    for k = 1:trial_info.num_of_all_trials 
        
        if find(bad == k)
            
            % Assign a code for conditions:
            if k == 1
                code(k) = cleaned_data.trialinfo(i);% assign the first code
            else
                
                length_previous = length(find(code==code(k-1)));
                if length_previous < 89
                    code(k) = code(k-1); % assign the previous code
                else
                    code(k) = cleaned_data.trialinfo(i+1)
                end
               
            end
            
            data_zeropad{k} =zeros(size(data{1},1),trial_length); % zero-pad the trial
        else
            
            data_zeropad{k} = data{i};
            code(k) = cleaned_data.trialinfo(i);
            i = i+1;    
        end
    end
    
 
    % Save data according to codes:
        
        indices = find(code==200);
        pick = [data_zeropad(:)];
        data_selected = pick(indices);
        save(['data_control1_', m_c, num2str(subjects{subj}), '.mat'], 'data_selected');
        lengths(1) = length(data_selected);
        
        indices = find(code==202);
        pick = [data_zeropad(:)];
        data_selected = pick(indices);
        save(['data_control2_', m_c, num2str(subjects{subj}), '.mat'], 'data_selected');
        lengths(2) = length(data_selected);
        
        indices = find(code==204);
        pick = [data_zeropad(:)];
        data_selected = pick(indices);
        save(['data_self1_', m_c, num2str(subjects{subj}), '.mat'], 'data_selected');
        lengths(3) = length(data_selected);
        
        indices = find(code==206);
        pick = [data_zeropad(:)];
        data_selected = pick(indices);
        save(['data_self2_', m_c, num2str(subjects{subj}), '.mat'], 'data_selected');
        lengths(4) = length(data_selected);
       
        display(lengths)
        
        if length(unique(lengths)) > 1
            disp(['Subject: ', num2str(subjects{subj}), m_c,  ', the lengths of different conditions do not match, check the data.'])
            break;
        end
    
    
end


