'''
Created on Mar 18, 2014

@author: ankit
'''


''' Dependencies for the class'''
import re
from collections import defaultdict
import networkx as nx

import sys
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
#sys.path.append('/usr/lib64/graphviz/python/')
import gv

''' Graph Library '''
# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import depth_first_search
from pygraph.algorithms.minmax import minimal_spanning_tree
from pygraph.readwrite.dot import write



class BuildGraph(object):
    '''
    classdocs
    '''
    Graph=[]
    GraphEdges=defaultdict(list)
    notFound=open('WordNotFound.txt','a') #file containing missing words
    topics={}  # contains topic words present in the graph and their IDs
    matches=0 # words in Graph/Total WOrds
    topicEdges=defaultdict(list)
    gr=nx.Graph()   # graph object
    G=nx.Graph()
    Gs=nx.Graph()
    SpanG=nx.Graph()
    #Features
    gM_connComp=0
    gM_sizeMaxComp=0
    gM_maxDeg=0
    shortestPath=[]
    
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
    def loadGraph(self,fileObj):
        for line in fileObj:
            self.Graph.append(line.split()[1])
            try:
                self.G.add_node(line.split()[1].lower())
            except:
                pass
        self.Graph= map(str.lower,self.Graph) # convert everything to lower
        return
    
    def loadGraphEdgesTopicEdges(self,edgeObj):
        for line in edgeObj:
            temp=line.split()
            self.GraphEdges[temp[0]].append(temp[1:]) 
            
            # if the id in the graph is in the topics append projection topic graph
            if self.Graph[int(temp[0])] in self.topics.keys():
                key=self.Graph[int(temp[0])]
                self.topicEdges[key].append(self.Graph[int(temp[1])])
        return
    
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
                if item in self.Graph:
                    match_count+=1
                    self.topics[item]=self.Graph.index(item) #store id of that keywords
                else:
                    self.notFound.write(item+'\n')
        print 'Total no of matches found ' + str(match_count) +' out of ' + str(word_count)+' for ApPress Dataset'
        self.matches= float(match_count)/word_count
        return
        




# This would be the main function accessing the class
#------------------------------------------------------------------------------------

    def buildProjectionGraph(self,edgeObj):        
        #Create the projection graph
        for key in self.topics:
            try:
                self.gr.add_nodes(key)
            except:
                pass
        # Create the main Graph
        
        
        #Add edges to the graph
        for line in edgeObj:
            temp=line.split()           
            # if the id in the graph is in the topics append projection topic graph
            key=self.Graph[int(temp[0])]
            sibling=self.Graph[int(temp[1])]
            try:
                self.G.add_edge(key,sibling)
            except:
                pass
            if self.Graph[int(temp[0])] in self.topics.keys():
                if sibling in self.topics.keys():
                    try:
                        self.gr.add_edge(key,sibling)
                    except:
                        pass
        print "Done adding edges"         
        return
            
    def ProjectionFeatures(self):
        closed=[]
        print "in ProjectionFeatures"
        for node in self.gr.nodes():
            if node not in closed:
                #st,pre,post=depth_first_search(self.gr, root=node)
                x=nx.dfs_preorder_nodes(self.G[node])
                pre=list(x)
                closed=closed + pre            
                self.gM_connComp=  self.gM_connComp+1
                if len(pre)>self.gM_sizeMaxComp:
                    self.gM_sizeMaxComp=len(pre)
            if self.gM_maxDeg < len(self.gr.neighbors(node)):
                    self.gM_maxDeg=len(self.gr.neighbors(node))
                    
        print "Number of connected components"
        print self.gM_connComp
        print "max size of a connected components"
        print self.gM_sizeMaxComp
        print "max no of nodes"
        print self.gM_maxDeg
    
    
    def SpanningFeatures(self):
      
        closed=[]
        count=0
        tempG=nx.Graph()
        for node in self.gr.nodes():
            try:
                tempG.add_node(node)
            except:
                pass
        
        for source in self.gr.nodes():
            for target in self.gr.nodes():
                if source!=target and [source,target] not in closed:
                    path=nx.shortest_path(self.G, source, target)
                    self.shortestPath.append(path)
                    closed.append([source,target])
                    closed.append([target,source])
                    tempG.add_edge(source, target, len(path)-1)
                    for i in range(0,len(path)):
                        try:
                            self.Gs.add_node(path[i])
                            if i!=len(path):
                                self.Gs.add_edge(path[i],path[i+1])
                        except:
                            pass
        self.SpanG=nx.minimum_spanning_tree(self.Gs)
                    
        #Compute Features
       
        
       # self.gS_avgMSTWeight=float(weight)/count
                    
        return
           
            
            
            
        
            
        
''' contains location of the graph'''
Graph_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-network.labels.csv'
GraphEdges_path='/home/ankit/Dropbox/14-topics-semantics/en-network/en-network.edges'
f = open(Graph_path,'r')
f1= open(GraphEdges_path,'r')
Data = BuildGraph()
print "starting Program"
Data.loadGraph(f)

print "Done building the Graph"

#compare how similar are words between Graph and data
data_path='/home/ankit/Dropbox/14-topics-semantics/DATA/'
D1=open(data_path+'apPress100T.txt','r') #621 unique words
D2=open(data_path+'econ100T.txt','r')
D3=open(data_path+'music100T.txt','r')
D4=open(data_path+'Newman-data/nytimes.topics.txt','r')
D5=open(data_path+'Newman-data/iabooks.topics.txt','r')


Data.processTopics(D1)

#Data.loadGraphEdgesTopicEdges(f1)
Data.buildProjectionGraph(f1)
Data.ProjectionFeatures()
Data.SpanningFeatures()







