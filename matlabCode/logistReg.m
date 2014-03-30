clear;
clc;
%addpath('/home/ankit/software/liblinear-1.93/');
%load 'apPressData.mat'   % AP Press Datatset
load 'econData.mat'   % Economics Datatset

%scale the features between 0 and 1
I=Features;
for i=1:size(Features,2),
	scaledI = (I(:,i)-min(I(:,i))) ./ (max(I(:,i)-min(I(:,i))));
	Features(:,i)=scaledI;
end

sprintf('Done Scaling Features')

X=Features;
Y=labels;
reg_c=1.3;
inc=0.0001
best_c=0; max_model=0;
for iter=1:100
	options=sprintf('-s %d -c %d -v %d -q',5,reg_c,75); %liblinear options
	model = train(Y,sparse(X), options);    %liblinear call
	%options=sprintf('-s %d -c %d -v %d -q',0,reg_c,75); %libsvm options
	%model = svmtrain(Y,X, options);     %libsvm call
	if max_model<model,
		best_c=reg_c;
		max_model=model;
	end
	reg_c=reg_c+inc;
	plot(iter,100-model,'LineWidth',2,'MarkerSize',10,'Marker','*');
	drawnow;
	hold on;
end












%{
sprintf('Finding  parameters through cross validation')
rng('default') % for reproducibility
[B,FitInfo] = lassoglm(X,Ybool,'binomial',...
    'NumLambda',75,'CV',25);
    
lassoPlot(B,FitInfo,'PlotType','CV');


indx = FitInfo.Index1SE;
B0 = B(:,indx);
nonzeros = sum(B0 ~= 0)

cnst = FitInfo.Intercept(indx);
B1 = [cnst;B0];

preds = glmval(B1,X,'logit');
hist(Ybool - preds) % plot residuals
title('Residuals from lassoglm model')

Ypred=preds;
Ypred(find(Ypred <=0.5))=0;
Ypred(find(Ypred >0.5))=1;
length(find(Ypred==Ybool))
%}