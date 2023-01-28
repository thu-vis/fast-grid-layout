# A similarity-perserving grid layout for sample exploration

Codes for the grid layout developed in the paper ["OoDAnalyzer: Interactive Analysis of Out-of-Distribution Samples"](https://ieeexplore.ieee.org/document/8994105) (TVCG 2020).

![demo](grid.gif)

## Install
This repo is tested with Python 3.8 on Ubuntu

First, install requirements.txt
```
pip install -r requirements.txt
```
Then, install fastlapjv
```
git clone git@github.com:thu-vis/fast-lapjv.git
cd fast-lapjv/
python setup.py install --user
```
Finally, install faiss(you can also follow [this doc](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md)).
```
conda install -c pytorch faiss-gpu
# or
conda install -c pytorch faiss-cpu
```


## How to setup the demo
1. download data from [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/fdbca618102c46be84f2/?dl=1) and unzip
1. run backend
```bash
python demo.py --data_path YOUR_DATA_PATH
```
2. install and run frontend

replace `BACKEND_BASE_URL` in `webpack.base.conf.js` to your backend URL
```bash
cd frontend
yarn # setup all frontend packages
yarn start # start demo
```
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
