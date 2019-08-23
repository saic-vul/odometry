from keras.layers import Flatten

from slam.models.layers import (chunk,
                                concat,
                                conv2d,
                                gated_conv2d,
                                dense,
                                construct_outputs,
                                transform_inputs)
from slam.utils import mlflow_logging


def construct_encoder(inputs,
                      kernel_sizes=[7, 5, 3, 3, 3, 3],
                      strides=[2, 1, 4, 1, 2, 1],
                      dilation_rates=None,
                      kernel_initializer='glorot_normal',
                      use_gated_convolutions=False,
                      use_batch_norm=False):
    conv = gated_conv2d if use_gated_convolutions else conv2d

    layers = len(strides)
    if dilation_rates is None:
        dilation_rates = [1] * layers

    assert layers == len(dilation_rates) and layers == len(kernel_sizes)
    for i in range(layers):
        inputs = conv(inputs,
                      64,
                      kernel_size=kernel_sizes[i],
                      strides=strides[i],
                      dilation_rate=dilation_rates[i],
                      padding='same',
                      batch_norm=use_batch_norm and i == 0,
                      activation='relu',
                      kernel_initializer=kernel_initializer)

    flatten = Flatten()(inputs)
    return flatten


@mlflow_logging(ignore=('inputs',), prefix='model.', name='Flexible')
def construct_flexible_model(inputs,
                             kernel_sizes=[7, 5, 3, 3, 3, 3],
                             strides=[2, 1, 4, 1 ,2, 1],
                             dilation_rates=None,
                             output_size=500,
                             regularization=0,
                             activation='relu',
                             kernel_initializer='glorot_normal',
                             use_gated_convolutions=False,
                             use_batch_norm=False,
                             split=False,
                             transform=None,
                             agnostic=False,
                             channel_wise=False,
                             return_confidence=False):

    inputs, scale = transform_inputs(inputs,
                                     transform=transform,
                                     agnostic=agnostic,
                                     channel_wise=channel_wise)

    features = construct_encoder(inputs,
                                 kernel_sizes=kernel_sizes,
                                 strides=strides,
                                 dilation_rates=dilation_rates,
                                 kernel_initializer=kernel_initializer,
                                 use_gated_convolutions=use_gated_convolutions,
                                 use_batch_norm=use_batch_norm)

    fc_rotation = dense(features,
                        output_size=output_size,
                        layers_num=2,
                        regularization=regularization,
                        activation=activation,
                        kernel_initializer=kernel_initializer,
                        name='rotation')
    fc_translation = dense(features,
                           output_size=output_size,
                           layers_num=2,
                           regularization=regularization,
                           activation=activation,
                           kernel_initializer=kernel_initializer,
                           name='translation')

    if split:
        fc = chunk(fc_rotation, n=3) + chunk(fc_translation, n=3)
    else:
        fc = [fc_rotation] * 3 + [fc_translation] * 3

    outputs = construct_outputs(fc,
                                regularization=regularization,
                                scale=scale,
                                return_confidence=return_confidence)
    return outputs
