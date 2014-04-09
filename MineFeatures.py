'''
Created on Mar 21, 2014

@author: ankit
'''
'''
Created on Mar 18, 2014

@author: ankit
'''


''' Dependencies for the class'''
import re
import networkx as nx
import os

#import matplotlib.pyplot as plt
#import pydot
#import pygraphviz as pgv
#import sys
#sys.path.append('..')
#sys.path.append('/usr/lib/graphviz/python/')
#sys.path.append('/usr/lib64/graphviz/python/')



class MineFeatures(object):
    '''
    classdocs
    '''
    
    notFound=open('WordNotFound.txt','w+') #file containing missing words
   
    misses=0 # words in Graph/Total WOrds
   
    
    G=nx.Graph()    #BRYAN'S GRAPH
    G_Id={}
    gM=nx.Graph()   #  Projecttion graph object
    gS=nx.Graph()   # SPanning graph for topics with connector nodes
    gS_w=nx.Graph() # Spanning graph with weights (frm shortest distance)
    
    #Projection Features
    gM_connComp=0
    gM_sizeMaxComp=0
    gM_maxDeg=0
   
    #Spanning Features
    gS_avgMSTWeight=0
    gS_RatioC=0
    gS_MaxDegreeM=0
    gS_MaxDegreeC=0
    gS_AvgDegree=0
    gS_Density=0
    
    #Shortest Path Features"
    
    NumNoPath=0
    AvgSPlen=0
    MaxSPlen=0
    NumSP1=0
    NumSP2=0
    NumSP3=0
    NumSP4=0
    NumSP5=0
    NumSPm=0 # for length > 5
   

    def __init__(self):
        '''
        Constructor
        '''
        return
    ''' Build the Bryan's Graph'''
    
    
    def is_empty(self,any_structure):
        if any_structure:
            #print('Structure is not empty.')
            return False
        else:
            #print('Structure is empty.')
            return True
        
    '''Load Bryan's graph'''
    def loadGraph(self,fileObj):
        for line in fileObj:
            try:
                self.G.add_node(line.split()[1].lower())
                self.G_Id[int(line.split()[0].lower())]=line.split()[1].lower()
            except:
                pass
        return
    
    '''Add edges to the Bryan's Graph'''
    def loadEdges(self,edgeObj):
        for line in edgeObj:
            temp=line.split()    
            key=int(temp[0])
            sib_key=int(temp[1])
            try:
                self.G.add_edge(self.G_Id[key],self.G_Id[sib_key])
            except:
                pass
        return
        
    def updateSpanningFeatures(self):
         
        #Avg,Max Degree of orignal and connector nodes feature
        neighbours=0.0
        for node in self.gS.nodes():
            temp=self.gS.neighbors(node)
            neighbours+=len(temp)
            
            #check if node is orignal
            if self.gM.has_node(node):
                if len(temp)>self.gS_MaxDegreeM:
                    self.gS_MaxDegreeM=len(temp)
            else:
                if len(temp)>self.gS_MaxDegreeC:
                    self.gS_MaxDegreeC=len(temp)
                
        self.gS_AvgDegree=neighbours/self.gS.order()
        
        # Average Weight
        weight=0.0
        edges=self.gS_w.edges(data=True)
        for item in edges:
            if not self.is_empty(item[2]):
                weight+=item[2]['weight']    
        self.gS_avgMSTWeight=weight/len(edges)
            
        #ratio
        self.gS_RatioC=float(self.gS.order()-self.gM.order())/self.gM.order()
        
        #Density
        noOfNodes=self.gS.order()
        self.gS_Density=float(len(self.gS.edges()))/(noOfNodes*(noOfNodes-1))
        return
        
    ''' Projection Features'''
    #Double checked they are working right :)
    def calc_ProjFeatures(self):
        #Add edges to projection Graph
        for node in self.gM.nodes():
            neighbours=self.G.neighbors(node)
            for item in neighbours:
                if self.gM.has_node(item):
                    try:
                        if node!=item:
                            self.gM.add_edge(node,item)
                    except:
                        pass
        
           
        #Initialize and Calculate features
        closed=[];self.gM_connComp=0;
        self.gM_maxDeg=0;self.gM_sizeMaxComp=0
        
        for node in self.gM.nodes():
            if node not in closed:
                x=nx.dfs_preorder_nodes(self.gM,node)
                pre=list(x)                
                closed=closed +pre      
                self.gM_connComp=  self.gM_connComp+1
                if len(pre)>self.gM_sizeMaxComp:
                    self.gM_sizeMaxComp=len(pre)
            if self.gM_maxDeg < self.gM.degree(node):
                    self.gM_maxDeg=self.gM.degree(node)
        return
    
    
    def update_SPfeatures(self,path):
        self.AvgSPlen+=len(path)-1
        
        p_len=len(path)-1
        
        if p_len==1:
            self.NumSP1+=1
        if p_len==2:
            self.NumSP2+=1
        if p_len==3:
            self.NumSP3+=1
        if p_len==4:
            self.NumSP4+=1
        if p_len==5:
            self.NumSP5+=1
        if p_len>5:
            self.NumSPm+=1
        if p_len>self.MaxSPlen:
            self.MaxSPlen=p_len
                
        return
        
    
    '''Build spanning graph fro feature calculation'''
    def calc_SpanningFeatures(self,path,count):
        self.gS.add_nodes_from(self.gM.nodes())
        self.gS_w.add_nodes_from(self.gM.nodes())
        
        
        closed=[] 
        
        path_len=0
        sp_count=0
        
        #open file to write shortes paths
        path_file=open(os.getcwd()+path+'shortestPath/SP_'+str(count)+'.txt','w+')
                   
        for source in self.gM.nodes():
            for target in self.gM.nodes():
                if source!=target and [source,target] not in closed:
                    path=nx.shortest_path(self.G, source, target)
                    sp_count+=1
                    for item in path:
                        path_file.write(item+' ') #update path txt file
                    path_file.write('\n')
                    self.update_SPfeatures(path)
                    
                    #append used nodes to closed
                    closed.append([source,target])
                    closed.append([target,source])
                    path_len= len(path)-1
                    
                    #write discovered paths to file for refrence
                                
                    #add weighted edges to weighted graph
                    self.gS_w.add_edge(source,target,weight=path_len)
                   
        #update the value of average
        self.AvgSPlen=self.AvgSPlen/sp_count
        path_file.close()
        
        #self.gS=nx.minimum_spanning_tree(self.gS)
        self.gS_w=nx.minimum_spanning_tree(self.gS_w)
        
        for node in self.gS_w.nodes():
            friends=self.gS_w.neighbors(node)
            for friend in friends:
                path=nx.shortest_path(self.G,node,friend)
                for i in range(0,len(path)-1):
                        self.gS.add_edge(path[i],path[i+1])     
        
        #time to build spannning features
        self.updateSpanningFeatures()
        
       
        return
        
    def clearVars(self):
        #clear variable for each run
        self.gM.clear()
        self.gS.clear()
        self.gS_w.clear()
        self.AvgSPlen=0;self.NumSP1=0; self.NumSP2=0;self.NumSP3=0;
        self.NumSP4=0;self.NumSP5=0;self.NumSPm=0
        self.MaxSPlen=0
        
        #Projection Features
        self.gM_connComp=0
        self.gM_sizeMaxComp=0
        self.gM_maxDeg=0
       
        #Spanning Features
        self.gS_avgMSTWeight=0
        self.gS_RatioC=0
        self.gS_MaxDegreeM=0
        self.gS_MaxDegreeC=0
        self.gS_AvgDegree=0
        self.gS_Density=0
        
        
        return
    
    
    def plot_graphs(self,path,count):
        '''Save graphs'''
        Gs=nx.to_agraph(self.gS)
        Gm=nx.to_agraph(self.gM)
        Gs_w=nx.to_agraph(self.gS_w)
        
        #add color to main nodes
        for node in self.gM.nodes():
            n=Gs.get_node(node)
            n.attr['shape']='box'
            n.attr['style']='filled'
            n.attr['fillcolor']='turquoise'
            
        #add weight to edges    
        for edge in self.gS_w.edges(data=True):
            ed=Gs_w.get_edge(edge[0],edge[1])
            ed.attr['label']=edge[2]['weight'] 
        
        loc= os.getcwd()+path+'/spanning/gS' + str(count)+'.png'
        loc1= os.getcwd()+path+'/projection/gM' + str(count)+'.png' 
        loc2= os.getcwd()+path+'/spanning_w/gS_w' + str(count)+'.png' 
        
        Gs.layout(prog='dot') # use dot
        Gm.layout(prog='dot') # use dot
        Gs_w.layout(prog='dot')
        
        Gs.draw(loc)
        Gm.draw(loc1)
        Gs_w.draw(loc2)
                  
        return
        
        
    
    def genFeatures(self,topicsObj,path):
        Feature_file=open(os.getcwd()+path+'Features.txt','w+')
        count=1
        for line in topicsObj:
            self.misses=0
            temp=re.findall(r"[\w']+",line)
            temp= map(str.lower,temp)
            temp= temp[1:] # comment this line when not running fr newman Data
            for item in temp:
                if item in self.G.nodes():   # check if item is in graph
                    self.gM.add_node(item)
                else:
                    self.misses+=1
            
            '''Feature Calculation'''
            self.calc_ProjFeatures()
            self.calc_SpanningFeatures(path,count)
            
            '''Plot Graphs'''
            #self.plot_graphs(path,count)
            count+=1 
           
            
            ''' Concatenate features and write to the File '''
            fea=str(self.misses)+' '+ str(self.gM_connComp) + ' ' +str(self.gM_sizeMaxComp) + ' ' + str(self.gM_maxDeg)
            fea1= str(self.gS_avgMSTWeight) +' ' + str(self.gS_RatioC) + ' ' + str(self.gS_MaxDegreeM) + ' ' + str(self.gS_MaxDegreeC)+ ' ' +str(self.gS_AvgDegree) + ' ' + str(self.gS_Density)
            fea2=str(self.AvgSPlen)+' ' +str(self.MaxSPlen)+ ' '+str(self.NumSP1)+' '+ str(self.NumSP2)+' '+str(self.NumSP3)+' '+str(self.NumSP4)+' '+str(self.NumSP5)+' '+str(self.NumSPm)
            f=fea+' ' +fea1 + ' '+ fea2
            Feature_file.write(f+'\n')
           
            ''' CLEAR ALL FEATURE VARS'''
            self.clearVars()
            
            
    
        print "Done writing"
        Feature_file.close()
       
        return
                





            
            
            
        
            
        
