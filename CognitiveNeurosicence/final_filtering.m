clc; clear;

cd('\\data.triton.aalto.fi\scratch\nbe\socialneurocognition\summer_data\subjects_pre_results_2')
addpath('\\home.org.aalto.fi\zhangj14\data\Documents\matlab_first\packages')

subjects = [56:58];

%%
for subj = subjects
    
    load(strcat('zeropadded-', num2str(subj), '.mat'));

    len_pre = length(find(data_final.trialinfo==300));
    len_post = length(find(data_final.trialinfo==302));

    for i = 1:2
        if i == 1
            condition = 'pre';
            len_data = len_pre;
            trials = data_final.trial(1:len_pre);
        elseif i == 2
            condition = 'post';
            len_data = len_post;
            trials = data_final.trial(len_pre+1:len_pre+len_post);
        end

        data_conc = [];
        for t = 1:len_data
            data_conc = [data_conc  trials{t}]; 
        end

        % Design the filter:

        freqs = [0.45 0.5 10.5 11];
        Fs = 400.002;  % Sampling Frequency

        Fstop1 = freqs(1);  % First Stopband Frequency
        Fpass1 = freqs(2);    % First Passband Frequency
        Fpass2 = freqs(3);    % Second Passband Frequency
        Fstop2 = freqs(4);    % Second Stopband Frequency
        Astop1 = 60;      % First Stopband Attenuation (dB)
        Apass  = 1;       % Passband Ripple (dB)
        Astop2 = 60;      % Seco    nd Stopband Attenuation (dB)
        match  = 'both';  % Band to match exactly
        % Construct an FDESIGN object and call its ELLIP method.
        h  = fdesign.bandpass(Fstop1, Fpass1, Fpass2, Fstop2, Astop1, Apass, ...
            Astop2, Fs);
        Hd = design(h, 'ellip', 'MatchExactly', match);

        for ch = 1:size(data_conc,1)
            filtered(:,ch) = filtfilthd(Hd, data_conc(ch,:)');
        end
        
        save(['filtered-', num2str(subj), '-', condition, '.mat'], 'filtered');

        clear data_conc filtered

    end
end