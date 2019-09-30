import os
import sys
import warnings
import mlflow

DATASET_PATH = '/dbstore/datasets/'
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(PROJECT_PATH, 'submodules/tf_models/research/struct2depth'))
sys.path.append(os.path.join(PROJECT_PATH, 'submodules', 'tfoptflow/tfoptflow'))

os.environ['OMP_NUM_THREADS'] = '4'
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '6'
os.environ['VECLIB_MAXIMUM_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '6'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.simplefilter('ignore')

TRACKING_URI = 'postgresql://odometry:YyXr9f8R@airuhead02:6432/slamdb'
ARTIFACT_PATH = '/dbstore/datasets/robotics/mlflow/odometry/artifacts'
mlflow.set_tracking_uri(TRACKING_URI)

TUM_PATH = '/dbstore/datasets/Odometry_team/tum_rgbd/'
TUM_BOVW_PATH = '/dbstore/datasets/Odometry_team/tum_bovw_p2/'
KITTI_PATH = '/dbstore/datasets/Odometry_team/KITTI_odometry_2012/'
KITTI_MIXED_PATH = '/dbstore/datasets/Odometry_team/KITTI_odometry_2012_mixed/'
KITTI_BOVW_PATH = '/dbstore/datasets/Odometry_team/KITTI_odometry_2012_bovw_p2/'
DISCOMAN_V10_PATH = '/dbstore/datasets/Odometry_team/discoman_v10/'
DISCOMAN_V10_MIXED_PATH = '/dbstore/datasets/Odometry_team/discoman_v10_mixed/'
DISCOMAN_V10_BOVW_PATH = '/dbstore/datasets/Odometry_team/discoman_v10_bovw_p2/'
SAIC_OFFICE_PATH = '/dbstore/datasets/Odometry_team/saic_office_prepare_v1_1_again/'
RETAIL_BOT_PATH = '/dbstore/datasets/Odometry_team/retail_bot/'
EUROC_PATH = '/dbstore/datasets/Odometry_team/EuRoC_stride1/'
EUROC_MIXED_PATH = '/dbstore/datasets/Odometry_team/EuRoC_mixed/'
EUROC_SINTEL_MIXED_PATH = '/dbstore/datasets/Odometry_team/EuRoC_sintel_mixed/'
EUROC_BOVW_PATH = '/dbstore/datasets/Odometry_team/EuRoC_bovw_p2/'
ZJU_PATH = '/dbstore/datasets/Odometry_team/zju_prepare/'
