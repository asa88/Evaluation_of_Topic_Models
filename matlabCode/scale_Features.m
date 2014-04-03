function  Features=scale_features(Features)

I=Features;
for i=1:size(Features,2),
	scaledI = (I(:,i)-min(I(:,i))) ./ (max(I(:,i)-min(I(:,i))));
	Features(:,i)=scaledI;
end