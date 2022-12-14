# A similarity-perserving grid layout for sample exploration

Codes for the grid layout developed in the paper ["OoDAnalyzer: Interactive Analysis of Out-of-Distribution Samples"](https://ieeexplore.ieee.org/document/8994105) (TVCG 2020).

## Install
```
pip install -r requirements.txt
```

## Usage
```
from GridLayout import GridLayout

X = np.random.rand(500, 128)
labels = np.random.randint(10, size=500)
grid = GridLayout()
X_embedded, grid_ass, grid_size = grid.fit(X, labels) # labels are optional
```

## How to setup demo
1. download data from [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/fdbca618102c46be84f2/?dl=1) and unzip
1. install and run backend
```bash
pip install -r requirements.txt
python demo.py --data_path YOUR_DATA_PATH
```
2. install and run frontend

replace `BACKEND_BASE_URL` in `webpack.base.conf.js` to your backend URL
```bash
cd frontend
yarn
yarn start
```

## Acknowledgement
This code is implemented based on the published code of [lapjv](https://github.com/src-d/lapjv), and it is our pleasure to acknowledge their contributions.

## Citation
If you use this code for your research, please consider citing:
```
@article{chen2020oodanalyzer,
    title = {{OoDAnalyzer}: Interactive Analysis of Out-of-Distribution Samples},
    author = {Chen, Changjian and Yuan, Jun and Lu, Yafeng and Liu, Yang and Yuan, Songtao and Liu, Shixia},
    journal = {IEEE Transactions on Visualization and Computer Graphics (accepted)},
    year = {2020}
}
```

## Contact
If you have any problem about our code, feel free to contact
- changjianchen.me@gmail.com

or describe your problem in Issues.
