#!/usr/bin/env python
import argparse
import tempfile
import time

import dask_jobqueue
import distributed


def do_it(i):
    time.sleep(2.0)  # simulate a long-running task
    return i**2

if __name__ == '__main__':
    cluster_classes = {'htcondor': dask_jobqueue.HTCondorCluster,
                       'local': distributed.LocalCluster,
                       'lsf': dask_jobqueue.LSFCluster,
                       'moab': dask_jobqueue.MoabCluster,
                       'oar': dask_jobqueue.OARCluster,
                       'pbs': dask_jobqueue.PBSCluster,
                       'sge': dask_jobqueue.SGECluster,
                       'slurm': dask_jobqueue.SLURMCluster}

    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('parallelization',
                                      'parallel processing and cluster engine')
    group.add_argument('-j', '--jobs', type=int)
    group.add_argument('--cluster', default='local',
                       choices=cluster_classes.keys())
    args = parser.parse_args()

    cluster_class = cluster_classes[args.cluster]
    cluster = cluster_class(dashboard_address=None,
                            local_directory=tempfile.gettempdir())
    cluster.adapt(maximum=args.jobs)
    client = distributed.Client(cluster)
    for future in distributed.as_completed(client.map(do_it, range(10))):
        print(future.result())
