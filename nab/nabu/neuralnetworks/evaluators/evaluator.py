'''@file evaluator.py
contains the Evaluator class'''

import os
from abc import ABCMeta, abstractmethod
import tensorflow as tf
from nabu.processing import input_pipeline
from nabu.tools.default_conf import apply_defaults

class Evaluator(object):
    '''the general evaluator class

    an evaluator is used to evaluate the performance of a model'''

    __metaclass__ = ABCMeta

    def __init__(self, conf, dataconf, model):
        '''Evaluator constructor

        Args:
            conf: the evaluator configuration as a ConfigParser
            dataconf: the database configuration
            model: the model to be evaluated
        '''

        self.conf = dict(conf.items('evaluator'))

        #apply default configuration
        default = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'defaults',
            type(self).__name__.lower() + '.cfg')
        apply_defaults(self.conf, default)

        self.model = model

        #get the database configurations
        inputs = self.model.input_names
        input_sections = [self.conf[i].split(' ') for i in inputs]
        self.input_dataconfs = []
        for sectionset in input_sections:
            self.input_dataconfs.append([])
            for section in sectionset:
                self.input_dataconfs[-1].append(dict(dataconf.items(section)))

        targets = self.conf['targets'].split(' ')
        if targets == ['']:
            targets = []
        target_sections = [self.conf[o].split(' ') for o in targets]
        self.target_dataconfs = []
        for sectionset in target_sections:
            self.target_dataconfs.append([])
            for section in sectionset:
                self.target_dataconfs[-1].append(dict(dataconf.items(section)))
        print 'INIT'
        print inputs
        print input_sections
        print self.input_dataconfs
        print targets
        print target_sections
        print self.target_dataconfs

    def evaluate(self):
        '''evaluate the performance of the model

        Returns:
            - the loss as a scalar tensor
            - an operation to update the loss
            - the number of batches in the validation set as an integer
        '''

        batch_size = int(self.conf['batch_size'])

        with tf.name_scope('evaluate'):

            #a variable to hold the validation loss
            loss = tf.get_variable(
                name='validation_loss',
                shape=[],
                dtype=tf.float32,
                initializer=tf.zeros_initializer(),
                trainable=False
            )

            #get the list of filenames fo the validation set
            data_queue_elements, _ = input_pipeline.get_filenames(
                self.input_dataconfs + self.target_dataconfs)

            #compute the number of batches in the validation set
            numbatches = len(data_queue_elements)/batch_size

            #cut the data so it has a whole numbe of batches
            data_queue_elements = data_queue_elements[:numbatches*batch_size]

            #create a queue to hold the filenames
            data_queue = tf.train.string_input_producer(
                string_tensor=data_queue_elements,
                shuffle=False,
                seed=None,
                capacity=batch_size*2)

            #create the input pipeline
            data, seq_length, _, _ = input_pipeline.input_pipeline(
                data_queue=data_queue,
                batch_size=batch_size,
                numbuckets=1,
                dataconfs=self.input_dataconfs + self.target_dataconfs
            )

            inputs = {
                self.model.input_names[i]: d
                for i, d in enumerate(data[:len(self.input_dataconfs)])}
            
            input_seq_length = {
                self.model.input_names[i]: d
                for i, d in enumerate(seq_length[:len(self.input_dataconfs)])}

            target_names = self.conf['targets'].split(' ')
            targets = {
                target_names[i]: d
                for i, d in enumerate(data[len(self.input_dataconfs):])}

            target_seq_length = {
                target_names[i]: d
                for i, d in enumerate(seq_length[len(self.input_dataconfs):])}
            print 'Evaluating'
            print 'INPUTS:'
            print inputs
            print 'INPUT_SEQ_LENGTH:'
            print input_seq_length
            print 'TARGET NAMES'
            print target_names
            print 'TARGETS'
            print targets
            print 'TARGET_SEQ_LENGTH:'
            print target_seq_length
            update_loss = self.update_loss(
                loss, inputs, input_seq_length, targets, target_seq_length)

        return loss, update_loss, numbatches

    @abstractmethod
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
