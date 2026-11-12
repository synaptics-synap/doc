SyNAP Release Notes
*******************

Version 3.2.0
=============

Toolkit
-------

- New features

  - Added pip wheels for Python 3.12 and 3.10
  - Introduced a new Detector class for post-processing YOLOv8 segmentation models
  - Added a Python-based model export pipeline for YOLOv8, YOLOv9, and YOLO11

- Improvements and updates

  - Upgraded to Verisilicon Acuity 6.30.6
  - Enhanced flexibility in requirements.txt to accommodate varying dependencies

- Fixes

  - Resolved mixed quantization issue with the OCR model

Version 3.1.0
=============

Toolkit
-------

- New features

  - Support importing models in TorchScript format
  - Progress indicator when quantizing models (can be disabled with --silent)

- Improvements and updates

  - Error indication when model output directory not mounted in docker container

Version 3.0.1
=============

Runtime
-------
 
- Fixes

  - Spurious error log when GPU delegate specified for tlite model


Toolkit
-------

- Fixes

  - Heterogeneous model conversion with multiple NPU subgraphs (conversion was successful but
    execution of the generated model failed)


Version 3.0.0
=============

Release date: 2024.03.01

Runtime
-------

- New features

  - Support for models in .synap format (C++ API fully backward compatible with SyNAP 2.x)
  - Support for heterogeneous model execution (NPU, CPU, GPU)
  - Full support and compatibility with legacy SyNAP 2.x models (*model.nb* and *model.json*)
  - Integrate Onnx runtime 1.16.3
  - Integrate TFlite runtime 2.15
  - TimVx delegate for TFlite for improved online inference on NPU
  - Optimized model benchmark binary ``benchmark_model`` integrating TimVx delegate
  

Toolkit
-------

- New features

  - Support for heterogeneous model conversion (NPU, CPU, GPU). The desired delegate(s) can be
    selected at model compilation time.
  - Generates *.synap* format by default. The *.synap* format is a bundle that contains both the
    model subgraph(s) and the companion meta-information. This replaces the *model.nb* and
    *model.json* files in SyNAP 2.x. It's still possible to generate the legacy *model.nb* and
    *model.json* files compatible with SyNAP 2.x runtime by specifying the ``--out-format nb``
    option when converting the model.
  - New preprocessing option to accept model input in 32-bits floating point

- Improvements and updates

  - Inference time for some models with mixed quantization


- Fixes

  - Preprocessing support for non-quantized models
  - Mixed quantization for tflite models ("No layers to requantize" error)
  - Accuracy issues with some models when using mixed quantization


Version 2.8.1
=============

Toolkit
-------

- Fixes

  - Import of Tensorflow .nb models
  - Import of ONNX models containing MaxPool layers
  - Import of ONNX models containing Slice layers


Version 2.8.0
=============

Runtime
-------

- New features

  - Detector now supports 'yolov8' format
  - Tensor now supports assignment from float and int16 data

- Improvements and updates

  - Image Preprocessor now adds horizontal or vertical gray bars when importing an image to
    preserve proportions. The image is always kept at the center.
  - Verisilicon software stack upgraded to Ovxlib 1.1.84
  - Improvements and clarifications in SyNAP.pdf user manual

- Fixes

  - Layer-by-layer profiling now provides more accurate timings


Toolkit
-------

- Improvements and updates

  - Verisilicon Acuity 6.21.2
  - Conversion docker updated to Tensorflow 2.13.0 and ONNX 1.14.0

- Fixes

  - Issues with mixed quantization with some models


Version 2.7.0
=============

Runtime
-------

- New features

  - Face recognition support
  - Optional OpenCV support
  - Model import tutorial: SyNAP_ModelImport.pdf

- Improvements and updates

  - Load network directly from a user buffer (avoid data copy)
  - Verisilicon software stack upgraded to Unify driver 6.4.13 and ovxlib 1.1.69
  - Improvements and clarifications in SyNAP.pdf user manual

- Fixes

  - Bounding box scaling in postprocessing for 'yolov5' format


Toolkit
-------

- New features

  - Model preprocessing now supports nv12 format

- Improvements and updates

  - Verisilicon Acuity 6.15.0
  - Conversion docker to ubuntu 22.04 and tensorflow 2.10.0

- Fixes

  - Import of .pb models when post-processing enabled (skip reordering)
  - Support relative model pathnames in model_convert.py


Version 2.6.0
=============

Runtime
-------

- New features

  - Tensor assign() supports data normalization
  - Preprocessor supports 16-bits models
  - Preprocessor supports models with preprocessing and cropping
  - Preprocessor rescale now preserves the input aspect-ratio by default
    (a gray band is added on the bottom of the image if needed)
  - Support for scalar tensors
  - Detector supports yolov5 output format
  - Buffer sharing (allows to share the tensor memory between different networks avoiding data copy)

