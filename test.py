#!/usr/bin/env python
import argparse
import time

import dask_jobqueue
import distributed
import tqdm


def do_it(i):
    time.sleep(2.0)  # simulate a long-running task
    return i**2

if __name__ == '__main__':
    cluster_classes = {cls.config_name: cls
                       for cls in dask_jobqueue.__dict__.values()
                       if hasattr(cls, 'config_name')}
    cluster_classes['local'] = distributed.LocalCluster

    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('parallelization',
                                      'parallel processing and cluster engine')
    group.add_argument('-j', '--jobs', type=int)
    group.add_argument('--cluster', default='local',
                       choices=cluster_classes.keys())
    args = parser.parse_args()

    cluster_class = cluster_classes[args.cluster]
    cluster = cluster_class()
    cluster.adapt(maximum=args.jobs)
    client = distributed.Client(cluster)
    for future in tqdm(distributed.as_completed(client.map(do_it, range(10)))):
        print(future.result())
