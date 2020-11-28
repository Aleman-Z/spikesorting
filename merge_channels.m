%Get folders

folders=getfolder;

folders=folders(or(contains(folders,'Pre'),contains(folders,'Trial')) );
%folders=folders(or(contains(folders,'Pre'),contains(folders,'Post')) );

for i=1:length(folders)
    folders{i}
end


%% Identify channels to merge
channels=[52,53,59,58,49,51,46,47,48,12,31,13,30,10,11,32,4,3,2,9,6,5,22,25,23,24,20,21,27,26,17,28,18,19
    ];
%%
clc
%i=1;
f=waitbar(0,'Please wait...');
counter=0;
for j=1:length(channels)
for i=1:length(folders)-1
% folders{i+1}   
counter=counter+1;
%Read presleep first.
if i==1
    cd(folders{i})
    cd
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

end

%Read next (post)trial
cd ..
cd(folders{i+1})
cd
files=dir;
files={files.name};
file=files(contains(files,['CH',num2str(channels(j)),'_']));
file=file{1};


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
 cd ..
end