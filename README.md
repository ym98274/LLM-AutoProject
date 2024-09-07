### Designing effective LLM systems for Autonomous driving: towards a paradigm for configuring LLM based end-to-end self-driving architectures

The objective of this work is to help develop a stronger convergence for the development of LLM based end-to-end self driving systems.

This system proposed by the [LMDrive drive study](https://github.com/opendilab/LMDrive/tree/main) is adopted as the baseline due to frequent use of its underlying components in similar LLM based systems.

As part of this work, 5 modifications are implemented in respect of 3 LMDrive system components: 
  1. RGB backbone encoder
  2. Lidar point cloud encoder
  3. LLM scene reasoning component

These component modifications have demonstrates promising results in testing: 



The updated code has been tested extensivley to be compatible with the CARLA simulation environment. Thus autonmous-driving researchers are encouraged to download the modified components and evaluate these with the CARLA simulator.




