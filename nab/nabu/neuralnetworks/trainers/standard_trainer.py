'''@file standard_trainer.py
contains the StandardTrainer'''

from nabu.neuralnetworks.trainers import trainer

class StandardTrainer(trainer.Trainer):
    '''a trainer with no added functionality'''

    def aditional_loss(self):
        '''
        add an aditional loss

        returns:
            the aditional loss or None
        '''

        return None

    def chief_only_hooks(self, outputs):
        '''add hooks only for the chief worker

        Args:
            outputs: the outputs generated by the create graph method

        Returns:
            a list of hooks
        '''

        return []

    def hooks(self, outputs):
        '''add hooks for the session

        Args:
            outputs: the outputs generated by the create graph method

        Returns:
            a list of hooks
        '''

        return []
