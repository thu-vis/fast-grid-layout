# A similarity-perserving grid layout for sample exploration

Codes for the grid layout developed in the paper ["OoDAnalyzer: Interactive Analysis of Out-of-Distribution Samples"](https://ieeexplore.ieee.org/document/8994105) (TVCG 2020).

![demo](grid.gif)

## Install
This repo is tested with Python 3.8 on Ubuntu

1.  install requirements.txt
```
pip install -r requirements.txt
```
2. install fastlapjv
```
git clone git@github.com:thu-vis/fast-lapjv.git
cd fast-lapjv/
python setup.py install --user
```
3. install faiss (you can also follow [this doc](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md)).
```
conda install -c pytorch faiss-gpu
# or
conda install -c pytorch faiss-cpu
```


## How to setup the demo
1. Download data from [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/fdbca618102c46be84f2/?dl=1) and unzip

2. Run demo (if the port 5005 is occupied, you can change to another port by modifying the commend)
```bash
python demo.py --data_path YOUR_DATA_PATH --port 5005
```

3. Visit http://localhost:5005/ on your browser.

## data format in demo
```
predict_info.pkl: a dict
{
	features: np array of features
        labels: np array of labels
	preds: np array of preds
	scores: np array of scores
	class_names: a list of class names
}

trainImages.npy: all training images with shape (n, width, height, channel) 
```

## Acknowledgement
This code is implemented based on the published code of [lapjv](https://github.com/src-d/lapjv), and it is our pleasure to acknowledge their contributions.

## Citation
If you use this code for your research, please consider citing:
```
@article{chen2021oodanalyzer,
  author={Chen, Changjian and Yuan, Jun and Lu, Yafeng and Liu, Yang and Su, Hang and Yuan, Songtao and Liu, Shixia},
  journal={IEEE Transactions on Visualization and Computer Graphics}, 
  title={{OoDAnalyzer}: Interactive Analysis of Out-of-Distribution Samples}, 
  year={2021},
  volume={27},
  number={7},
  pages={3335-3349}}
```

## Contact
If you have any problem about our code, feel free to contact
- changjianchen.me@gmail.com

or describe your problem in Issues.
