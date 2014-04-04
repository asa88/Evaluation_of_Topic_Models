function [max_model,best_c,model]= L1LogitCV(X,Y,reg_c)


inc=0.2;
best_c=0; max_model=0;
cv=[]; c_val=[];
classifier=6;
%for iter=5:-5,	
while(1/reg_c<=1)
	%reg_c=2^iter;
	%LIBLINEAR
	%---------------------------------------------------------------------------------------
	options=sprintf('-s %d -c %d -v %d  -q -B 1',classifier,reg_c,75); %liblinear  crossvalidation options
	model = train(Y,sparse(X), options);    %liblinear call
		
	%LIBSVM
	%---------------------------------------------------------------------------------------
	
	%options=sprintf('-s %d -c %d -v %d -q',0,reg_c,75); %libsvm options
	%model = svmtrain(Y,X, options);     %libsvm call
	
	if max_model <= model,
		best_c=1/reg_c;
		max_model=model;
	end
	cv=[cv;model];
	c_val=[c_val;1/reg_c];
	reg_c=reg_c-inc;
	

end
	
	figure;
	plot(c_val,100-cv,'LineWidth',1);
	axis([min(c_val) max(c_val) min(100-cv) max(100-cv)])
	title('Parameter Selection through cross-validation');
	xlabel('value of C (regualriztion parameter)');
	ylabel('Cross-validation error');
	
	
options=sprintf('-s %d -c %d -q -B 1',classifier,best_c^-1);
	model = train(Y,sparse(X), options);    %liblinear call
	
