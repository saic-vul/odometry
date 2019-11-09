import os

import __init_path__
import env

import mlflow

from slam.base_trainer import BaseTrainer
from slam.models import construct_flexible_model

from slam.linalg import Intrinsics, create_optical_flow_from_rt


class FlexibleWithAugmentationTrainer(BaseTrainer):

    def set_model_args(self):
        self.construct_model_fn = construct_flexible_model
        self.lr = 0.001
        self.loss = 'mae'
        self.scale_rotation = 50

    def set_dataset_args(self):
        self.x_col = ['path_to_optical_flow']
        self.y_col = ['euler_x', 'euler_y', 'euler_z', 't_x', 't_y', 't_z']
        self.image_col = ['path_to_optical_flow', 'path_to_binocular_depth']
        self.load_mode = ['flow_xy', 'depth']
        self.preprocess_mode = ['flow_xy', 'depth']

    @staticmethod
    def get_parser():
        parser = BaseTrainer.get_parser()
        parser.add_argument('--generate_flow_by_rt_proba', type=float, default=1)
        parser.add_argument('--gt_from_uniform_percentile', type=int, default=None)
        parser.add_argument('--augment_with_rectangle_proba', type=float, default=0)
        return parser

    def log_params(self):
        super().log_params()
        mlflow.log_param('generate_flow_by_rt_proba',
                         self.train_generator_args.get('generate_flow_by_rt_proba'))
        mlflow.log_param('gt_from_uniform_percentile',
                         self.train_generator_args.get('gt_from_uniform_percentile'))
        mlflow.log_param('augment_with_rectangle_proba',
                         self.train_generator_args.get('augment_with_rectangle_proba'))


if __name__ == '__main__':

    parser = FlexibleWithAugmentationTrainer.get_parser()
    args = parser.parse_args()

    generate_flow_by_rt_proba = args.generate_flow_by_rt_proba
    gt_from_uniform_percentile = args.gt_from_uniform_percentile
    augment_with_rectangle_proba = args.augment_with_rectangle_proba

    del args.generate_flow_by_rt_proba
    del args.gt_from_uniform_percentile
    del args.augment_with_rectangle_proba

    args.train_generator_args = {
        'generate_flow_by_rt_proba': generate_flow_by_rt_proba,
        'gt_from_uniform_percentile': gt_from_uniform_percentile,
        'augment_with_rectangle_proba': augment_with_rectangle_proba
    }

    trainer = FlexibleWithAugmentationTrainer(**vars(args))
    trainer.train()