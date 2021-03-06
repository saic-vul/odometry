import sys
from typing import Dict
from pathlib import Path

import env


DATASET_PATHS = {'kitti_8/3': env.KITTI_MIXED_PATH,
                 'kitti_4/6': env.KITTI_MIXED_PATH,
                 'kitti_4/6_bovw': env.KITTI_BOVW_PATH,
                 'kitti_4/6_mixed': env.KITTI_MIXED_PATH,
                 'kitti_4/6_bovw_mixed': env.KITTI_BOVW_PATH,
                 'tum_fr1': env.TUM_PATH,
                 'tum_fr2': env.TUM_PATH,
                 'tum_fr3': env.TUM_PATH,
                 'tum': env.TUM_PATH,
                 'tum_bovw': env.TUM_BOVW_PATH,
                 'zju': env.ZJU_PATH,
                 'euroc': env.EUROC_MIXED_PATH,
                 'euroc_bovw': env.EUROC_BOVW_PATH,
                 'euroc_mixed_1_2_3': env.EUROC_MIXED_PATH}

DATASET_TYPES = list(DATASET_PATHS.keys())


def get_dataset_root(dataset_type):
    dataset_root = DATASET_PATHS.get(dataset_type, None)
    if dataset_root is None:
        raise RuntimeError('Unknown dataset_type')

    return dataset_root


def is_int(string: str):
    try:
        int(string)
        return True
    except:
        return False


def get_config(dataset_root: str, dataset_type: str, stride=None) -> Dict:

    assert dataset_type in DATASET_TYPES

    this_module = sys.modules[__name__]
    dataset_type = dataset_type.replace('/', '_').replace('+', '_')
    config = getattr(this_module, f'get_{dataset_type}_config')(dataset_root, stride)
    return config


def add_stride_to_path(config, stride):
    if stride is None:
        return config

    keys = ['train_trajectories', 'val_trajectories', 'test_trajectories']
    for key in keys:
        if config[key] is not None:
            config[key] = [f'{stride}/{trajectory}' for trajectory in config[key]]

    return config


def gen_strides_from_path(config):
    sub_dirs = ['train', 'val', 'test']
    for d in sub_dirs:
        trajectories = config[f'{d}_trajectories']
        config[f'{d}_strides'] = [int(Path(t).parent.name) for t in trajectories] if trajectories else None
    return config


def get_zju_config(_dataset_root, _stride):
    config = {'train_trajectories': ['A0',
                                     'A3',
                                     'A4',
                                     'A5',
                                     'B0',
                                     'B2'],
              'val_trajectories': ['A1',
                                   'A6',
                                   'B1'],
              'test_trajectories': ['A2',
                                    'A7',
                                    'B3'],
              'exp_name': 'zju',
              'target_size': (120, 160),
              'depth_multiplicator': 1.0,
              'rpe_indices': 'full',
              'train_strides': 1,
              'val_strides': 1,
              'test_strides': 1,
              }
    return config


def get_euroc_config(_dataset_root, stride, pwc_mode=None):
    if pwc_mode is None:
        exp_name = 'euroc'
    elif pwc_mode == 'sintel':
        exp_name = 'euroc_sintel'
    elif pwc_mode == 'sintel_g':
        exp_name = 'euroc_sintel_g'
    else:
        raise Exception('pwc_mode is invalid')
    if stride is not None and stride > 1:
        exp_name += f'_stride{stride}'
    config = {'train_trajectories': ['MH_01_easy',
                                     'MH_03_medium',
                                     'MH_04_difficult',
                                     'V1_01_easy',
                                     'V1_03_difficult',
                                     'V2_01_easy',
                                     'V2_03_difficult'],
              'val_trajectories': ['MH_02_easy',
                                   'V1_02_medium'],
              'test_trajectories': ['MH_05_difficult',
                                    'V2_02_medium'],
              'exp_name': exp_name,
              'target_size': (120, 188),
              'depth_multiplicator': 1.0,
              'rpe_indices': 'full',
              'train_strides': stride or 1,
              'val_strides': stride or 1,
              'test_strides': stride or 1,
              }
    config = add_stride_to_path(config, stride)
    return config


