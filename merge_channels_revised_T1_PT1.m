%% Start by going to the Study day folder 
%You need Adritools in your Matlab path. Else Matlab won't recognize'getfolder'.
addpath(genpath('/home/genzel/dimitris/ADRITOOLS-master'))
addpath(genpath('/home/genzel/dimitris/analysis-tools-master'))

%Sampling freq:
fs=20000; % For OS-normal Rats 1-9 this should be 20000.
          % For other Rats of OS-normal and all RGS14 Rats use 30000.
%%
%Get trial folders 
cd ..
cd ..
foldername='/media/genzel/Data/rat9/sd15/Rat_OS_Ephys_Rat9_57989_SD15_OR_SD_25-26_06_2018';
addpath((foldername));
cd(foldername)

folders=getfolder;
folders=folders(or(contains(folders,'trial1'),contains(folders,'post_trial1')));

for i=1:length(folders)
    fprintf(folders{i})
    fprintf('\n')
    
    %Ignore test folders
    if i~=1
        if ~contains(folders{i},'trial5') && contains(folders{i-1},'trial5')
            remove_ind=[i];
        end
    end
end

if exist('remove_ind','var') == 1
    folders=folders(1:remove_ind-1);
end    
    

%% Check that the order is correct in the printed folder names.
% If order is wrong, fix by swapping place of trial cell to the beginning. 
if contains(folders{end},'post') ==0
    folders=[folders(end) folders(1:end-1)];
end

if size(folders,2)~=2
    error('Check data, you have multiple chunks of your post or trial data.')
    
end

%% Select channels to merge
channels=[ ...
        33,42,43,64 ...
        34,35,36,41 ...
        37,38,39,40 ...
        22,23,24,25 ...
        20,21,26,27 ...
        17,18,19,28 ...
        14,15,16,29 ...
        12,13,30,31 ...
        1,10,11,32
        ];



%% Merging
clc
f=waitbar(0,'Please wait...');
counter=0;
tic

for j=1:length(channels)
    for i=1:length(folders)-1
        
        fprintf('Channel: %d\n', channels(j));
        % folders{i+1}   
        counter=counter+1;
        
        %Read presleep first.
        if i==1         
            cd(folders{i})
            % Check for a truncated folder
            subfolders = getfolder;
            if size(subfolders, 1) > 0
                if subfolders{1} == "truncated"
                    cd('truncated');
                    fprintf('Found truncated folder in %s !\n', folders{i});
                end
            end
               
            CD=split(cd,'/');
            % CD{end}
            
            files=dir;
            files={files.name};
            file=files(contains(files,['CH',num2str(channels(j))]));
            file=file{1};
            
            if  j==1   %Only run with the first channel.
                signal=load_open_ephys_data(file); % changed to simple version
                trial_durations(1)=length(signal);
            end
            
            % load data from file 1
            NUM_HEADER_BYTES = 1024;
            fid1 = fopen(file);
            fseek(fid1,0,'eof');
            filesize = ftell(fid1);
            fseek(fid1,0,'bof');
            hdr1 = fread(fid1, NUM_HEADER_BYTES, 'char*1');
            samples1 = fread(fid1, 'int16');

        end

        %Read next (post)trial
        cd ..

        % Check for a truncated folder
        subfolders = getfolder;
        if size(subfolders, 1) > 0
            if subfolders{1} == "truncated"
                cd ..
            end
        end

        cd(folders{i+1})
        
        % Check for a truncated folder
        subfolders = getfolder;
        if size(subfolders, 1) > 0
            if subfolders{1} == "truncated"
                cd('truncated');
                fprintf('Found truncated folder in %s !\n', folders{i+1});
            end
        end
        
        CD=split(cd,'/');
        % CD{end}
        
        files=dir;
        files={files.name};
        file=files(contains(files,['CH',num2str(channels(j))]));
        file=file{1};
        
        if  j==1
            signal=load_open_ephys_data(file);
            trial_durations(i+1)=length(signal);
        end
        % load data from file 2
        fid2 = fopen(file);
        fseek(fid2,0,'eof');
        filesize = ftell(fid2);
        fseek(fid2,0,'bof');
        hdr2 = fread(fid2, NUM_HEADER_BYTES, 'char*1');
        samples2 = fread(fid2, 'int16');

        cd ..
        % Check for a truncated folder
        subfolders = getfolder;
        if size(subfolders, 1) > 0
            if subfolders{1} == "truncated"
                cd ..
            end
        end

        if i==1 && j==1 %If presleep and first channel, create new folder 'T1_PT1_merged'
            mkdir('T1_PT1_merged')   
        end

        cd('T1_PT1_merged')

        % write data into new file
        fid_final=fopen( ['100_','CH',num2str(channels(j)),'_0.continuous'], 'w');

        fwrite(fid_final, hdr1, 'char*1'); %First header, expected by Kilosort 
        fwrite(fid_final, samples1, 'int16');
        fwrite(fid_final, samples2, 'int16');
        fclose(fid1);
        fclose(fid2);
        fclose(fid_final);

        %% Now that file has been saved read again
        files=dir;
        files={files.name};
        file=files(contains(files,['CH',num2str(channels(j)),'_']));
        file=file{1};

        % load data from file 1
        NUM_HEADER_BYTES = 1024;
        fid1 = fopen(file);
        fseek(fid1,0,'eof');
        filesize = ftell(fid1);
        fseek(fid1,0,'bof');
        hdr1 = fread(fid1, NUM_HEADER_BYTES, 'char*1');
        samples1 = fread(fid1, 'int16');
        progress_bar(counter,(length(folders)-1)*length(channels),f)
        
    end
    %xo
    if j==1
        Trial_durations=table;
        Trial_durations.Variables=[ [{'Samples'};{'Cumulative Samples'};{'Seconds'}; {'Cumulative Seconds'};{'Minutes'}; {'Cumulative Minutes'};{'Hours'}; {'Cumulative Hours'}] [num2cell(trial_durations);num2cell(cumsum(trial_durations)); num2cell(trial_durations/fs); num2cell(cumsum(trial_durations/fs));num2cell(trial_durations/fs/60); num2cell(cumsum(trial_durations/fs/60));num2cell(trial_durations/fs/60/60); num2cell(cumsum(trial_durations/fs/60/60))] ];
        Trial_durations.Properties.VariableNames=[{'Unit'} cellfun(@(x) strrep(x(find(isletter(x), 1):end),'-','_') ,folders,'UniformOutput',false)];
        writetable(Trial_durations,strcat('Trial_durations.xls'),'Sheet',1,'Range','A1:Z50')
        save('trials_durations_samples.mat','trial_durations')
    end

    cd ..
end

toc

