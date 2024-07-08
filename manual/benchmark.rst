Reference Models
================

Timings
-------

The tables in this section contain inference timings for a set of representative models.
The quantized models have been imported and compiled offline using SyNAP toolkit.
The floating point models are benchmarked for comparison purpose with the corresponding
quantized models.

The *mobilenet_v1*, *mobilenet_v2*, *posenet* and *inception* models are open-source models
available in `tflite` format from *TensorFlow Hosted Models* page:
``https://www.tensorflow.org/lite/guide/hosted_models``

*yolov5* models are available from  ``https://github.com/ultralytics/yolov5``,
while *yolov5_face* comes from ``https://github.com/deepcam-cn/yolov5-face``.

Other models come from AI-Benchmark APK: ``https://ai-benchmark.com/ranking_IoT.html``.

Some of the models are Synaptics proprietary, including test models, object detection
(*mobilenet224*), super-resolution and format conversion models.

The model *test_64_128x128_5_132_132* has been designed to take maximum advantage of the computational capabilities of the NPU.
It has 64 5x5 convolutions with a [1, 128, 128, 132] input and output.
Its execution requires 913'519'411'200 operations (0.913 TOPs). Inference time shows that
in the right conditions VS640 and SL1640 achieve above 1.6 TOP/s while VS680 and SL1680 able to achieve above 7.9 TOP/s.
For 16-bits inference the maximum TOP/s can be achieved with *test_64_64x64_5_132_132*. With this model
we achieve 0.45 TOP/s on VS640/SL1640 and above 1.7 TOP/s on VS680/SL1680.
For actual models used in practice it's very difficut to get close to this level of performance and it's
hard to predict the inference time of a model from the number of operation it contains. The only reliable
way is to execute the model on the platform and measure.

Remarks:

- In the following tables all timing values are expressed in milliseconds

- The columns *Online CPU* and *Online NPU* represent the inference time obtained by running
  the original `tflite` model directly on the board (*online* conversion)

- Online CPU tests have been done with 4 threads (``--num_threads=4``) on both *vs680* and *vs640*

- Online CPU tests of *floating point models* on *vs640* have been done in *fp16* mode (``--allow_fp16=true``)

- Online NPU tests executed with the *timvx* delegate (``--external_delegate_path=libvx_delegate.so``)

- The *Offline Infer* column represents the inference time obtained by using a model converted offline
  using SyNAP toolkit (median time over 10 consecutive inferences)

- The *Online* timings represent the minimum time measured (for both init and inference).
  We took minimim instead of average because this is measure less sensitive to outliers due to the
  test process being temporarily suspended by the CPU scheduler

- Online timings, in particular for init and CPU inference, can be influenced by other processes
  running on the board and the total amount of free memory available. We ran all tests on Android
  AOSP/64bits with 4GB of memory on VS680 and 2GB on VS640. Running on Android GMS or 32-bits OS or
  with less memory can result in longer init and inference times

- Offline tests have been done with non-contiguous memory allocation and no cache flush

- Models marked with `*` come precompiled and preinstalled on the platform


.. raw:: latex

    \clearpage

Inference timings on VS680 and SL1680
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These tables show the inference timings for a set of models on VS680 and SL1680.
All tests have been done on 64-bits OS with 4GB of memory.

.. table:: Synaptics models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs680_synaptics.rst

.. table:: Open models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs680_open.rst


.. raw:: latex

    \clearpage

.. table:: AiBenchmark 4 models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs680_aibench4.rst

.. table:: AiBenchmark 5 models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs680_aibench5.rst


.. raw:: latex

    \clearpage


Inference timings on VS640 and SL1640
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These tables show the inference timings for a set of models on VS640 and SL1640.
All tests have been done on 64-bits OS with *2GB* of memory.

.. table:: Synaptics models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs640_synaptics.rst

.. table:: Open models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs640_open.rst


.. raw:: latex

    \clearpage

.. table:: AiBenchmark 4 models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs640_aibench4.rst


.. table:: AiBenchmark 5 models
   :widths: 45,11,11,11,11,11,11,4
   :class: widetable

   .. include:: benchmark/test_report_vs640_aibench5.rst


.. raw:: latex

    \clearpage


Super Resolution
----------------

Synaptics provides two proprietary families of super resolution models: *fast* and *qdeo*, the former
provides better inference time, the latter better upscaling quality.
They can be tested using ``synap_cli_ip`` application, see :ref:`synap_cli_ip`.

