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

import matplotlib.pyplot as plt
#import sys
#sys.path.append('..')
#sys.path.append('/usr/lib/graphviz/python/')
#sys.path.append('/usr/lib64/graphviz/python/')



class MineFeatures(object):
    '''
    classdocs
    '''
    
    notFound=open('WordNotFound.txt','a') #file containing missing words
    Feature_file=open('Features.txt','a')
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
        #reintizalize all spanning feature
        self.gS_avgMSTWeight=0;self.gS_RatioC=0
        self.gS_MaxDegreeM=0;self.gS_MaxDegreeC=0
        self.gS_AvgDegree=0;self.gS_Density=0
         
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
                        self.gM.add_edge(node,item)
                    except:
                        pass
        nx.draw(self.gM)    
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
        
        #print self.gM_connComp
        #print self.gM_maxDeg
        #print self.gM_sizeMaxComp

        
        return
    
    '''Build spanning graph fro feature calculation'''
    def calc_SpanningFeatures(self):
        self.gS.add_nodes_from(self.gM.nodes())
        self.gS_w.add_nodes_from(self.gM.nodes())
        
        
        closed=[] 
        
        path_len=0
        for source in self.gM.nodes():
            for target in self.gM.nodes():
                if source!=target and [source,target] not in closed:
                    path=nx.shortest_path(self.G, source, target)
                    
                    #append used nodes to closed
                    closed.append([source,target])
                    closed.append([target,source])
                    
                    self.gS.add_nodes_from(path[1:len(path)-1])
                    path_len= len(path)-1
                    
                    #add weighted edges to weighted graph
                    self.gS_w.add_edge(source,target,weight=path_len)
                    
                    #add adges to normal spanning graph
                    for i in range(0,len(path)-1):
                        try:
                            self.gS.add_edge(path[i],path[i+1])
                        except:
                            pass
        
        self.gS=nx.minimum_spanning_tree(self.gS)
        self.gS_w=nx.minimum_spanning_tree(self.gS_w)
        
        
        #time to build spannning features
        self.updateSpanningFeatures()
        
       
        return
        
    
    def genFeatures(self,topicsObj):
        for line in topicsObj:
            self.gM.clear()
            self.gS.clear()
            self.gS_w.clear()
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
            plt.figure(1,figsize=(8,8))
            
            self.calc_SpanningFeatures()
            
            # layout graphs with positions using graphviz neato
            pos=nx.graphviz_layout(self.gS,prog="neato")
            # color nodes the same in each connected subgraph
            C=nx.connected_component_subgraphs(self.gS)
            nx.draw(self.gS,
             pos,
             node_size=500,
             vmin=0.0,
             vmax=1.0,
             with_labels=True
             )
           
            plt.savefig("atlas.png",dpi=75)
            exit()
           
            
            ''' Concatenate features and write to the File'''
            fea=str(self.misses)+' '+ str(self.gM_connComp) + ' ' +str(self.gM_sizeMaxComp) + ' ' + str(self.gM_maxDeg)
            fea1= str(self.gS_avgMSTWeight) +' ' + str(self.gS_RatioC) + ' ' + str(self.gS_MaxDegreeC) + ' ' + str(self.gS_MaxDegreeM)+ ' ' +str(self.gS_AvgDegree) + ' ' + str(self.gS_Density)
            f=fea+' ' +fea1
            self.Feature_file.write(f+'\n')
    
        print "Done writing"
        self.Feature_file.close()
       
        return
                
    '''
    def processTopics(self,topicsObj):
        match_count=0
        word_count=0
        for line in topicsObj:
            line=line.rstrip('\r\n')
            temp=re.findall(r"[\w']+",line)
            temp= map(str.lower,temp) #convert all words to lowerccase
            #temp= temp[1:] # comment line when running fr regular dataset
            for item in temp:
                word_count+=1
                if self.G.has_node(item):
                    match_count+=1
                    #  self.topics[item]=self.Graph.index(item) #store id of that keywords
                else:
                    self.notFound.write(item+'\n')
        print 'Total no of matches found ' + str(match_count) +' out of ' + str(word_count)+' for ApPress Dataset'
        self.matches= float(match_count)/word_count
        return
        '''





            
            
            
        
            
        
''' contains location of the graph'''
Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-network.labels.csv'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-network.edges'
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


Data.genFeatures(D4)
'''
#Data.loadGraphEdgesTopicEdges(f1)
Data.buildProjectionGraph(f1)
Data.ProjectionFeatures()
Data.SpanningFeatures()
'''






