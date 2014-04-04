clear;
clc;
%addpath('/home/ankit/software/liblinear-1.93/');
%load('apPressData.mat');   % AP Press Datatset
%load('apPressData.mat');
%load('econData.mat');   % Economics Datatset
%Ts=load('econData.mat'); 

Ts=load('iaBooksData.mat');
load('nyTimesData.mat')

%scale the Training features between 0 and 1
I=Features;
for i=1:size(Features,2),
	scaledI = (I(:,i)-min(I(:,i))) ./ (max(I(:,i)-min(I(:,i))));
	Features(:,i)=scaledI;
end

%scale the Testing features between 0 and 1
I=Ts.Features;
for i=1:size(Ts.Features,2),
	scaledI = (I(:,i)-min(I(:,i))) ./ (max(I(:,i)-min(I(:,i))));
	Ts.Features(:,i)=scaledI;
end

sprintf('Done Scaling Features')

X=Features;
Y=labels;
ts_data=Ts.Features;
ts_labels=Ts.labels;
c=0.1667^-1;
classifier=6;
best_c=0; max_model=0;


	%LIBLINEAR
	%---------------------------------------------------------------------------------------
	%options=sprintf('-s %d -c %d -v %d -q',5,reg_c,75); %liblinear  crossvalidation options
	options=sprintf('-s %d -c %d -q -B 1 ',classifier,c);   %liblinear  training options

	model = train(Y,sparse(X), options);    %liblinear call
	[predicted_label, accuracy, prob_estimates] = predict(ts_labels, sparse(ts_data), model,'-b 1');
	
	%LIBSVM
	%---------------------------------------------------------------------------------------
	%options=sprintf('-s %d -c %d -q',0,c); %libsvm options
	%model = svmtrain(Y,X, options);     %libsvm call
	%[predict_label, accuracy, prob_estimates] = svmpredict(ts_labels, ts_data, model);
	
	
	
