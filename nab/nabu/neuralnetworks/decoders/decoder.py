'''@file decoder.py
neural network decoder environment'''

import os
from abc import ABCMeta, abstractmethod
from nabu.tools.default_conf import apply_defaults

class Decoder(object):
    '''the abstract class for a decoder'''

    __metaclass__ = ABCMeta

    def __init__(self, conf, model):
        '''
        Decoder constructor

        Args:
            conf: the decoder config
            model: the model that will be used for decoding
        '''

        self.conf = dict(conf.items('decoder'))

        #apply default configuration
        default = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'defaults',
            type(self).__name__.lower() + '.cfg')
        apply_defaults(self.conf, default)

        self.model = model

    @abstractmethod
    def __call__(self, inputs, input_seq_length):
        '''decode a batch of data

        Args:
            inputs: the inputs as a dictionary of [batch_size x ...] tensors
            input_seq_length: the input sequence lengths as a dictionary of
                [batch_size] vectors

        Returns:
            - the decoded sequences as a dictionary of outputs
        '''

    @abstractmethod
    def write(self, outputs, directory, names):
        '''write the output of the decoder to disk

        args:
            outputs: the outputs of the decoder as a dictionary
            directory: the directory where the results should be written
            names: the names of the utterances in outputs
        '''

    @abstractmethod
    def update_evaluation_loss(self, loss, outputs, references,
                               reference_seq_length):
        '''update the evaluation loss

        args:
            loss: the current evaluation loss
            outputs: the outputs of the decoder as a dictionary
            references: the references as a dictionary
            reference_seq_length: the sequence lengths of the references

        Returns:
            an op to update the evalution loss
        '''
