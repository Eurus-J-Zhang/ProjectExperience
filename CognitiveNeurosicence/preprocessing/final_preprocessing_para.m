clear; clc;
%%
addpath('\\home.org.aalto.fi\zhangj14\data\Documents\matlab_first\fieldtrip-new\fieldtrip-20200607')
addpath('\\home.org.aalto.fi\zhangj14\data\Documents\matlab_first\packages')
addpath(genpath('\\home.org.aalto.fi\zhangj14\data\Documents\matlab_first\ft_BIU'))

ft_defaults;

%% load excel data

excel_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\behavioral_full\';
data_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects\'; 
save_path = '\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects_pre_results_2';
%%
subjects = [59];

subj_idx = 1;
for subj=subjects

    prepost = 'pre';
    [sent_pre_orig{subj_idx}, sent_pre_cond{subj_idx}, sent_pre_id{subj_idx}] = sentence_length(subj, prepost, excel_path);
    prepost = 'post';
    [sent_post_orig{subj_idx}, sent_post_cond{subj_idx}, sent_post_id{subj_idx}] = sentence_length(subj, prepost, excel_path);  
    subj_idx = subj_idx + 1;
end
clear subj prepost subj_idx

%% create epoched data structures

channels = {'MEG'};
source = 'xc,lf_c,rfhp0.1Hz'; 

%%

subj_idx = 1;
for subj = subjects

    cd(strcat (data_path, 'para', num2str(subj)));

%%
    cfg = [];
    cfg.dataset = source;
    hdr = ft_read_header(cfg.dataset);
    event = ft_read_event(cfg.dataset);

    trig = [event(find(strcmp('TRIGGER', {event.type}))).value];
    idx = [event(find(strcmp('TRIGGER', {event.type}))).sample];

    sampRate = hdr.Fs;
%%
    cond200 = 200;
    time200 = idx(find(trig==cond200));
    if subj==45
        time200_pre = sort_triggers(sent_pre_cond{subj_idx}(1:6,:), time200(2:7));
        time200_post = sort_triggers(sent_post_cond{subj_idx}(1:6,:), time200(8:13)); 
    else
        time200_pre = sort_triggers(sent_pre_cond{subj_idx}(1:6,:), time200(1:6)); 
        time200_post = sort_triggers(sent_post_cond{subj_idx}(1:6,:), time200(7:12));  
    end

    cond202 = 202;
    time202 = idx(find(trig==cond202)); 
    time202_pre = sort_triggers(sent_pre_cond{subj_idx}(7:12,:), time202(1:6));
    time202_post = sort_triggers(sent_post_cond{subj_idx}(7:12,:), time202(7:12));

    cond204 = 204;
    time204 = idx(find(trig==cond204));
    time204_pre = sort_triggers(sent_pre_cond{subj_idx}(13:18,:), time204(1:6));
    time204_post = sort_triggers(sent_post_cond{subj_idx}(13:18,:), time204(7:12));

    cond206 = 206;
    time206 = idx(find(trig==cond206));
    time206_pre = sort_triggers(sent_pre_cond{subj_idx}(19:24,:), time206(1:6));
    time206_post = sort_triggers(sent_post_cond{subj_idx}(19:24,:), time206(7:12));

    cfg_pre = [];
    cfg_pre.dataset = source;
    cfg_pre.channel = channels;
    cfg_pre.trialfun = 'trialfun_beg';
    cfg_pre = ft_definetrial(cfg_pre);
    cfg_pre = define_epochs(sent_pre_id{subj_idx}(1:6,:), time200_pre, cond200, sampRate, cfg_pre);
    cfg_pre = define_epochs(sent_pre_id{subj_idx}(7:12,:), time202_pre, cond202, sampRate, cfg_pre);
    cfg_pre = define_epochs(sent_pre_id{subj_idx}(13:18,:), time204_pre, cond204, sampRate, cfg_pre);
    cfg_pre = define_epochs(sent_pre_id{subj_idx}(19:24,:), time206_pre, cond206, sampRate, cfg_pre);
    cfg_pre.trl(:,7) = 300; 
    cfg_pre.trl = round(cfg_pre.trl);
    data_pre{subj_idx} = ft_preprocessing(cfg_pre);

    cfg_post = [];
    cfg_post.dataset = source;
    cfg_post.channel = channels;
    cfg_post.trialfun = 'trialfun_beg';
    cfg_post = ft_definetrial(cfg_post);
    cfg_post = define_epochs(sent_post_id{subj_idx}(1:6,:), time200_post, cond200, sampRate, cfg_post);
    cfg_post = define_epochs(sent_post_id{subj_idx}(7:12,:), time202_post, cond202, sampRate, cfg_post);
    cfg_post = define_epochs(sent_post_id{subj_idx}(13:18,:), time204_post, cond204, sampRate, cfg_post);
    cfg_post = define_epochs(sent_post_id{subj_idx}(13:18,:), time206_post, cond206, sampRate, cfg_post);
    cfg_post.trl(:,7) = 302;
    cfg_post.trl = round(cfg_post.trl);
    data_post{subj_idx} = ft_preprocessing(cfg_post);

    cfg = [];
    data_combined{subj_idx} = ft_appenddata(cfg, data_pre{subj_idx}, data_post{subj_idx}); 

    subj_idx = subj_idx + 1;