- Improvements and updates

  - Support 64bits compilation

- Fixes

  - Fix Tensor::set_buffer in case the same Buffer is assigned/deassigned multiple times
  - Fix model json parsing for 16-bits models


Toolkit
-------

- New features

  - Support compilation of models with embedded preprocessing including: format conversion
    (eg. YUV to RGB), layout conversion (eg. NCHW to NHWC), normalization and cropping
  - Support "full" model quantization mode
  - Mixed quantization: the user can mix 8-bits and 16-bits quantization in the same model by
    specifying the quantization type for each layer

- Improvements and updates

  - Quantization images now rescaled preserving the aspect-ratio of the content


Version 2.5.0
=============

Runtime
-------

- New features

  - Support for NNAPI compilation cache
  - Move support for Network objects in C++ API
  - Unified libovxlib.so supporting both VS640 and VS680

- Improvements and updates

  - Faster init time for NNAPI online inference (release mode)
  - Error checking on out-of-sequence API calls
  - Accuracy of layer-by-layer metrics
  - Unify all logcat messages with "SyNAP" tag
  - Memory optimization: on-demand loading of compressed OpenVX kernels (saves more than 80MB of RAM)
  - Verisilicon software stack upgraded to Unify driver 6.4.11 and ovxlib 1.1.50
  - Overall improvements now achieve a score of 33.8 with AIBenchmark 4.0.4

- Fixes

  - Layer-by-layer metrics was not working on some models (inference fail)

Toolkit
-------

- New features

  - Support compilation of Caffe models

- Improvements and updates

  - Verisilicon Acuity 6.9
  - Error reporting for quantization issues


Version 2.4.0
=============

Runtime
-------

- New features

  - New internal SyNAP model compilation cache
    This dramatically improves model initialization time during the first inference. Typical speedup
    of the first inference is by a factor of 3, can be a factor of 20 or more on some models.

- Improvements and updates

  - Further runtime optimizations allowing VS680 to achieve a score of 31.5 in ai-benchmark 4.0.4
  - SyNAP default log level is now WARNING (instead of no logs)
  - Operator support table updated in User Manual

- Fixes

  - Correctly support multiple online models at the same time
    Compiling multiple online models in parallel could in some cases give issues (SyNAP HAL crash)
    in previous releases.

Toolkit
-------
- New features

  - New internal SyNAP model compilation cache
    This dramatically improves model compilation time. Typical speedup is by a factor of 3, can be a
    factor of 20 or more on some models.

- Fixes

  - Conversion of ONNX models when output layer name(s) specified explicitly in metafile


Version 2.3.0
=============

Runtime
-------

- New features

  - By-layer profiling support
    Low-level driver and runtime binaries and libraries now support layer by layer profiling of
    any network.
  - Allocator API in synap device and associated SE-Linux rules
    This is the default allocator in libsynapnb and the NNAPI is already making use of it.
    This also enable any user application (native or not) to execute models without root
    priviledge, including the synap_cli family.
  - Sample Java support

- Improvements and updates

  - Reorganize libraries. We now have the following libraries:

    - libsynapnb.so: core EBG execution library
    - libsynap_preprocess.a: pre-processing
    - libsynap_postprocess.a: post-processing (classification, detection, etc)
    - libsynap_img.a: image processing utilities
    - libsynap_utils.a: common utilities
    - libsynap_app.a: application support utilities
    - Repeat mode to synap_cli
    - EBG for profiling generation to synap_cli_nb


- Fixes

  - Memory leak when running models

Toolkit
-------


- New features

  - By-layer profiling
  - Secure Model Generation for VS640 (VS680 was already supported)
    Note: This feature requires special agreement with Synaptics in order to be enabled.


Version 2.2.1
=============

Runtime
-------


- New features

  - New NNHAL architecture (NNAPI)
    NNRT is now using libsynapnb directly to execute an EBG model; this saves memory and
    simplify dependencies.
    VIPBroker dependency was removed from OVXLIB which is now only used as a graph compiler.

- Fixes

  - Memory leak when dellocating Buffers


Version 2.2.0
=============

Runtime
-------

