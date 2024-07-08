Statistics and Usage
====================

.. highlight:: none

SyNAP provides NPU usage information and statistics.
This is done via the standard linux :code:`/sysfs` interface.
Basically  :code:`/sysfs` allows to provide information about system devices
and resources using a *pseudo file-system* where each piece of information is seen
as a file that can be read/written by the user using standard tools.

On Android statistics are available in  :code:`/sys/class/misc/synap/device/misc/synap/statistics/`::


    $ SYNAP_STAT_DIR=/sys/class/misc/synap/device/misc/synap/statistics


On Yocto Linux they are in :code:`/sys/class/misc/synap/statistics/`::

    $ SYNAP_STAT_DIR=/sys/class/misc/synap/statistics

.. code-block::

    $ ls $SYNAP_STAT_DIR
    inference_count  inference_time  network_profile networks


.. important::

    The content of the statistics files is only available from **root** user.


.. note::
    There are no statistics regarding inference performed on the CPU or the GPU. CPU inference can
    occour at the user-space level and it's not possible to track it inside the SyNAP driver.

.. _sysfs-inference-counter:

``inference_count``
-------------------

This file contains the total number of inferences performed on the NPU since system startup.
Example::

    # cat $SYNAP_STAT_DIR/inference_count
    1538


``inference_time``
-------------------

This file contains the total time spent doing NPU inferences since system startup.
It is a 64-bits integer expressed in microseconds.
Example::

    # cat $SYNAP_STAT_DIR/inference_time 
    32233264


``networks``
------------

This file contains detailed information for each network *currently* loaded in the NPU driver
with a line per network. Each line contains the following information:

- **pid**: process that created the network
- **nid**: unique network id
- **inference_count**: number of inferences for this network
- **inference_time**: total inference time for this network in us
- **inference_last**: last inference time for this network in us
- **iobuf_count**: number of I/O buffers currently registered to the network
- **iobuf_size**: total size of I/O buffers currently registered to the network
- **layers**: number of layers in the network


Example::

    # cat $SYNAP_STAT_DIR/networks
    pid: 3628, nid: 38, inference_count: 22, inference_time: 40048, inference_last: 1843, iobuf_count: 2, iobuf_size: 151529, layers: 34
    pid: 3155, nid: 4, inference_count: 3, inference_time: 5922, inference_last: 1843, iobuf_count: 2, iobuf_size: 451630, layers: 12

.. important::

    This file will be empty if there is no network currently loaded

It's easy to show in realtime the information for all the networks currently loaded with the
standard ``watch`` command::

    # watch -n 1 cat $SYNAP_STAT_DIR/networks

.. _sysfs-networks:

``network_profile``
-------------------

This file contains detailed information for each network *currently* loaded in the NPU driver,
with a line per network. The information in each line is the same as in the ``networks`` file.
In addition if a model has been compiled offline with profiling enabled (see section :ref:`model-profiling-label`)
or executed online with profiling enabled (see section :ref:`online_benchmarking_nnapi`)
the corresponding line will be followed by detailed layer-by-layer information:

- **lyr**: index of the layer (or group of layers)
- **cycle**: number of execution cycles
- **time_us**: execution time in us
- **byte_rd**: number of bytes read
- **byte_wr**: number of bytes written
- **ot**: operation type (NN: Neural Network core, SH: Shader, TP: TensorProcessor)
- **name**: operation name

Example::

    # cat $SYNAP_STAT_DIR/network_profile
    pid: 21756, nid: 1, inference_count: 78, inference_time: 272430, inference_last: 3108, iobuf_count: 2, iobuf_size: 151529, layers: 34
    | lyr |    cycle | time_us | byte_rd | byte_wr | ot | name
    |   0 |   153811 |     202 |  151344 |       0 | TP | TensorTranspose
    |   1 |   181903 |     461 |    6912 |       0 | NN | ConvolutionReluPoolingLayer2
    |   2 |     9321 |      52 |    1392 |       0 | NN | ConvolutionReluPoolingLayer2
    |   3 |    17430 |      51 |    1904 |       0 | NN | ConvolutionReluPoolingLayer2
    |   4 |    19878 |      51 |    1904 |       0 | NN | ConvolutionReluPoolingLayer2
    ...
    |  28 |    16248 |      51 |    7472 |       0 | NN | ConvolutionReluPoolingLayer2
    |  29 |   125706 |     408 |  120720 |       0 | TP | FullyConnectedReluLayer
    |  30 |   137129 |     196 |    2848 |    1024 | SH | Softmax2Layer
    |  31 |        0 |       0 |       0 |       0 | -- | ConvolutionReluPoolingLayer2
    |  32 |        0 |       0 |       0 |       0 | -- | ConvolutionReluPoolingLayer2
    |  33 |      671 |      51 |    1008 |       0 | NN | ConvolutionReluPoolingLayer2


Clearing statistics
-------------------

Statistics can be cleared by writing to either the ``inference_count`` or ``inference_time`` file.

Example::

    # cat $SYNAP_STAT_DIR/inference_time 
    32233264
    # echo > $SYNAP_STAT_DIR/inference_time 
    # cat $SYNAP_STAT_DIR/inference_time
    0
    # cat $SYNAP_STAT_DIR/inference_count 
    0


Using ``/sysfs`` information
----------------------------

The information available from :code:`/sysfs` can be easily used from scripts or tools.
For example in order to get the average NPU utilization in a 5 seconds period::

    us=5000000;
    echo > $SYNAP_STAT_DIR/inference_time;
    usleep $us;
    npu_usage=$((`cat $SYNAP_STAT_DIR/inference_time`*100/us));
    echo "Average NPU usage: $npu_usage%"