end
%
keep save_path data_combined subjects channels

%% inspect trials and channels

subj_idx = 1;
for subj = subjects
    cfg = [];
    cfg.hpfilter = 'yes';
    cfg.hpfreq = 60;
    cfg.channels = channels;
    cfg.padding = 10;
    data_hpfilt = ft_preprocessing(cfg, data_combined{subj_idx});

    set(0, 'DefaultFigureWindowStyle','docked')
    cfg = [];
    data_rejected{subj_idx} = ft_rejectvisual(cfg, data_hpfilt);
    
    [idx,loc] = ismember(data_rejected{subj_idx}.cfg.artfctdef.summary.artifact(:,1), data_combined{subj_idx}.sampleinfo(:,1));
    bad_trials = loc(idx);
    data_combined{subj_idx}.trialinfo(:,5) = ones;  
    data_combined{subj_idx}.trialinfo(bad_trials,5) = zeros;
   
    subj_idx = subj_idx + 1;
end
%%
keep save_path subjects data_combined data_rejected channels

%% filter data

subj_idx = 1;
for subj = subjects
    cfg = [];               
    cfg.channels = channels;
    cfg.bpfilter = 'yes';
    cfg.bpfreq = [0.2 200];
    cfg.padding = 10;
     data_filtered = ft_preprocessing(cfg, data_combined{subj_idx});
    %data_filtered = ft_preprocessing(cfg, data_combined_2{1});
    cfg = [];
    cfg.resamplefs = 400;
    data_resampled{subj_idx} = ft_resampledata(cfg, data_filtered);
    subj_idx = subj_idx + 1;
end

keep save_path channels subjects data_resampled data_rejected

%% save the data

cd(save_path);
subj_idx = 1;
for subj = subjects
    %eval(['data = data_filtered{subj_idx};']);
    eval(['data = data_resampled{subj_idx};']);
    save(strcat('no_ica-', num2str(subjects(subj_idx))), 'data');
    subj_idx = subj_idx + 1;
end

%% compute ICA

cfg = [];
cfg.channels = channels;
cfg.method = 'runica';

subj_idx = 1;
for subj=subjects
    %ica{subj_idx} = ft_componentanalysis(cfg, data_filtered{subj_idx});
    ica{subj_idx} = ft_componentanalysis(cfg, data_resampled{subj_idx});
    subj_idx = subj_idx + 1;
end

%% inspect the ICA components

subj_idx = 1;
cfg = [];
%ft_databrowser(cfg, ica{subj_idx}, data_filtered{subj_idx}); 
ft_databrowser(cfg, ica{subj_idx});%, data_resampled{subj_idx});

%% remove the ICA components

cfg = [];
cfg.component = [1,4];%change

%41:1,2 ok
%46:1,2,3
%48:1
%49:1
%51:2,9
%52:1,2
%59:1,4
%60:1,2

data_final = ft_rejectcomponent(cfg, ica{subj_idx});
%%
cd(save_path);  
save(strcat('preprocessed-', num2str(subjects(subj_idx))), 'data_final')

%% zero bad trials and/or channels

if ~isequal(data_rejected{subj_idx}.label, data_final.label)
    ch_idx = find(ismember(data_final.label, data_rejected{subj_idx}.label)==0);
    for ch = ch_idx'
        for tri_idx = 1:length(data_final.trial)
            data_final.trial{tri_idx}(ch,:) = 0;
        end
    end
end

bad_trials = find(data_final.trialinfo(:,5)==0);
for i = 1:length(bad_trials)
    trial = data_final.trial{bad_trials(i)};
    data_final.trial{bad_trials(i)} = zeros(size(trial, 1), size(trial, 2));
end  

cd(save_path);  
save(strcat('zeropadded-', num2str(subjects(subj_idx))), 'data_final')

%% visualize the data

figure;
cfg = [];
cfg.title = ['subj' subjects(subj_idx)];
cfg.layout = '4D248.lay';
cfg.showlabels = 'yes';
cfg.fontsize = 6;
ft_multiplotER(cfg, data_final);

figure;
cfg = [];
cfg.title = ['subj' subjects(subj_idx)];
cfg.layout = '4D248.lay';
cfg.xlim = [-0.7 : 0.4 : 3.15];  
ft_topoplotER(cfg, data_final);

figure;
cfg = [];
cfg.title = ['subj' subjects(subj_idx)];
cfg.layout = '4D248.lay';
ft_topoplotER(cfg, data_final);
