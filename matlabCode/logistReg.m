clear;
clc;

load 'apPressData.mat'

%{
%scale the features between 0 and 1
I=Features;
for i=1:size(Features,2),
	scaledI = (I(:,i)-min(I(:,i))) ./ (max(I(:,i)-min(I(:,i))));
	Features(:,i)=scaledI;
end
%}
sprintf('Done Scaling Features')

X=Features;
Ybool=labels;
Ybool(find(Ybool==-1))=0;

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