// CPP Program to determine level of each node 
// and print level 
#include <iostream>
#include <vector>
#include <algorithm> 
#include <queue>
using namespace std; 
struct vertex{
    int node;
    int level;
    bool operator<(const vertex & other) const{
        return level < other.level;
    }
};
// function to determine level of each node starting 
// from x using BFS 
void printLevels(vector<int> graph[], int V, int x) 
{ 
    // array to store level of each node 
    int level[V]; 
    bool marked[V]; 
  
    // create a queue 
    queue<int> que; 
  
    // enqueue element x 
    que.push(x); 
  
    // initialize level of source node to 0 
    level[x] = 0; 
  
    // marked it as visited 
    marked[x] = true; 
  
    // do until queue is empty 
    while (!que.empty()) { 
  
        // get the first element of queue 
        x = que.front(); 
  
        // dequeue element 
        que.pop(); 
  
        // traverse neighbors of node x 
        for (int i = 0; i < graph[x].size(); i++) { 
            // b is neighbor of node x 
            int b = graph[x][i]; 
  
            // if b is not marked already 
            if (!marked[b]) { 
  
                // enqueue b in queue 
                que.push(b); 
  
                // level of b is level of x + 1 
                level[b] = level[x] + 1; 
  
                // mark b 
                marked[b] = true; 
            } 
        } 
    } 
  
    // display all nodes and their levels 
    vector<vertex> vec;
    for(int i = 0;i < V;i++){
        vertex kk = {i,level[i]};
        vec.push_back(kk);
    }
    sort(vec.begin(),vec.end());
    for(int i = 0;i <vec.size();i++){
        if(level[i] != 0){cout << vec[i].node << " " << vec[i].level << endl;}
    }
} 
  
// Driver Code 
int main() 
{ 
    // adjacency graph for tree 
    int V; cin >> V;int source; cin >> source;
    int M; cin >> M;
    vector<int> graph[V];
    // graph[0].push_back(1); 
    // graph[0].push_back(2); 
    // graph[1].push_back(3); 
    // graph[1].push_back(4); 
    // graph[1].push_back(5); 
    // graph[2].push_back(5); 
    // graph[2].push_back(6); 
    // graph[6].push_back(7);
    for(int i = 0;i < M;i++){
        int a,b; cin >> a >> b;
        a--;b--; graph[a].push_back(b);
        graph[b].push_back(a);
    }
  
    // call levels function with source as 0 
    printLevels(graph, V, source);
    return 0; 
} 
