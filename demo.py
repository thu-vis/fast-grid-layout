#! /usr/bin/python3
import os
import pickle
import json
import argparse
import numpy as np
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
import copy
import math
from tempfile import NamedTemporaryFile
from typing import List

from queue import PriorityQueue
import numpy as np
from PIL import Image

from sampling import HierarchySampling
from GridLayout import GridLayout

class DataCtrler(object):

    def __init__(self):
        super().__init__()
        self.statistic = {}
        self.labels = None
        self.preds = None
        self.features = None
        self.grider = GridLayout()
        self.sampler = HierarchySampling()
        self.trainImages = None
        self.enableTSNEBuffer = True
        
    def processStatisticData(self, data):     
        return data
    
    def processSamplingData(self, samplingPath):
        self.sampling_buffer_path = samplingPath
        
        if os.path.exists(self.sampling_buffer_path):
            self.sampler.load(self.sampling_buffer_path)
        else:
            data = self.features
            n = data.shape[0]
            d = 1
            for dx in data.shape[1:]:
                d *= dx
            data = data.reshape((n, d))
            
            labels = self.labels
            self.sampler.fit(data, labels, 0.5, 400)
            self.sampler.dump(self.sampling_buffer_path)

    def process(self, predictData = None, trainImages = None, bufferPath="/tmp/hierarchy.pkl"):
        """process raw data
        """        
        self.bufferPath = bufferPath
        
        self.statistic = {
            "names": predictData["class_names"],
            "hierarchy": [{'name':n, 'children':[{'name':n, 'children':[n]}]} for n in predictData["class_names"]]
        }

        self.labels = predictData["labels"].astype(int)
        self.preds = predictData["preds"].astype(int)
        self.features = predictData["features"]
        self.scores = predictData["scores"]
        self.confidence = np.max(self.scores, axis=1)
        
        sampling_buffer_path = os.path.join(bufferPath, "hierarchy.pkl")
        self.sampling = self.processSamplingData(sampling_buffer_path)
        
        self.trainImages = trainImages

    def getLabelHierarchy(self):
        """ hierarchy labels
        """        
        return self.statistic
   
    def getImageGradient(self, imageID: int, method: str) -> list:
        """ get gradient of image

        Args:
            imageID (int): image id
            method (str): method for feature visualization

        Returns:
            list: gradient
        """        
        if self.trainImages is not None:
            image = self.trainImages[imageID]
            return image.tolist()
        else:
            return []
        
    def gridZoomIn(self, nodes: List[int], constraints: List[List[float]], depth: int) -> dict:
        """main function of zoom in grid layout

        Args:
            nodes (List[int]): list of selected nodes
            constraints (List[List[float]]): positions of selected nodes
            depth (int): zoom in levels

        Returns:
            dict: zoom in result
        """              
        
        # cache top result in buffer to accelarate loading speed
        TSNEBufferPath = os.path.join(self.bufferPath, "tsneTop.json")
        if depth==0 and self.enableTSNEBuffer and os.path.exists(TSNEBufferPath):
            with open(TSNEBufferPath) as f:
                return json.load(f)
            
        # zoom in and sample nodes
        neighbors, newDepth = self.sampler.zoomin(nodes, depth)
        if type(neighbors)==dict:
            while True:
                newnodes = []
                for neighbor in neighbors.values():
                    newnodes += neighbor
                if len(newnodes) >= 400 or newDepth==self.sampler.max_depth:
                    break
                neighbors, newDepth = self.sampler.zoomin(newnodes, newDepth)
        zoomInConstraints = None
        zoomInConstraintX = None
        if constraints is not None:
            zoomInConstraints = []
            zoomInConstraintX = []
        zoomInNodes = []
        if type(neighbors)==list:
            zoomInNodes = neighbors
            if constraints is not None:
                zoomInConstraints = np.array(constraints)
                zoomInConstraintX = self.features[nodes]
        else:
            for children in neighbors.values():
                for child in children:
                    if int(child) not in nodes:
                        zoomInNodes.append(int(child))
            if constraints is not None:
                zoomInConstraints = np.array(constraints)
            zoomInConstraintX = self.features[nodes]
            zoomInNodes = nodes + zoomInNodes
            gridsize = int(math.sqrt(len(zoomInNodes)))
            zoomInNodes = zoomInNodes[:gridsize*gridsize]
        zoomInLabels = self.labels[zoomInNodes]
        zoomInPreds = self.preds[zoomInNodes]
        zoomInConfidence = self.confidence[zoomInNodes]

        # zoom in hierarchical labels
        def getBottomLabels(zoomInNodes):
            hierarchy = copy.deepcopy(self.statistic['hierarchy'])
            labelnames = copy.deepcopy(self.statistic['names'])
            nodes = [{
                "index": zoomInNodes[i],
                "label": zoomInLabels[i],
                "pred": zoomInPreds[i]
            } for i in range(len(zoomInNodes))]

            root = {
                'name': '',
                'children': hierarchy,
            }
            counts = {}
            for node in nodes:
                if not counts.__contains__(labelnames[node['pred']]):
                    counts[labelnames[node['pred']]] = 0
                counts[labelnames[node['pred']]] += 1

            def dfsCount(root, counts):
                if isinstance(root, str):
                    if not counts.__contains__(root): # todo
                        counts[root] = 0
                    return {
                        'name': root,
                        'count': counts[root],
                        'children': [],
                        'realChildren': [],
                        'emptyChildren': [],
                    }
                else:
                    count = 0
                    realChildren = []
                    emptyChildren = []
                    for i in range(len(root['children'])):
                        root['children'][i] = dfsCount(root['children'][i], counts)
                        count += root['children'][i]['count']
                        if root['children'][i]['count'] != 0:
                            realChildren.append(root['children'][i])
                        else: 
                            emptyChildren.append(root['children'][i])
                    root['realChildren'] = realChildren
                    root['emptyChildren'] = emptyChildren
                    counts[root['name']] = count
                    root['count'] = count
                    return root
            
            dfsCount(root, counts)

            pq = PriorityQueue()

            class Cmp:
                def __init__(self, name, count, realChildren):
                    self.name = name
                    self.count = count
                    self.realChildren = realChildren

                def __lt__(self, other):
                    if self.count <= other.count:
                        return False
                    else:
                        return True

                def to_list(self):
                    return [self.name, self.count, self.realChildren]
            
            pq.put(Cmp(root['name'], root['count'], root['realChildren']))
            classThreshold = 10
            countThreshold = 0.5
        
            
            while True:
                if pq.qsize()==0:
                    break
                top = pq.get()
                if pq.qsize() + len(top.realChildren) <= classThreshold or top.count / root['count'] >= countThreshold:
                    for child in top.realChildren:
                        pq.put(Cmp(child['name'], child['count'], child['realChildren']))
                    if pq.qsize()==0:
                        pq.put(top)
                        break
                else:
                    pq.put(top)
                    break
    
            pq_list = []
            while not pq.empty():
                pq_list.append(pq.get().name)
            return pq_list

        bottomLabels = getBottomLabels(copy.deepcopy(zoomInNodes))
        labelTransform = self.transformBottomLabelToTop(bottomLabels)
        constraintLabels = labelTransform[self.labels[nodes]]
        labels = labelTransform[zoomInLabels]  
      
        # calculate grid layout
        tsne, grid, gridsize = self.grider.fit(self.features[zoomInNodes], labels = labels, constraintX = zoomInConstraintX,  constraintY = zoomInConstraints, constraintLabels = constraintLabels)
        tsne = tsne.tolist()
        grid = grid.tolist()
        zoomInLabels = zoomInLabels.tolist()
        zoomInPreds = zoomInPreds.tolist()
        zoomInConfidence = zoomInConfidence.tolist()


        # return result
        n = len(zoomInNodes)
        nodes = [{
            "index": zoomInNodes[i],
            "tsne": tsne[i],
            "grid": grid[i],
            "label": zoomInLabels[i],
            "pred": zoomInPreds[i],
            "confidence": zoomInConfidence[i]
        } for i in range(n)]
        res = {
            "nodes": nodes,
            "grid": {
                "width": gridsize,
                "height": gridsize,
            },
            "depth": newDepth
        }
        if depth==0 and self.enableTSNEBuffer:
            with open(TSNEBufferPath, 'w') as f:
                json.dump(res, f)
        return res

    def findGridParent(self, children, parents):
        return self.sampler.findParents(children, parents)
    
    def transformBottomLabelToTop(self, topLabels):
        topLabelChildren = {}
        topLabelSet = set(topLabels)
        def dfs(nodes):
            childrens = []
            for root in nodes:
                if type(root)==str:
                    childrens.append(root)
                    if root in topLabelSet:
                        topLabelChildren[root] = [root]
                else:
                    rootChildren = dfs(root['children'])
                    childrens += rootChildren
                    if root['name'] in topLabelSet:
                        topLabelChildren[root['name']] = rootChildren
            return childrens
        dfs(self.statistic['hierarchy'])
        childToTop = {}
        for topLabelIdx in range(len(topLabels)):
            for child in topLabelChildren[topLabels[topLabelIdx]]:
                childToTop[child] = topLabelIdx
        n = len(self.statistic['names'])
        labelTransform = np.zeros(n, dtype=int)
        for i in range(n):
            if not childToTop.__contains__(self.statistic['names'][i]):
                print('not include ' + self.statistic['names'][i])
            else:
                labelTransform[i] = childToTop[self.statistic['names'][i]]
        return labelTransform.astype(int)
    
