
%load('iaBooksData.mat');
load('nyTimesData.mat');

start=5;
uptil=10;
reg_c=40;

start2=1;
uptil2=18;

%Features=[Features(:,start:uptil);Ts.Features(:,start2:uptil2)];
%Features=[Features(:,start:uptil), Features(:,11:18); Ts.Features(:,start2:uptil2),Ts.Features(:,11:18)];
%labels=[labels;Ts.labels];


Features=Features(:,start:uptil);
%Features=[Features(:,start:uptil), Features(:,11:18)];
Fea=scale_Features(Features);

[max_model,c,model]=L1LogitCV(Fea,labels,reg_c)