These models are preinstalled in ``$MODELS/image_processing/super_resolution`` .


.. table:: Synaptics SuperResolution Models on Y+UV Channels
   :widths: 40,20,20,10
   :align: right

   ================================= ================= ================= ===========
   Name                              **Input Image**   **Ouput Image**   **Factor**
   ================================= ================= ================= ===========
   sr_fast_y_uv_960x540_3840x2160    960x540           3840x2160           4
   sr_fast_y_uv_1280x720_3840x2160   1280x720          3840x2160           3
   sr_fast_y_uv_1920x1080_3840x2160  1920x1080         3840x2160           2
   sr_qdeo_y_uv_960x540_3840x2160    960x540           3840x2160           4
   sr_qdeo_y_uv_1280x720_3840x2160   1280x720          3840x2160           3
   sr_qdeo_y_uv_1920x1080_3840x2160  1920x1080         3840x2160           2
   sr_qdeo_y_uv_640x360_1920x1080    640x360           1920x1080           3
   ================================= ================= ================= ===========


.. _conversion_models:

Format Conversion
-----------------

Conversion models can be used to convert an image from ``NV12`` format to ``RGB``.
A set of models is provided for the most commonly used resolutions.
These models have been generated by taking advantage of the
preprocessing feature of the ``SyNAP`` toolkit (see :ref:`preprocessing`) and can be used to convert
an image so that it can be fed to a processing model with ``RGB`` input.

These models are preinstalled in ``$MODELS/image_processing/preprocess`` and can be
tested using ``synap_cli_ic2`` application, see :ref:`synap_cli_ic2`.

.. table:: Synaptics Conversion Models NV12 to RGB 224x224
   :widths: 40,20,20
   :align: right

   ====================================== ====================== =====================
   Name                                   **Input Image (NV12)** **Ouput Image (RGB)**
   ====================================== ====================== =====================
   convert_nv12@426x240_rgb@224x224        426x240               224x224
   convert_nv12@640x360_rgb@224x224        640x360               224x224
   convert_nv12@854x480_rgb@224x224        854x480               224x224
   convert_nv12@1280x720_rgb@224x224      1280x720               224x224
   convert_nv12@1920x1080_rgb@224x224     1920x1080              224x224
   convert_nv12@2560x1440_rgb@224x224     2560x1440              224x224
   convert_nv12@3840x2160_rgb@224x224     3840x2160              224x224
   convert_nv12@7680x4320_rgb@224x224     7680x4320              224x224
   ====================================== ====================== =====================

.. table:: Synaptics Conversion Models NV12 to RGB 640x360
   :widths: 40,20,20
   :align: right

   ====================================== ====================== =====================
   Name                                   **Input Image (NV12)** **Ouput Image (RGB)**
   ====================================== ====================== =====================
   convert_nv12@426x240_rgb@640x360        426x240               640x360
   convert_nv12@640x360_rgb@640x360        640x360               640x360
   convert_nv12@854x480_rgb@640x360        854x480               640x360
   convert_nv12@1280x720_rgb@640x360      1280x720               640x360
   convert_nv12@1920x1080_rgb@640x360     1920x1080              640x360
   convert_nv12@2560x1440_rgb@640x360     2560x1440              640x360
   convert_nv12@3840x2160_rgb@640x360     3840x2160              640x360
   convert_nv12@7680x4320_rgb@640x360     7680x4320              640x360
   ====================================== ====================== =====================
   
.. table:: Synaptics Conversion Models NV12 to RGB 1920x1080
   :widths: 40,20,20
   :align: right

   ====================================== ====================== =====================
   Name                                   **Input Image (NV12)** **Ouput Image (RGB)**
   ====================================== ====================== =====================
   convert_nv12@426x240_rgb@1920x1080      426x240               1920x1080
   convert_nv12@640x360_rgb@1920x1080      640x360               1920x1080
   convert_nv12@854x480_rgb@1920x1080      854x480               1920x1080
   convert_nv12@1280x720_rgb@1920x1080    1280x720               1920x1080
   convert_nv12@1920x1080_rgb@1920x1080   1920x1080              1920x1080
   convert_nv12@2560x1440_rgb@1920x1080   2560x1440              1920x1080
   convert_nv12@3840x2160_rgb@1920x1080   3840x2160              1920x1080
   convert_nv12@7680x4320_rgb@1920x1080   7680x4320              1920x1080
   ====================================== ====================== =====================


