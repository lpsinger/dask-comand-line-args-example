# Dask jobqueue example

This is a demonstration of using [dask_jobqueue] to parallelize Python code
using multiple local processes or one of many cluster job schedulers including
[HTCondor] and [PBS]. Example configurations are included for the
[LIGO Caltech cluster] and [NASA Pleiades].

## Set up

1.  Clone this repository:

        $ git clone https://github.com/lpsinger/dask-comand-line-args-example
        $ cd dask-comand-line-args-example

2.  Create a Python virtual environment and install dask-jobqueue inside it:

        $ python3 -m venv env
        $ source env/bin/activate
        $ pip install git+https://github.com/dask/dask-jobqueue

    Note that it is important that dask-jobqueue is installed from git rather
    than from the Python Package Index because of [dask/dask-jobqueue#405].

3.  Copy the file `jobqueue.yaml` into the directory `~/.config/dask`:

        $ mkdir -p ~/.config/dask
        $ cp jobqueue.yaml ~/.config/dask

4.  Create a self-signed certificate to encrypt Dask's communication:

        $ openssl req -x509 -keyout ~/.config/dask/cert.pem -out ~/.config/dask/cert.pem -days 365 -nodes -batch

5.  Try out the test script using local workers (no cluster scheduler):

        $ ./test.py -j 2

6.  Try out the test script using your cluster's scheduler.

    On the LIGO Caltech cluster:

        $ ./test.py -j 2 --cluster htcondor

    On NASA Pleiades (does not yet work):

        $ ./test.py -j 2 --cluster pbs

[dask_jobqueue]: https://jobqueue.dask.org/
[HTCondor]: https://htcondor.readthedocs.io/
[PBS]: https://www.altair.com/pbs-professional/
[LIGO Caltech cluster]: https://computing.docs.ligo.org/guide/grid/
[NASA Pleiades]: https://www.nas.nasa.gov/hecc/
[dask/dask-jobqueue#405]: https://github.com/dask/dask-jobqueue/pull/405
