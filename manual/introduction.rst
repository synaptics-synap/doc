Introduction
============

The purpose of SyNAP is to optimize the execution of neural networks by taking best advantage of the
available hardware - *NPU*, *GPU*, *CPU* or even :ref:`heterogeneous_inference`.

In order to do this, SyNAP converts neural network models from their original representation (e.g.
Tensorflow Lite or ONNX) and optimizes and compiles them for the target hardware.

This model optimization can occur at one of two stages:

    - *Pre-optimized* - a binary specific to the target hardware is compiled ahead of time.

    - *Just-in-time* (JIT) - at runtime, compiled at the moment the network is going to be executed.


.. note::

    For embedded applications with a single hardware target, *pre-optimization* is resource optimial.

    For quick prototyping or portability across hardware targets, *JIT-optimization* offers flexibility.

    

Pre-optimizing Models
------------------------

In this mode the network has to be converted from its original representation (e.g.
Tensorflow Lite) to the internal SyNAP representation, optimized for the target hardware.
Doing the optimization offline allows to perform the highest level of optimizations possible
without the tradeoffs of the just-in-time compiler.

In most cases the model conversion can be done with a one-line command using SyNAP toolkit.
SyNAP toolkit also supports more advanced operations, such as network quantization and preprocessing.
Optionally an offline model can also be signed and encrypted to support Synaptics SyKURE\ :sup:`TM`
secure inference technology.

.. note::

    a compiled model is target-specific and will fail to execute on a different hardware

.. figure:: images/offline_conversion.png

    Pre-optimization and execution


JIT Optimization
-----------------------

JIT Optimization allows the execution of a model directly without any
intermediate steps. This is the most flexible method as all the required conversions and
optimizations are done on the fly at runtime, just before the model is executed. The price to be paid
for this is that model compilation takes some time (typically a few seconds) when the model
is first executed.
Another important limitation is that online execution is not available in a secure media path, that is
to process data in secure streams.

.. figure:: images/online_conversion.png

   JIT Optimization and execution





.. raw:: latex

    \clearpage


NPU Hardware Capabilities
-------------------------

The NPU itsef actually consists of multiple units. These units can execute in parallel when possible
to reduce inference times as much as possible. Three types of units are available:

    - **Convolutional Core**: these units are highly optimized to execute convolutions.
      Cannot be used to implement any other layer.
    - **Tensor Processor**: optimized to execute highly parallel operations, such as tensor-add.
      The *Lite* version is similar but supports a reduced operation set.
    - **Parellel Processing Unit**: very flexible unit that can be programmed to process tensors
      with customized kernels. It supports SIMD execution but it is less specialized (so less
      efficient) than the Neural Network Engine and Parellel Processing Units.

In addition the NPU also contains an internal static RAM which is used to provide fast
access to the data and/or weights thus reducing the need to access the slower external memory
during processing.


.. figure:: images/NPU.png
    :scale: 60 %

    NPU Architecture


The NPU of each SoC differ in the number of units it contains:

    +--------------+------------------------+-------------------+---------------------------+
    | SoC          | Neural Network Core    | Tensor Processor  | Parallel Processing Unit  |
    +==============+========================+===================+===========================+
    | VS640,       |                      4 |        2 + 4 Lite |                         1 |
    | SL1640       |                        |                   |                           |
    +--------------+------------------------+-------------------+---------------------------+
    | VS680,       |                     22 |                 8 |                         1 |
    | SL1680       |                        |                   |                           |
    +--------------+------------------------+-------------------+---------------------------+


