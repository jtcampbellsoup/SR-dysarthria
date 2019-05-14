'''@file main.py
this function is used to run distributed training on a local cluster'''

import os
import atexit
import subprocess
import tensorflow as tf


def local_cluster(expdir):
    '''main function'''

    #read the cluster file
    clusterfile = os.path.join(expdir, 'cluster', 'cluster')
    machines = dict()
    machines['worker'] = []
    machines['ps'] = []
    with open(clusterfile) as fid:
        for line in fid:
            if line.strip():
                split = line.strip().split(',')
                machines[split[0]].append(
                    (split[1], int(split[2]), split[3]))

    #start all the jobs
    processes = []
    for job in machines:
        task_index = 0
        for _ in machines[job]:
            processes.append(subprocess.Popen(
                ['python', '-u', 'nabu/scripts/train.py',
                 '--clusterfile=%s' % clusterfile,
                 '--job_name=%s' % job, '--task_index=%d' % task_index,
                 '--ssh_command=None', '--expdir=%s' % expdir]))
            task_index += 1

    for process in processes:
        atexit.register(cond_term, process=process)

    for process in processes:
        process.wait()

if __name__ == '__main__':
    tf.app.flags.DEFINE_string('expdir', 'expdir', 'The experiments directory')
    FLAGS = tf.app.flags.FLAGS

    local_cluster(FLAGS.expdir)

def cond_term(process):
    '''terminate pid if it exists'''

    try:
        os.kill(process.terminate)
    #pylint: disable=W0702
    except:
        pass
