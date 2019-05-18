'''@file data.py
does the data preperation'''

import os
from six.moves import configparser
import gzip
import tensorflow as tf
from nabu.processing.processors import processor_factory
from nabu.processing.tfwriters import tfwriter_factory

def main(expdir):
    '''main function'''

    #read the data conf file
    parsed_cfg = configparser.ConfigParser()
    parsed_cfg.read(os.path.join(expdir, 'database.cfg'))

    #loop over the sections in the data config
    name = parsed_cfg.sections()[0]
    
    #read the section
    conf = dict(parsed_cfg.items(name))
    
    #read the processor config
    proc_cfg = configparser.ConfigParser()
    proc_cfg.read(os.path.join(expdir, 'processor.cfg'))
    
    #create a processor
    processor = processor_factory.factory(
        proc_cfg.get('processor', 'processor'))(proc_cfg)

    #create a writer
    writer = tfwriter_factory.factory(conf['type'])(conf['dir'])

    #loop over the data files
    for datafile in conf['datafiles'].split(' '):

        if datafile[-3:] == '.gz':
            open_fn = gzip.open
        else:
            open_fn = open
        count = 0
        #loop over the lines in the datafile
        for line in open_fn(datafile):

            #split the name and the data line
            splitline = line.strip().split(' ')
            name = splitline[0]
            dataline = ' '.join(splitline[1:])

            print dataline 
            try:
                #process the dataline
                processed = processor(dataline)

                #write the processed data to disk
                if processed is not None:
                    writer.write(processed, name)
            except:
                count += 1
                print count
        print count

    #write the metadata to file
    processor.write_metadata(conf['dir'])

if __name__ == '__main__':
    tf.app.flags.DEFINE_string('expdir', 'expdir', 'The experiments directory')
    FLAGS = tf.app.flags.FLAGS

    main(FLAGS.expdir)
