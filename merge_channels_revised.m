%% Start by going to the Study day folder 
%You need Adritools in your Matlab path. Else Matlab won't recognize'getfolder'.
addpath(genpath('/home/genzel/dimitris/ADRITOOLS-master'))
addpath(genpath('/home/genzel/dimitris/analysis-tools-master'))

%Sampling freq:
fs=20000; %Can be different for some OS rats.

%%
%Get trial folders 
cd ..
cd ..
cd('/media/genzel/Data/rat9/sd14/Rat_OS_Ephys_Rat9_57989_SD14_OR_SD_NOV_23-24_05_2018')

folders=getfolder;
folders=folders(or(or(contains(folders,'pre'),contains(folders,'trial')),contains(folders,'novelty')));

for i=1:length(folders)
    fprintf(folders{i})
    fprintf('\n')
    %Ignore test folders
    if i~=1
        if ~contains(folders{i},'Trial5') && contains(folders{i-1},'Trial5')
            remove_ind=[i];
        end
    end
end

if exist('remove_ind','var') == 1
    folders=folders(1:remove_ind-1);
end    
    

answer = questdlg('Does this day need Novelty included?', ...
	'Select one', ...
	'Yes','No','No');
% Handle response
switch answer
    case 'Yes'
        if length(folders)> 12
                         error('There are more folders than expected. Stop and check why.')
        end        


        if length(folders)< 12
           error('There are less folders than expected. Stop and check why.')
        end
        
    case 'No'
        if length(folders)> 11
             error('There are more folders than expected. Stop and check why.')
        end

        if length(folders)< 11
           error('There are less folders than expected. Stop and check why.')
        end
end    
    
    



% In case you need to remove an extra folder, you can use this example.
%    folders{9}=[];
%    folders = folders(~cellfun(@isempty, folders))

%% Check that the order is correct in the printed folder names.

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
%i=1;
f=waitbar(0,'Please wait...');
counter=0;
tic

for j=1:length(channels)
    for i=1:length(folders)-1
        
        % folders{i+1}   
        counter=counter+1;
        
        %Read presleep first.
        if i==1         
            cd(folders{i})
            % Check for a truncated folder
            if exist('truncated', 'dir')
                cd('truncated') 
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
        if exist('truncated', 'dir')
            cd ..
        end

        cd(folders{i+1})
        CD=split(cd,'/');
        % CD{end}
        
        files=dir;
        files={files.name};
        file=files(contains(files,['CH',num2str(channels(j))]));
        file=file{1};
        
        if  j==1
            signal=load_open_ephys_data_faster(file);
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

        if i==1 && j==1 %If presleep and first channel, create new folder 'merged'
            mkdir('merged')   
        end

        cd('merged')

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