dataCtrler = DataCtrler()
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/allData', methods=['GET'])
def allData():
    alldata = {
    }
    return jsonify(alldata)

@app.route('/api/labelHierarchy', methods=["POST"])
def labelHierarchy():
    return jsonify(dataCtrler.getLabelHierarchy())


@app.route('/api/imageGradient', methods=["GET"])
def imageGradient():
    imageID = int(request.args['imageID'])
    method = request.args['method']
    return jsonify(dataCtrler.getImageGradient(imageID, method))

@app.route('/api/grid', methods=["POST"])
def grid():
    nodes = request.json['nodes']
    constraints = None
    if 'constraints' in request.json:
        constraints = request.json['constraints']
    depth = request.json['depth']
    return jsonify(dataCtrler.gridZoomIn(nodes, constraints, depth))

@app.route('/api/findParent', methods=["POST"])
def findParent():
    children = request.json['children']
    parents = request.json['parents']
    return jsonify(dataCtrler.findGridParent(children, parents))

def main():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--data_path", type=str, default='./data/')
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5005)
    args = parser.parse_args()
    if not os.path.exists(args.data_path):
        raise Exception("The path does not exist.")

    predictPath = os.path.join(args.data_path, "predict_info.pkl")
    trainImagePath = os.path.join(args.data_path, "trainImages.npy")
    bufferPath = os.path.join(args.data_path, "buffer")
    with open(predictPath, 'rb') as f:
        predictData = pickle.load(f)
    trainImages = np.load(trainImagePath)
    
    dataCtrler.process(predictData = predictData, trainImages = trainImages, bufferPath = bufferPath)

    app.run(port=args.port, host=args.host, threaded=True, debug=False)

if __name__ == "__main__":
    main()