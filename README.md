## Designing effective LLM systems for Autonomous driving: towards a paradigm for configuring LLM based end-to-end self-driving architectures

The objective of this work is to help develop stronger convergence for the development of LLM based end-to-end self driving systems.

The system proposed by the [LMDrive drive study](https://github.com/opendilab/LMDrive/tree/main) is adopted as the baseline due to the frequent use of its underlying components in similar LLM based systems.

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
Note: The DGCNN architecture was trained with less than half of the samples used to train the PointPillars baseline

| Lidar Backbone           | Overall Loss | Detection Loss | Waypoint Loss | Cross-entropy Loss |
|--------------------------|--------------|----------------|---------------|--------------------|
| PointPillars (Baseline)   | 1.0350       | 0.2765     | 1.6263        | 0.6712         |
| DGCNN                    | **0.8387**   | **0.2604**     | **1.3956**        | **0.0335**         |

LLM Component results:

| LLM Backbone            | Overall Loss | Waypoint Loss | Classification Loss |
|-------------------------|--------------|---------------|---------------------|
| LLaVA-v1.5 (Baseline)    | **0.943**        | **0.922**         | **0.105**               |
| GIT                     | 1.179        | 1.126         | 0.264               |


The authors of the original LMdrive system note that training for the vision encoder component with the complete dataset took 2-3 days with 8 A100 GPUs with 80GB memory. A similar estimate was provided in respect of the LLM component.

To support quick protyping, this work modifies the training scripts to run with a single GPU and in a non-distriubuted fashion. These are also provided with model code and weights but can be further adjusted for specific requirements.

The updated code has been tested extensivley to be compatible with the CARLA simulation environment. Thus, autonomous-driving researchers are encouraged to download the modified components and evaluate these with the CARLA simulator.

### Usage instructions

The model weights are provided together with the modified scripts.

Follow the setup guidance on the [LMDrive repo](https://github.com/opendilab/LMDrive?tab=readme-ov-file#setup) to build the environment.

To commence training ensure the scripts of the original LMDrive system are replaced with the modified scripts. For vision-encoder training, it is only necessary to replace

Additional data parsing scripts are provided to help download a selected data distribution.

To use the modified architectures for evalaution on the CARLA simulator, download the model weights and update the path in `leaderboard/scripts/run_evaluation.sh`




