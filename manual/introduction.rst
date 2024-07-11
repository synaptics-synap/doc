Introduction
============

The purpose of SyNAP is to optimize the execution of neural network models by taking best advantage of *NPU* or *GPU* hardware accelerators on-board `Synaptics Astra Processors <https://www.synaptics.com/products/embedded-processors>`_. 

In order to do this, SyNAP converts the models from their original representation (e.g. Tensorflow Lite, PyTorch or ONNX) and compiles them into the `.synap` binary format specific to the target hardware. 


Optimizing models
-----------------------

For embedded software with a single hardware target, an *ahead of time compilation* approach is resource optimial - and in most cases can be done with a :ref:`single command in SyNAP <working_with_models>`. 

You can also pass advanced optimization options (e.g. :ref:`mixed quantization <../tutorials/model_import>`, :ref:`heterogeneous inference <heterogeneous_inference>`) using a :ref:`YAML metafile <working_with_models.html#conversion-metafile>`. The model can also be signed and encrypted to support Synaptics SyKURE\ :sup:`TM`
secure inference technology.


.. figure:: images/preoptimized.svg


.. note::

    While optimal for the target hardware, a pre-optimized model is target specific and will fail to execute on different hardware

JIT Compilation
-----------------------

Just-in-time compilation enables the execution of TensorFlow Lite models directly. For applications that require portability (e.g. must be able to run on an Astra embedded board or an Android phone), the JIT compilation approach offers flexibilty at the cost of performance. 

.. note::

    JIT compilation is flexible, but initialization time can take a few seconds, and additional optimization and secure media paths are not available.


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


