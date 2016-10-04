#from: https://github.com/hennymac/Algorithms1/tree/master/Week4
#but cannot reset the stack size

from collections import defaultdict
import resource
import sys

#set rescursion limit and stack size limit
# resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
# sys.setrecursionlimit(10**6)


class Track(object):
    """Keeps track of explored, time, source, leader, et cetera"""
    def __init__(self,explored):
        self.explored = explored
        self.current_time = 0
        self.current_source = None
        self.leader = defaultdict(list)
        self.finish_times = {}

    def addNode(self,node):
        """adds node to SCC group"""
        self.leader[self.current_source] += [node]

def dfs(graph,start,track):
    track.explored[start] = True
    track.addNode(start)
    for edge in graph[start]:
        if not track.explored[edge]:
            dfs(graph,edge,track)
    track.current_time += 1
    track.finish_times[start] = track.current_time


def dfs_loop(graph,nodes,track):
    for node in nodes:
        if not track.explored[node]:
            track.current_source = node
            dfs(graph,node,track)


def scc(graph,reverse_graph,nodes):

    explored = [False for i in range(len(nodes))]
    track = Track(explored)
    dfs_loop(reverse_graph,nodes,track)
    sorted_nodes = sorted(track.finish_times, key=track.finish_times.get,reverse=True)
    explored = [False for i in range(len(nodes))]
    track = Track(explored)
    dfs_loop(graph,sorted_nodes,track)
    return track


def loaddata(filename):

    with open(filename,"r") as f:
        edges = [map(int,line.split()) for line in f]

    nodes = list(set([v-1 for edge in edges for v in edge]))
    G = {i: [] for i in range(len(nodes))}
    Grev = {i: [] for i in range(len(nodes))}
    for edge in edges:
        G[edge[0]-1] += [edge[1]-1]
        Grev[edge[1]-1] += [edge[0]-1]

    return G,Grev,nodes

def main():
    filename = '../large_data_files/SCC.txt'
    # filename = '33300.txt'

    G,Grev,nodes = loaddata(filename)

    scc_dict = scc(G,Grev,nodes).leader
    scc_size = []
    for key, value in scc_dict.items():
        scc_size.append(len(value))
    print sorted(scc_size, reverse=True)[:5]


if (__name__ == '__main__'):
    main()
