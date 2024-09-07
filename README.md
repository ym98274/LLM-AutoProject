### Designing effective LLM systems for Autonomous driving: towards a paradigm for configuring LLM based end-to-end self-driving architectures

The objective of this work is to help develop stronger convergence for the development of LLM based end-to-end self driving systems.

This system proposed by the [LMDrive drive study](https://github.com/opendilab/LMDrive/tree/main) is adopted as the baseline due to the frequent use of its underlying components in similar LLM based systems.

As part of this work, 5 modifications are implemented in respect of 3 LMDrive system components: 
  1. RGB backbone encoder
  2. Lidar point cloud encoder
  3. LLM scene reasoning component

These component modifications have demonstrated promising results by either exceeding baseline component performance or obtaining similar results with much less complexity: 

RGB Component results:

| RGB Backbone        | Overall Loss | Detection Loss | Waypoint Loss | Cross-entropy Loss |
|---------------------|--------------|----------------|---------------|--------------------|
| ResNet-50 (Baseline) | 1.0350      | 0.2765         | 1.6263        | 0.6712             |
| CSPDarknet53        | 0.8714       | 0.2891         | 1.2934        | 0.6373             |
| ConvNeXT            | **0.8342**       | **0.2743**         | 1.2360        | **0.6201**             |
| ResNeXT             | 0.8509       | 0.2802         | **1.2335**        | 0.7716             |


Lidar Component results: 

| Lidar Backbone           | Overall Loss | Detection Loss | Waypoint Loss | Cross-entropy Loss |
|--------------------------|--------------|----------------|---------------|--------------------|
| PointPillars (Baseline)   | 1.0350       | 0.2765     | 1.6263        | 0.6712         |
| DGCNN                    | **0.8387**   | **0.2604**     | **1.3956**        | **0.0335**         |

LLM Component results:

| LLM Backbone            | Overall Loss | Waypoint Loss | Classification Loss |
|-------------------------|--------------|---------------|---------------------|
| LLaVA-v1.5 (Baseline)    | **0.943**        | **0.922**         | **0.105**               |
| GIT                     | 1.179        | 1.126         | 0.264               |



The updated code has been tested extensivley to be compatible with the CARLA simulation environment. Thus autonmous-driving researchers are encouraged to download the modified components and evaluate these with the CARLA simulator.






