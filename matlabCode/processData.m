%Y=load('/home/ankit/Dropbox/14-topics-semantics/DATA/Newman-data/iabooks.eval.txt');
Y=load('/home/ankit/Dropbox/14-topics-semantics/DATA/Newman-data/nytimes.eval.txt');

avg_rating=sum(Y')/9;

avg_rating(find(avg_rating <1.5))=1;
avg_rating(find(avg_rating >=1.5))= -1;


labels=avg_rating';
%Features=load('Features_iaBooks.txt');
Features=load('Features_nyTimes.txt');

%save('iaBooksData.mat','Features','labels');
save('nyTimesData.mat','Features','labels');
