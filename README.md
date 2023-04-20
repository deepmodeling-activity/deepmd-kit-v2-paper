# Data for DeePMD-kit v2 paper

This is the repository for supporting data in the following paper:

Jinzhe Zeng, Duo Zhang, Denghui Lu, Pinghui Mo, Zeyu Li, Yixiao Chen, Mari´an Rynik, Li’ang Huang, Ziyao Li, Shaochen Shi, Yingze Wang,
Haotian Ye, Ping Tuo, Jiabin Yang, Ye Ding, Yifan Li, Davide Tisi, Qiyu
Zeng, Han Bao, Yu Xia, Jiameng Huang, Koki Muraoka, Yibo Wang,
Junhan Chang, Fengbo Yuan, Sigbjørn Løland Bore, Chun Cai, Yinnian Lin,
Bo Wang, Jiayan Xu, Jia-Xin Zhu, Chenxing Luo, Yuzhi Zhang, Rhys E. A.
Goodall, Wenshuo Liang, Anurag Kumar Singh, Sikai Yao, Jingchao Zhang,
Renata Wentzcovitch, Jiequn Han, Jie Liu, Weile Jia, Darrin M. York,
Weinan E, Roberto Car, Linfeng Zhang, and Han Wang,
DeePMD-kit v2: A software package for Deep Potential models,
[arXiv:2304.09409](https://arxiv.org/abs/2304.09409), 2023.

Please give the proper credits if you reuse these data.

## Data sets and LAMMPS data

| Name  | Link           | LAMMPS data |
| ----- | -------------- | ----------- |
| Water | [AISSquare](https://aissquare.com/datasets/detail?pageType=datasets&name=H2O-PBE0TS) | [water.lmp](models/water.lmp) |
| Cu    | [AISSquare](https://aissquare.com/datasets/detail?pageType=datasets&name=Cu-dpgen) | [copper.lmp](models/copper.lmp) |
| HEA   | Coming soon | [hea.lmp](models/hea.lmp) |
| OC2M  | [AISSquare](https://aissquare.com/datasets/detail?pageType=datasets&name=Open_Catalyst_2020%28OC20_Dataset%29) | |
| SPICE | [10.5281/zenodo.7606550](https://doi.org/10.5281/zenodo.7606550) | |

## Models

| System  | `loc_frame` FP64 | `loc_frame` FP32 | `se_e2_a` FP64 | `se_e2_a` FP32 | `se_e2_a+se_e2_r` FP64 | `se_e2_a+se_e2_r` FP32 | `se_e2_a+se_e3` FP64 | `se_e2_a+se_e3` FP32 | `se_atten` FP64 | `se_atten` FP32 |
| ------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| Water | [01](models/01) | [02](models/02) | [03](models/03) | [04](models/04) | [05](models/05) | [06](models/06) | [07](models/07) | [08](models/08) | [09](models/09) | [10](models/10) |
| Cu | [11](models/11) | [12](models/12) | [13](models/13) | [14](models/14) | [15](models/15) | [16](models/16) | [17](models/17) | [18](models/18) | [19](models/19) | [20](models/20) | 
| OC2M |  |  |  |  |  |  |  |  | [29](models/29) | [30](models/30) | 
| HEA  |  |  | [33](models/33) | [34](models/34) | [35](models/35) | [36](models/36) | [37](models/37) | [38](models/38) | [39](models/39) | [40](models/40) | 
| Dipeptides |  |  | [43](models/43) | [44](models/44) | [45](models/45) | [46](models/46) | [47](models/47) | [48](models/48) | [49](models/49) | [50](models/50) | 
| SPICE |  |  |  |  |  |  |  |  | [59](models/59) | [60](models/60) | 
