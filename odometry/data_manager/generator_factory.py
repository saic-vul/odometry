import os
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from keras_preprocessing.image import ImageDataGenerator

from odometry.data_manager.generator import ExtendedDataFrameIterator


class GeneratorFactory:
    def __init__(self,
                 dataset_root,
                 csv_name,
                 train_trajectories=None,
                 val_trajectories=None,
                 x_col=('path_to_rgb', 'path_to_rgb_next'),
                 y_col=('euler_x', 'euler_y', 'euler_z', 't_x', 't_y', 't_z'),
                 image_col=('path_to_rgb', 'path_to_rgb_next'),
                 train_generator_args=None,
                 val_generator_args=None,
                 validate_on_train_trajectory=False,
                 val_ratio=0.0,
                 number_of_folds=None,
                 fold_index=0,
                 train_sampling_step=1,
                 val_sampling_step=1,
                 batch_size=128,
                 cached_images=None,
                 *args, **kwargs):

        self.dataset_root = dataset_root
        self.csv_name = csv_name

        self.x_col = list(x_col)
        self.y_col = list(y_col)
        self.image_col = list(image_col)

        self.batch_size = batch_size

        assert validate_on_train_trajectory == bool(val_ratio)
        if validate_on_train_trajectory:
            assert val_trajectories is None
            val_trajectories = train_trajectories

        self.train_trajectories = train_trajectories
        self.val_trajectories = val_trajectories

        self.df_train = self._get_multi_df_dataset(self.train_trajectories) \
                            if self.train_trajectories else None
        self.df_val = self._get_multi_df_dataset(self.val_trajectories)

        if number_of_folds is not None:
            val_ratio = 1. / number_of_folds

        if val_ratio:
            val_samples = int(np.ceil(val_ratio * len(self.df_val))) # upper-round to cover all dataset with k folds
            start = val_samples * fold_index
            end = start + val_samples
            print('fold #{}: validate on samples {} -- {} (out of {})'.format(fold_index, start, end, len(self.df_val)))
            self.df_train = pd.concat([self.df_train[:start], self.df_train[end:]])
            self.df_val = self.df_val[start:end]

        if train_sampling_step != 1:
            self.df_train = self.df_train.iloc[::train_sampling_step]
        if val_sampling_step != 1:
            self.df_val = self.df_val.iloc[::val_sampling_step]

        if train_generator_args is None:
            train_generator_args = {}
        if val_generator_args is None:
            val_generator_args = {}

        self.train_generator_args = train_generator_args
        self.val_generator_args = val_generator_args

        self.args = args
        self.kwargs = kwargs

        self.cached_images = cached_images
        if type(self.cached_images) == str:
            self.load_cache(self.cached_images)

        if self.df_train is not None:
            self.input_shapes = self.get_train_generator().input_shapes
        else:
            self.input_shapes = self.get_val_generator().input_shapes

    def _get_multi_df_dataset(self, trajectories):
        df = None
        for trajectory_name in tqdm(trajectories):
            current_df = pd.read_csv(os.path.join(self.dataset_root, trajectory_name, self.csv_name))
            current_df[self.image_col] = trajectory_name + '/' + current_df[self.image_col]
            current_df['trajectory_id'] = trajectory_name
            if df is None:
                df = current_df
            else:
                df = df.append(current_df, sort=False)

        df.index = range(len(df))
        return df

    def warm_up_cache(self):
        assert self.cached_images is not None

        print('Train:', flush=True)
        train_generator = self.get_train_generator()
        for batch_index in tqdm(range(len(train_generator))):
            train_generator[batch_index]

        print('Validation:', flush=True)
        val_generator = self.get_val_generator()
        for batch_index in tqdm(range(len(val_generator))):
            val_generator[batch_index]

    def load_cache(self, cache_file):
        try:
            with open(cache_file, 'rb') as cache_fp:
                self.cached_images = pickle.load(cache_fp)
        except:
            print('Failed to load cached images from "{}", initialized empty cache'.format(cache_file))
            self.cached_images = {}
        else:
            print('Successfully loaded cached images from "{}"'.format(cache_file))

    def dump_cache(self, cache_file):
        with open(cache_file, 'wb') as cache_fp:
            pickle.dump(self.cached_images, cache_fp)
        print('Saved cached images to "{}"'.format(cache_file))

    def _get_generator(self, dataframe, generator_args, trajectory=False):
        if trajectory:
            shuffle = False
            filter_invalid = False
        else:
            shuffle = True
            filter_invalid = True

        return ExtendedDataFrameIterator(
            dataframe,
            self.dataset_root,
            ImageDataGenerator(**generator_args),
            x_col=self.x_col,
            y_col=self.y_col,
            image_col=self.image_col,
            batch_size=self.batch_size,
            shuffle=shuffle,
            seed=42,
            interpolation='nearest',
            cached_images=self.cached_images,
            filter_invalid=filter_invalid,
            *self.args, **self.kwargs)

    def get_train_generator(self):
        return self._get_generator(self.df_train, self.train_generator_args)

    def get_val_generator(self):
        return self._get_generator(self.df_val, self.val_generator_args, trajectory=True)
