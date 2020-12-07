%% Start by going to the Study day folder 
%You need Adritools in your Matlab path. Else Matlab won't recognize'getfolder'.

%Sampling freq:
fs=30000; %Can be different for some OS rats.
%%
%Get trial folders 

folders=getfolder;

folders=folders(or(contains(folders,'Pre'),contains(folders,'Trial')) );
%folders=folders(or(contains(folders,'Pre'),contains(folders,'Post')) );

for i=1:length(folders)
    folders{i}
    %Ignore test folders
    if i~=1
        if ~contains(folders{i},'Trial5') && contains(folders{i-1},'Trial5')
            remove_ind=[i];
        end
    end
end

folders=folders(1:remove_ind-1);
%% Check that the order is correct in the printed folder names.

%% Select channels to merge
% channels=[52,53,59,58,49,51,46,47,48,12,31,13,30,10,11,32,4,3,2,9,6,5,22,25,23,24,20,21,27,26,17,28,18,19
%     ];
%%
channels=[ ...
14,29,15,16 ...
63,45,62,44 ...
42,64,33,43 ...
36,35,41,34 ...
40,39,38,37 ...
54,55,57,56 ...
52,53,59,58 ...
49,60,50,51 ...
46,61,47,48 ...
12,31,13,30 ...
10,11,32,1 ...
4,3,2,9 ...
8,6,5,7 ...
22,25,23,24 ...
20,21,27,26 ...
17,28,18,19
];
%%
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
    CD=split(cd,'/');
    CD{end}
    files=dir;
    files={files.name};
    file=files(contains(files,['CH',num2str(channels(j)),'_']));
    file=file{1};
if  j==1   %Only run with the first channel.
    signal=load_open_ephys_data_faster(file);
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
cd(folders{i+1})
CD=split(cd,'/');
CD{end}
files=dir;
files={files.name};
file=files(contains(files,['CH',num2str(channels(j)),'_']));
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
%% Now that file has been saved read again.


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
Trial_durations.Properties.VariableNames=[{'Unit'} folders];
writetable(Trial_durations,strcat('Trial_durations.xls'),'Sheet',1,'Range','A1:Z50')
save('trials_durations_samples.mat','trial_durations')
end

 cd ..
end
toc