.. table:: 
   :widths: 10,10,80

   ============== =========== =======================================================================
   **Component**    **Type**    **Description**
   ============== =========== =======================================================================
   all            Add         Linux Baseline VSSDK support
   lib            Add         ``Preprocessor`` class with support for image rescaling and conversion
   lib            Add         ``Classifier`` postprocessor
   lib            Add         `Detector`` postprocessors with full support for
                              ``TFLite_Detection_PostProcess`` layer with external anchors
   lib            Add         ``Label_info`` class
   lib            Add         ``ebg_utils``: new shared library for EBG format manipulation
   lib            Fix         NPU lock functionality
   lib            Remove      ``nnapi_lock()`` API, use vendor.NNAPI_SYNAP_DISABLE property instead.
                              This doesn't require any special permission for the application.
   bin            Add         ``synap_cli_nb``: new program for NBG to EBG conversion
   driver         Optimize    Much reduced usage of contiguous memory
   NNAPI          Update      VSI OVXLIB to 1.1.37
   NNAPI          Update      VSI NNRT/NHAL to 1.3.1
   NNAPI          Add         More operators supported
   NNAPI          Optimize    Much higher score for some AI-benchmark models (ex: PyNET and U-Net)
   NNAPI          Add         Android CTS/VTS pass for both VS680 and VS640
   ============== =========== =======================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ===============================================================================
   **Type**    **Description**
   =========== ===============================================================================
   Fix         Crash when importing one TFLite object-detection models
   Add         Full support for TFLite_Detection_PostProcess layerb
   Add         Support for ${ANCHOR} and ${FILE:name} variables in tensor format string
   Add         Support for ${ENV:name} variables substitution in model yaml metafile
   Add         Support for security.yaml file
   Update      VSI acuity toolkit to 6.3.1
   Update      Improved error checking
   Update      Layer name and shape are now optional when doing quantization
   Add         Support for single mean value in metafile
   Remove      synap_profile tool
   Fix         Handling of relative paths
   =========== ===============================================================================


Version 2.1.1
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ===============================================================================
   **Type**    **Description**
   =========== ===============================================================================
   Fix         Timeout expiration in online model execution
               (ai-benchmark 4.0.4 now runs correctly)
   Fix         Issues in ``sysfs`` diagnostic
   Change      On android ``synap`` logs don't go to ``stderr`` anymore (just to logcat)
   =========== ===============================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ===============================================================================
   **Type**    **Description**
   =========== ===============================================================================
   Fix         ``sysfs`` section in User Manual 
   Update      Inference timings section in User Manual now includes y-uv models
   =========== ===============================================================================


Version 2.1.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Add         Full support for SyKURE\ :sup:`TM`: Synaptics secure inference technology
   Improve     Tensor Buffers for NNAPI and synapnb now allocated in non-contiguous memory
               by default
   Add         Buildable source code for ``synap_cli_ip`` sample application
   Change      Per-target organization of libraries and binaries in the install tree
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Add         Support for NHWC tensors in rescale layer
   Fix         Tensor format in json file for converted models
   Improve     Reorganize sections in User Manual
   =========== ==========================================================================


Version 2.0.1
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Improve     Online inference performance
   Add         Option to show SyNAP version in synap_cli application
   Add         Buildable source code for all SyNAP sample applications and libraries  
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Update      Model coversion tool (fixes offline performance drop in some cases)
   =========== ==========================================================================


Version 2.0.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Improve     Inference engine now supports the new EBG (Executable Binary Graph) model
               format.

               Compared to previous NBG format, EBG brings several impovements:

               - Much faster loading time

               - Better maintenance and stability (10x lighter driver source code)

               - Pave the way to secure inference


               NBG models are not supported anymore.
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Update      Model coversion tools now support EBG generation
   =========== ==========================================================================


Version 1.5.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Add         Synap device information and statistics in sysfs
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Update      Conversion toolkit to v. 5.24.5
   Improve     Model quantization algorithm
   Add         Generate network information file when model is converted
   Add         Host tools binaries and libraries in toolkit/bin and toolkit/lib
   =========== ==========================================================================


Version 1.4.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Fix         CTS/VTS now run successfully with NNAPI
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Update      Conversion toolkit to v. 5.24
   Add         Model benchmark binary: /vendor/bin/android_arm_benchmark_model
   Add         Model test script and specs
   =========== ==========================================================================


Version 1.3.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**     **Description**
   =========== ==========================================================================
   Change      Update and cleanup object Detector API 
   Change      synap_cli_od allows to specify model
   Add         synap_cli_od source code
   Add         Cmake standalone build for synap_cli_ic and synap_cli_od
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   Add         Import and conversion of ONNX models
   =========== ==========================================================================


Version 1.2.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**     **Description**
   =========== ==========================================================================
   Change      Remove private implementation details from Buffer.hpp 
   Change      Switch memory allocation to dmabuf
   Fix         Model pathnames and documentation for object detection
   Add         Synap device
   Add         OpenVX headers and librairies
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**    **Description**
   =========== ==========================================================================
   New         Model quantization support
   =========== ==========================================================================


Version 1.1.0
=============

Runtime
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**     **Description**
   =========== ==========================================================================
   New         NNAPI lock support: :code:`Npu::lock_nnapi()`
   =========== ==========================================================================


Toolkit
-------

.. table:: 
   :widths: 10,90

   =========== ==========================================================================
   **Type**     **Description**
   =========== ==========================================================================
   New         Model profiling tool: ``synap_profile.py``
   New         NNAPI benchmarking script: ``synap_benchmark_nnapi.sh``
   =========== ==========================================================================


Version 1.0.0
=============

Initial Version.

