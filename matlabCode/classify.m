
load('iaBooksData.mat');
Ts=load('nyTimesData.mat');

start=1;
uptil=18;
reg_c=20;

start2=1;
uptil2=18;

Features=[Features(:,start:uptil);Ts.Features(:,start2:uptil2)];
%Features=[Features(:,start:uptil), Features(:,11:18); Ts.Features(:,start2:uptil2),Ts.Features(:,11:18)];
labels=[labels;Ts.labels];


%Features=Features(:,start:uptil);
%Features=[Features(:,start:uptil), Features(:,11:18)];
Fea=scale_Features(Features);

[max_model,c]=L1LogitCV(Fea,labels,reg_c)