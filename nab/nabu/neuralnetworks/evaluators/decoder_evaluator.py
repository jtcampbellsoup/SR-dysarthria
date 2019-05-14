'''@file decoder_evaluator.py
contains the DecoderEvaluator class'''

import tensorflow as tf
import evaluator
from nabu.neuralnetworks.decoders import decoder_factory

class DecoderEvaluator(evaluator.Evaluator):
    '''The Decoder Evaluator is used to evaluate a decoder'''

    def __init__(self, conf, dataconf, model):
        '''Evaluator constructor

        Args:
            conf: the evaluator configuration as a ConfigParser
            dataconf: the database configuration
            model: the model to be evaluated
        '''


        super(DecoderEvaluator, self).__init__(conf, dataconf, model)

        #create a decoder object
        self.decoder = decoder_factory.factory(
            conf.get('decoder', 'decoder'))(conf, model)

    def update_loss(self, loss, inputs, input_seq_length, targets,
                    target_seq_length):
        '''update the validation loss for a batch of data

        Args:
            loss: the current loss
            inputs: the inputs to the neural network, this is a list of
                [batch_size x ...] tensors
            input_seq_length: The sequence lengths of the input utterances, this
                is a list of [batch_size] vectors
            targets: the targets to the neural network, this is a list of
                [batch_size x max_output_length] tensors.
            target_seq_length: The sequence lengths of the target utterances,
                this is a list of [batch_size] vectors

        Returns:
            an operation to update the loss'''

        with tf.name_scope('evaluate_decoder'):

            #use the decoder to decoder
            outputs = self.decoder(inputs, input_seq_length)

            update_loss = self.decoder.update_evaluation_loss(
                loss, outputs, targets, target_seq_length)

        return update_loss
