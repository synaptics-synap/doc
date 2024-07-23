Introduction
============

SyNAP optimizes neural network models for on-device inference by targeting *NPU* or *GPU* hardware accelerators in `Synaptics Astra Embedded Processors <https://www.synaptics.com/products/embedded-processors>`_. To do this, it takes models in their original representation (e.g. Tensorflow Lite, PyTorch or ONNX) and compiles them to a binary network graph `.synap` format specific to the target hardware, ready for inference. 

Compiling models
----------------

For embedded software with a single hardware target, an *ahead of time compilation* approach is optimal - and in most cases can be done with a :ref:`single command<#>`. Optimization options (e.g. :ref:`mixed quantization<tutorials/model_import>`, :ref:`heterogeneous inference<heterogeneous_inference>`) can be passed at compile time using a :ref:`YAML metafile<conversion-metafile>`, and the model can be signed and encrypted to support Synaptics SyKURE\ :sup:`TM`
secure inference technology. 

.. figure:: images/preoptimized.svg

.. note::
  While optimal for the target hardware, a pre-optimized model is target specific and will fail to execute on different hardware. 

Running inference
-----------------

There are a number of ways you can run inference using compiled `.synap` models on Synaptics Astra hardware:

* Image classification, object detection and image processing using ``synap_cli`` commands. 

* Gstreamer plugin and Python examples for streaming media (e.g. webcam object detection).

* Embedded applications developed in C++ or Python can use the :doc:`SyNAP Framework API<framework_api>`.

.. important::

    The simplest way to start experimenting with *SyNAP* is to use the sample precompiled models and
    applications that come preinstalled on the Synaptics Astra board.

JIT compilation
---------------
For portable apps (e.g. targeting Android) you might consider the JIT compilation approach instead. This approach uses a :ref:`Tensorflow Lite external delegate based on TIM-VX<timvx_inference>` to run inference using the original `.tflite` model directly. 

This offers the greatest hardware portability, but there are a few disadvantages to this approach. Using this method requires any hardware-specific optimizations be done in the TensorFlow training or TFLite model export stages, which is much more involved than post-training quantization using SyNAP. Additionally, initialization time can take a few seconds on first inference, and secure media paths are not available.

Model Profiling & Benchmarks
----------------------
SyNAP provides :ref:`analysis tools<sysfs-inference-counter>` in order to identify bottlenecks and optimize models. These include:

* Overall model inference timing
* NPU runtime statistics (e.g. overall layer and I/O buffer utilization)
* Model profiling (e.g. per-layer operator type, execution time, memory usage)

You can also find a :doc:`comprehensive list of reference models and benchmarks<benchmark>`.

NPU Hardware
---------------------------------------

SyNAP aims to make best use of supported :ref:`neural network operators<npu_operators>` in order to accelerate on-device inference using the available NPU or GPU hardware. The NPUs themselves consist of several distinct types of functional unit:

    - **Convolutional Core**: Optimized to only execute convolutions (int8, int16, float 16).
    - **Tensor Processor**: Optimized to execute highly parallel operations (int8, int16, float 16).
    - **Parellel Processing Unit**: 128-bit SIMD execution unit (slower, but more flexible).
    - **Internal RAM**: used to cache data and weights.





    +--------------+------------------------+-------------------+---------------------------+
    | Chip         | Neural Network Core    | Tensor Processor  | Parallel Processing Unit  |
    +==============+========================+===================+===========================+
    | VS640,       |                      4 |   2 Full + 4 Lite |                         1 |
    | SL1640       |                        |                   |                           |
    +--------------+------------------------+-------------------+---------------------------+
    | VS680,       |                     22 |            8 Full |                         1 |
    | SL1680       |                        |                   |                           |
    +--------------+------------------------+-------------------+---------------------------+

