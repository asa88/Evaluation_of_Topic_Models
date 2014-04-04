function  Features=scale_features(Features)

fea=Features;
for i=1:size(Features,2),
	scaledI = (fea(:,i)-min(fea(:,i))) ./ (max(fea(:,i)-min(fea(:,i))));
	%scaledI=(fea(:,i)-mean(fea(:,i)))./std(fea(:,1));
	Features(:,i)=scaledI;
end
