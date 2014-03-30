
load 'apPressData.mat'


lambda = 0.0001*ones(9+1,1);
pred=[];
% Find Maximum value for regularization parameter and pick step increment
[f,g] = SquaredError(zeros(nVars,1),Features,y);
lambdaMax = max(abs(g));
lambdaInc = .01;



m=size(Features,1);
for mult = 1-lambdaInc:-lambdaInc:lambdaInc
    lambda = [0;mult*lambdaMax*ones(10,1)];
	for i=1:m, % for LOO cross validation
	
		X=Features;
		X = [ones(size(X,1),1), X]; % Add Bias element to features
		y=labels;
	
		test=X(i,:);
		test_label=labels(i); 
		X(i,:)=[];
		y(i)=[];
	
		funObj = @(w)LogisticLoss(w,X,y);
		w_init = zeros(size(X,2),1);

		% Maximum Likelihood
		fprintf('\nComputing Maximum Likelihood Logistic Regression Coefficients\n');
		mfOptions.Method = 'newton';
		wLogML = minFunc(funObj,w_init,mfOptions);

	
		% L1-Regularized Logistic Regression
		fprintf('\nComputing L1-Regularized Logistic Regression Coefficients...\n');
		wLogL1 = L1General2_PSSgb(funObj,w_init,lambda);
	
	
		pred=[pred;sign(test*wLogL1)];
	end
end
acc=length(find(pred==labels))
