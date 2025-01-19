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

The basline model with the components descrived in the original paper was also trained and then evaluated using the same type and quantity of data to allow for an accuract evalaution of perfmance changes.

The authors of the original LMDrive system note that training for the vision encoder component with the complete dataset took 2-3 days with 8 A100 GPUs with 80GB memory. A similar estimate was provided in respect of the LLM component.

To support quick protyping, this work modifies the training scripts to run with a single A100 GPU in a non-distriubuted fashion. These are also provided with model code and weights but can be further adjusted for specific requirements. Additional data parsing scripts are supplied to help download a selected data distribution.

The project code has been tested extensively to be compatible with the CARLA simulation environment. Thus, autonomous-driving researchers are encouraged to download the modified components and evaluate these with the CARLA simulator.

### Model Weights
To easily dilineate performance differences, each modified system was trained with a reduced number of samples which were downloaded with the data distribution/parsing script developed as part of this work. Training and evaluation was conducted by modifying a component and freezing the remaining components to better isolate the source of  performance changes.

The modifications are not expected to exceed the performance of the original LMDrive paper and were designed to identify the best route for development/improvement in line with the objectives of this work. The model weights and checkpoints are thus provided solely for testing and validation of the changes in performance described. Researchers are invited to download these and evaluate them using the default validation or the CARLA simulator. 


| Sytem Name        | Model weights                                                                                    | 
|-------------------|--------------------------------------------------------------------------------------------------|
| ResNet-50 (Baseline)  | [Download](https://mega.nz/file/rEBVyB6Y#dgXbqFi_NPobGUPxGY1horhESU_Cg8P2gpa8Nyp95JY)        | 
| CSPDarknet53   | [Download](https://mega.nz/file/7JRziIZL#zEBlD2LvLHps0eUm4EgfJqBXaaIo8AoN57FmF6-V5ek)               |
| ConvNeXT    | [Download](https://mega.nz/file/2NJXDaaT#Q8-QhrYUvy1Jy340Rga4VPQrE5K5yMtyhninw-vHerM)                  |
| ResNeXT   | [Download](https://mega.nz/file/WAxxVAbS#5LHNshQCXPrWApCKOlXo5yhjBeljGmqtPHrhJUGy6_E)                    | 
| PointPillars (Baseline)    | [Download](https://mega.nz/file/GVwwCLJC#RmWCj9NI3ETSE955qBwDx-yp-yyWwuDki3_QL-7nM8M)   | 
| DGCNN   | [Download](https://mega.nz/file/aIQgRQgJ#GzoA_rTRjOeGkN1Ol4G9yN0UkUnB6PmwQy1jJ0smjX8)                      |
| LLaVA-v1.5 (Baseline)     | [Download](https://mega.nz/file/rUJgDbTZ#N2aDzK33b_fvuxPq5y4SWIjQzml4hkQduoOY06nHLys)    |
| GIT   | [Download](https://mega.nz/file/KNQGQThS#5GF8ht8OUYWPJl0S1ockgQuJV99X45jN6uJ-5yxh0-I)                        | 

### Usage instructions

The model weights are provided together with the modified scripts.

Follow the setup guidance on the [LMDrive repo](https://github.com/opendilab/LMDrive?tab=readme-ov-file#setup) to build the environment.

To commence training, ensure the scripts of the original LMDrive system are replaced with the modified scripts. For vision-encoder training, it is only necessary to replace the `memufuser.py` script. 

For LLM training, ensure that that the `drive.py` as well as the `memfuser.py` script is replaced. Depending on whether you wish to train using only a single GPU, you can also use the modified training scripts. 

The LMDrive data is arranged in a series of directories with names denoting CARLA towns and wheather conditions. The data parsing script for the vision encoder training operates by downloading a selected list of directories. The parsing script for the LLM component modifies `nav_intruction_list.txt` such that the routes match the downloaded sensor-data samples.

To use the modified architectures for evaluation on the CARLA simulator, download the model weights and update the paths in `leaderboard/scripts/run_evaluation.sh`




