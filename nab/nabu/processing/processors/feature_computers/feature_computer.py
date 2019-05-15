'''@file feature_computer.py
contains the FeatureComputer class'''

import os
from abc import ABCMeta, abstractmethod
from nabu.tools.default_conf import apply_defaults

class FeatureComputer(object):
    '''A featurecomputer is used to compute features'''

    __metaclass__ = ABCMeta

    def __init__(self, conf):
        '''
        FeatureComputer constructor

        Args:
            conf: the feature configuration as a configparser
        '''

        self.conf = dict(conf.items('feature'))

        #apply default configuration
        default = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'defaults',
            type(self).__name__.lower() + '.cfg')
        apply_defaults(self.conf, default)


    def __call__(self, sig, rate):
        '''
        compute the features

        Args:


        Returns:
            the features as a [seq_length x feature_dim] numpy array
        '''

        #compute the features and energy
        print 'before comp_feat'
        print sig
        print rate
        print self.conf
        feat = self.comp_feat(sig, rate)

        return feat

    @abstractmethod
    def comp_feat(self, sig, rate):
        '''
        compute the features

        Args:
            sig: the audio signal as a 1-D numpy array
            rate: the sampling rate

        Returns:
            the features as a [seq_length x feature_dim] numpy array
        '''

    @abstractmethod
    def get_dim(self):
        '''the feature dimemsion'''
