#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <sstream>
#include <algorithm>

using namespace std;

vector<vector<int>> adjList; // Adjacency list representation
int numVertices;

// Function to read the graph from a file
void readGraphFromFile(const string &filename) {
    ifstream infile(filename);
    if (!infile) {
        cerr << "Error: Unable to open file!\n";
        exit(1);
    }

    string line;
    bool readingAdjacencyList = false;
    int vertex = 0;

    while (getline(infile, line)) {
        if (line.find("//") == 0) continue; // Skip comments

        if (!readingAdjacencyList) {
            numVertices = stoi(line); // Read number of vertices
            adjList.resize(numVertices);
            readingAdjacencyList = true;
        } else {
            stringstream ss(line);
            int neighbor;
            while (ss >> neighbor) {
                adjList[vertex].push_back(neighbor);
            }
            vertex++;
        }
    }
    infile.close();
}

// Function to identify the clique and independent set
void identifyCliqueAndIndependentSet(set<int> &clique, set<int> &independentSet) {
    for (int i = 0; i < numVertices; i++) {
        if (adjList[i].size() == numVertices - 1) {
            clique.insert(i); // If it connects to all others, it's in the clique
        } else {
            independentSet.insert(i);
        }
    }
}

// Function to find the minimum dominating set
set<int> findMinDominatingSet() {
    set<int> clique, independentSet;
    identifyCliqueAndIndependentSet(clique, independentSet);

    set<int> dominatingSet;

    // Step 1: If an independent set vertex has no neighbor in C, add it to the MinDS
    for (int v : independentSet) {
        bool hasNeighborInC = false;
        for (int neighbor : adjList[v]) {
            if (clique.count(neighbor)) {
                hasNeighborInC = true;
                break;
            }
        }
        if (!hasNeighborInC) {
            dominatingSet.insert(v);
        }
    }

    // Step 2: Greedily select minimum subset of C to dominate I
    set<int> covered;
    for (int v : independentSet) {
        for (int neighbor : adjList[v]) {
            if (clique.count(neighbor)) {
                covered.insert(v);
            }
        }
    }

    while (covered.size() < independentSet.size()) {
        int bestNode = -1, maxCover = 0;
        for (int c : clique) {
            int count = 0;
            for (int v : independentSet) {
                if (adjList[v].size() > 0 && covered.find(v) == covered.end() && find(adjList[v].begin(), adjList[v].end(), c) != adjList[v].end()) {
                    count++;
                }
            }
            if (count > maxCover) {
                maxCover = count;
                bestNode = c;
            }
        }
        if (bestNode == -1) break; // If no node found, break
        dominatingSet.insert(bestNode);
        for (int v : independentSet) {
            if (find(adjList[v].begin(), adjList[v].end(), bestNode) != adjList[v].end()) {
                covered.insert(v);
            }
        }
    }

    // Step 3: Ensure clique is dominated
    bool cliqueCovered = false;
    for (int v : clique) {
        if (dominatingSet.count(v)) {
            cliqueCovered = true;
            break;
        }
    }
    if (!cliqueCovered) {
        dominatingSet.insert(*clique.begin()); // Pick any vertex from C to dominate clique
    }

    return dominatingSet;
}

int main() {
    string filename = "graph.txt"; // Change this to your input file name
    readGraphFromFile(filename);

    set<int> minDominatingSet = findMinDominatingSet();

    cout << "Minimum Dominating Set: ";
    for (int v : minDominatingSet) {
        cout << v << " ";
    }
    cout << endl;

    return 0;
}