def get_euroc_mixed_1_2_3_config(_dataset_root, _stride, pwc_mode=None):
    if pwc_mode is None:
        exp_name = 'euroc_mixed_1_2_3'
    elif pwc_mode == 'sintel':
        exp_name = 'euroc_mixed_1_2_3_sintel'
    elif pwc_mode == 'sintel_g':
        exp_name = 'euroc_mixed_1_2_3_sintel_g'
    else:
        raise Exception('pwc_mode is invalid')
    config = {'train_trajectories': ['1/MH_01_easy',
                                     '1/MH_03_medium',
                                     '1/MH_04_difficult',
                                     '1/V1_01_easy',
                                     '1/V1_03_difficult',
                                     '1/V2_01_easy',
                                     '1/V2_03_difficult',
                                     '2/MH_01_easy',
                                     '2/MH_03_medium',
                                     '2/MH_04_difficult',
                                     '2/V1_01_easy',
                                     '2/V1_03_difficult',
                                     '2/V2_01_easy',
                                     '2/V2_03_difficult',
                                     '3/MH_01_easy',
                                     '3/MH_03_medium',
                                     '3/MH_04_difficult',
                                     '3/V1_01_easy',
                                     '3/V1_03_difficult',
                                     '3/V2_01_easy',
                                     '3/V2_03_difficult'
                                     ],
              'val_trajectories': ['1/MH_02_easy',
                                   '1/V1_02_medium',
                                   '2/MH_02_easy',
                                   '2/V1_02_medium',
                                   '3/MH_02_easy',
                                   '3/V1_02_medium'
                                   ],
              'test_trajectories': ['1/MH_05_difficult',
                                    '1/V2_02_medium',
                                    '2/MH_05_difficult',
                                    '2/V2_02_medium',
                                    '3/MH_05_difficult',
                                    '3/V2_02_medium'
                                    ],
              'exp_name': exp_name,
              'target_size': (120, 188),
              'depth_multiplicator': 1.0,
              'rpe_indices': 'full',
              }

    config = gen_strides_from_path(config)
    return config


def get_euroc_bovw_config(dataset_root, _stride):
    config = get_euroc_config(dataset_root, None)
    config['exp_name'] = 'euroc_bovw'
    return config

def get_kitti_8_3_config(_dataset_root, _stride):
    config = {'train_trajectories': ['00',
                                     '01',
                                     '02',
                                     '03',
                                     '04',
                                     '05',
                                     '06',
                                     '07'],
              'val_trajectories': ['08',
                                   '09',
                                   '10'],
              'test_trajectories': None,
              'exp_name': 'kitti_8/3',
              'target_size': (96, 320),
              'depth_multiplicator': 1.0,
              'rpe_indices': 'kitti',
              'train_strides': 1,
              'val_strides': 1,
              'test_strides': 1,
              }
    return config


def get_kitti_4_6_config(_dataset_root, stride):
    exp_name = 'kitti_4/6'
    if stride is not None and stride > 1:
        exp_name += f'_stride{stride}'
    config = {'train_trajectories': ['00',
                                     '02',
                                     '08',
                                     '09'],
              'val_trajectories': ['03',
                                   '04',
                                   '05',
                                   '06',
                                   '07',
                                   '10'],
              'test_trajectories': None,
              'exp_name': exp_name,
              'target_size': (96, 320),
              'depth_multiplicator': 1.0,
              'rpe_indices': 'kitti',
              'train_strides': stride or 1,
              'val_strides': stride or 1,
              'test_strides': stride or 1,
              }
    config = add_stride_to_path(config, stride)
    return config


def get_kitti_4_6_bovw_config(dataset, _stride):
    config = get_kitti_4_6_config(dataset, None)
    config['exp_name'] = 'kitti_4/6_bovw'
    return config


def get_kitti_4_6_mixed_config(_dataset_root, _stride):
    config = {'train_trajectories': ['1/00',
                                     '1/02',
                                     '1/08',
                                     '1/09',
                                     '2/00',
                                     '2/02',
                                     '2/08',
                                     '2/09'],
              'val_trajectories': ['1/03',
                                   '1/04',
                                   '1/05',
                                   '1/06',
                                   '1/07',
                                   '1/10'],
              'test_trajectories': None,
              'exp_name': 'kitti_4/6_mixed',
              'target_size': (96, 320),
              'depth_multiplicator': 1.0,
              'rpe_indices': 'kitti',
              }

    config = gen_strides_from_path(config)
    return config


def get_tum_fr1_config(_dataset_root, _stride):
    config = {'train_trajectories': ['rgbd_dataset_freiburg1_desk',
                                     'rgbd_dataset_freiburg1_xyz',
                                     'rgbd_dataset_freiburg1_360',
                                     'rgbd_dataset_freiburg1_rpy',
                                     'rgbd_dataset_freiburg1_teddy',
                                     'rgbd_dataset_freiburg1_plant'],
              'val_trajectories': ['rgbd_dataset_freiburg1_room'],
              'test_trajectories': ['rgbd_dataset_freiburg1_desk2'],
              'exp_name': 'tum_fr1',
              'target_size': (120, 160),
              'depth_multiplicator': 1.0 / 5000,
              'rpe_indices': 'full',
              'train_strides': 1,
              'val_strides': 1,
              'test_strides': 1,
              }
    return config