''' contains location of the graph'''

'''OLD GRAPH'''
'''
Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-network.labels.csv'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-network.edges'
'''

'''En-10 GRAPH'''
'''
Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en_10-normed/en.labels'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-10_normed/en-10_normed.edges'
'''

'''En-20 GRAPH'''
'''
Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-20_normed/en.labels'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-20_normed/en-20_normed.edges'
'''


'''En-40 GRAPH'''

Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-40_normed/en.labels'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-40_normed/en-40_normed.edges'


'''En-40_100k GRAPH'''
'''
Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-100k/en-100k.labels'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-100k/en-40_normed_100k.edges'
'''


f = open(Graph_path,'r')
f1= open(GraphEdges_path,'r')
Data = MineFeatures()
print "starting Program"
Data.loadGraph(f)
Data.loadEdges(f1)


print "Done building the Graph"

#compare how similar are words between Graph and data
data_path='/home/ankit/Dropbox/14-topics-semantics/DATA/'
D1=open(data_path+'apPress100T.txt','r') #621 unique words
D2=open(data_path+'econ100T.txt','r')
D3=open(data_path+'music100T.txt','r')
D4=open(data_path+'Newman-data/nytimes.topics.txt','r')
D5=open(data_path+'Newman-data/iabooks.topics.txt','r')

book_path='/Data/iaBooks/graphs/'
news_path='/Data/NYtimes/graphs/'
Data.genFeatures(D5,book_path)
Data.genFeatures(D4,news_path)
'''
#Data.loadGraphEdgesTopicEdges(f1)
Data.buildProjectionGraph(f1)
Data.ProjectionFeatures()
Data.SpanningFeatures()
'''