def get_tum_fr2_config(_dataset_root, _stride):
    config = {'train_trajectories': ['rgbd_dataset_freiburg2_xyz',
                                     'rgbd_dataset_freiburg2_rpy',
                                     'rgbd_dataset_freiburg2_flowerbouquet_brownbackground',
                                     'rgbd_dataset_freiburg2_coke',
                                     'rgbd_dataset_freiburg2_metallic_sphere',
                                     'rgbd_dataset_freiburg2_metallic_sphere2',
                                     'rgbd_dataset_freiburg2_dishes'],
              'val_trajectories': ['rgbd_dataset_freiburg2_flowerbouquet'],
              'test_trajectories': ['rgbd_dataset_freiburg2_pioneer_slam3',
                                    'rgbd_dataset_freiburg2_360_hemisphere'],
              'exp_name': 'tum_fr2',
              'target_size': (120, 160),
              'depth_multiplicator': 1.0 / 5000,
              'rpe_indices': 'full',
              'train_strides': 1,
              'val_strides': 1,
              'test_strides': 1,
              }
    return config


def get_tum_fr3_config(_dataset_root, _stride):
    config = {'train_trajectories': ['rgbd_dataset_freiburg3_checkerboard_large',
                                     'rgbd_dataset_freiburg3_sitting_xyz',
                                     'rgbd_dataset_freiburg3_long_office_household',
                                     'rgbd_dataset_freiburg3_walking_xyz',
                                     'rgbd_dataset_freiburg3_walking_static',
                                     'rgbd_dataset_freiburg3_nostructure_notexture_far',
                                     'rgbd_dataset_freiburg3_nostructure_notexture_near_withloop',
                                     'rgbd_dataset_freiburg3_structure_notexture_far',
                                     'rgbd_dataset_freiburg3_walking_halfsphere',
                                     'rgbd_dataset_freiburg3_large_cabinet',
                                     'rgbd_dataset_freiburg3_structure_texture_near',
                                     'rgbd_dataset_freiburg3_sitting_halfsphere',
                                     'rgbd_dataset_freiburg3_nostructure_texture_near_withloop',
                                     'rgbd_dataset_freiburg3_nostructure_texture_far',
                                     'rgbd_dataset_freiburg3_sitting_static',
                                     'rgbd_dataset_freiburg3_structure_texture_far',
                                     'rgbd_dataset_freiburg3_walking_rpy',
                                     'rgbd_dataset_freiburg3_cabinet',
                                     'rgbd_dataset_freiburg3_structure_notexture_near',
                                     'rgbd_dataset_freiburg3_teddy'],
              'val_trajectories': ['rgbd_dataset_freiburg3_sitting_xyz_validation',
                                   'rgbd_dataset_freiburg3_walking_xyz_validation',
                                   'rgbd_dataset_freiburg3_walking_static_validation',
                                   'rgbd_dataset_freiburg3_nostructure_notexture_far_validation',
                                   'rgbd_dataset_freiburg3_nostructure_notexture_near_withloop_validation',
                                   'rgbd_dataset_freiburg3_structure_notexture_far_validation',
                                   'rgbd_dataset_freiburg3_large_cabinet_validation',
                                   'rgbd_dataset_freiburg3_structure_texture_near_validation',
                                   'rgbd_dataset_freiburg3_nostructure_texture_near_withloop_validation',
                                   'rgbd_dataset_freiburg3_sitting_static_validation',
                                   'rgbd_dataset_freiburg3_walking_rpy_validation',
                                   'rgbd_dataset_freiburg3_cabinet_validation',
                                   'rgbd_dataset_freiburg3_structure_notexture_near_validation'],
              'test_trajectories': ['rgbd_dataset_freiburg3_structure_texture_far_validation',
                                    'rgbd_dataset_freiburg3_long_office_household_validation',
                                    'rgbd_dataset_freiburg3_sitting_halfsphere_validation',
                                    'rgbd_dataset_freiburg3_nostructure_texture_far_validation',
                                    'rgbd_dataset_freiburg3_walking_halfsphere_validation'],
              'exp_name': 'tum_fr3',
              'target_size': (120, 160),
              'depth_multiplicator': 1.0 / 5000,
              'rpe_indices': 'full',
              'train_strides': 1,
              'val_strides': 1,
              'test_strides': 1,
              }
    return config


def get_tum_config(dataset_root, stride):
    fr1_config = get_tum_fr1_config(dataset_root, stride)
    fr2_config = get_tum_fr2_config(dataset_root, stride)
    fr3_config = get_tum_fr3_config(dataset_root, stride)

    config = fr1_config
    config['exp_name'] = 'tum'

    subsets = ['train', 'val', 'test']
    for subset in subsets:
        config[f'{subset}_trajectories'].extend(fr2_config[f'{subset}_trajectories'])
        config[f'{subset}_trajectories'].extend(fr3_config[f'{subset}_trajectories'])
    return config


def get_tum_bovw_config(dataset_root, _stride):
    config = get_tum_config(dataset_root, None)
    config['exp_name'] = 'tum_bovw'
    return config
