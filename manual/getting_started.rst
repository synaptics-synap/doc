Running Inference
=================

Methods
-------
1) The easiest way to get started is using the CLI commands. 

2) For application development, a C++ library API etc



.. highlight:: none

The simplest way to start experimenting with *Synp* is to use the sample precompiled models and
applications that come preinstalled on the board.

.. important::

    On Android the sample models can be found in :code:`/vendor/firmware/models/` while
    on Yocto Linux they are in :code:`/usr/share/synap/models/`.
    In this document we will refer to this directory as :code:`$MODELS`.

The models are organized in broad categires according to the type of data they take in input and
the information they generate in output.
Inside each category, models are organized per topic (for example "imagenet") and for each
topic a set of models and sample input data is provided.

For each category a corresponding command line test application is provided.

.. table:: Model Classification
   :widths: 30,10,40,20

   ======================== ==================== ========================================= ============
   **Category**             **Input**            **Output**                                **Test App**
   ======================== ==================== ========================================= ============
   image_classification     image                probabilities (one per class)             synap_cli_ic
   object_detection         image                detections (bound.box+class+probability)  synap_cli_od
   image_processing         image                image                                     synap_cli_ip
   ======================== ==================== ========================================= ============


In addition to the specific applications listed above ``synap_cli`` can be used to execute models of
all categories. The purpose of this application is not to provide high-level outputs but to measure
inference timings. This is the only sample application that can be used with models
requiring secure inputs or outputs.


.. _synap_cli_ic:

``synap_cli_ic`` application
------------------------------

This command line application allows to easily execute *image_classification* models.

It takes in input:

- the converted synap model (*.synap* extension)

- one or more images (*jpeg* or *png* format)

It generates in output:

- the top5 most probable classes for each input image provided

.. note::

    The jpeg/png input image(s) are resized in SW to the size of the network input tensor. This
    is not included in the classification time displayed.


Example::

    $ cd $MODELS/image_classification/imagenet/model/mobilenet_v2_1.0_224_quant
    $ synap_cli_ic -m model.synap ../../sample/goldfish_224x224.jpg
    Loading network: model.synap
    Input image: ../../sample/goldfish_224x224.jpg
    Classification time: 3.00 ms
    Class  Confidence  Description
        1       18.99  goldfish, Carassius auratus
      112        9.30  conch
      927        8.70  trifle
       29        8.21  axolotl, mud puppy, Ambystoma mexicanum
      122        7.71  American lobster, Northern lobster, Maine lobster, Homarus americanus


``synap_cli_od`` application
----------------------------

This command line application allows to easily execute *object_detection* models.

It takes in input:

- the converted synap model (*.synap* extension)

- optionally the confidence threshold for detected objects

- one or more images (*jpeg* or *png* format)

It generates in output:

- the list of object detected for each input image provided and for each of them the following information:

    - bounding box
    - class index
    - confidence

.. note::

    The jpeg/png input image(s) are resized in SW to the size of the network input tensor.


Example::

    $ cd $MODELS/object_detection/people/model/mobilenet224_full1/
    $ synap_cli_od -m model.synap ../../sample/sample001_640x480.jpg
    Input image: ../../sample/sample001_640x480.jpg (w = 640, h = 480, c = 3)
    Detection time: 26.94 ms
    #   Score  Class  Position  Size     Description
    0   0.95       0   94,193    62,143  person


.. important::

    The output of object detection models is not standardized, many different formats exist.
    The output format used has to be specified when the model is converted, see :ref:`model_conversion_tutorial`.
    If this information is missing or the format is unknown ``synap_cli_od`` doesn’t know how to
    interpret the result and so it fails with an error message: *"Failed to initialize detector"*.


.. _synap_cli_ip:

``synap_cli_ip`` application
------------------------------

This command line application allows to execute *image_processing* models.
The most common case is the execution of super-resolution models that take in input a low-resolution
image and generate in output a higher resolution image.

It takes in input:

- the converted synap model (*.synap* extension)

- optionally the region of interest in the image (if supported by the model)

- one or more raw images with one of the following extensions:
  *nv12*, *nv21*, *rgb*, *bgr*, *bgra*, *gray*  or *bin*


It generates in output:

- a file containing the processed image in for each input file.
  The output file is called ``outimage<i>_<W>x<H>.<ext>``, where <i> is the index of the corresponding 
  input file, <W> and <H> are the dimension of the image, and <ext> depends on the type of the
  output image, for example ``nv12`` or ``rgb``.
  By output files are created in the current directory, this can be changed with the ``--out-dir`` option.

.. note::

    The input image(s) are automatically resized to the size of the network input tensor.
    This is not supported for ``nv12``: if the network takes in input an ``nv12`` image,
    the file provided in input must have the same format and the *WxH* dimensions of the image must
    correspond to the dimensions of the input tensor of the network.

.. note::

    Any ``png`` and ``jpeg`` image can be converted to ``nv12`` and rescaled to the required size 
    using the ``image_to_raw`` command available in the *SyNAP* ``toolkit``
    (for more info see :ref:`using-docker-label`).
    In the same way the generated raw ``nv12`` or ``rgb`` images can be converted to ``png`` or ``jpeg``
    format using the ``image_from_raw`` command.


Example::
    
    $ cd $MODELS/image_processing/super_resolution/model/sr_qdeo_y_uv_1920x1080_3840x2160
    $ synap_cli_ip -m model.synap ../../sample/ref_1920x1080.nv12
    Input buffer: input_0 size: 1036800
    Input buffer: input_1 size: 2073600
    Output buffer: output_13 size: 4147200
    Output buffer: output_14 size: 8294400
    
    Input image: ../../sample/ref_1920x1080.nv12
    Inference time: 30.91 ms
    Writing output to file: outimage0_3840x2160.nv12


.. _synap_cli_ic2:

``synap_cli_ic2`` application
------------------------------

This application executes two models in sequence, the input image is fed to the first model and
its output is then fed to the second one which is used to perform classification as in ``synap_cli_ic``.
It provides an easy way to experiment with 2-stage inference, where for example the
the first model is a *preprocessing* model for downscaling and/or format conversion
(see :ref:`conversion_models`) and the second is an *image_classification* model.

It takes in input:

- the converted synap *preprocessing* model (*.synap* extension)

- the converted synap *classification* model (*.synap* extension)

- one or more images (*jpeg* or *png* format)

It generates in output:

- the top5 most probable classes for each input image provided

.. note::

    The shape of the output tensor of the first model must match that of the input of the second model.


As an example we can use a preprocessing model to convert and rescale a ``NV12`` image to ``RGB``
so that it can be processed by the standard ``mobilenet_v2_1.0_224_quant`` model::

    $ pp=$MODELS/image_processing/preprocess/model/convert_nv12@1920x1080_rgb@224x224
    $ cd $MODELS/image_classification/imagenet/model/mobilenet_v2_1.0_224_quant
    $ synap_cli_ic2 -m $pp/model.synap -m2 model.synap ../../sample/goldfish_1920x1080.nv12
    
    Inference time: 4.34 ms
    Class  Confidence  Description
        1       19.48  goldfish, Carassius auratus
      122       10.68  American lobster, Northern lobster, Maine lobster, Homarus americanus
      927        9.69  trifle
      124        9.69  crayfish, crawfish, crawdad, crawdaddy
      314        9.10  cockroach, roach

The classification output is very close to what we get in :ref:`synap_cli_ic`, the minor difference
is due to the difference in the image rescaled from NV12. The bigger overall inference time is
due to the processing required to perform rescale and conversion of the input 1920x1080 image.


``synap_cli`` application
-------------------------

This command line application can be used to run models of all categories.
The purporse of :code:`synap_cli` is not to show inference results but to benchmark the network
execution times. So it provides additional options that allow to run inference mutiple time in order
to collect statistics.

An additional feature is that :code:`synap_cli` can automatically generate input images with random
content. This makes it easy to test any model even without having a suitable input file available.


Example::

    $ cd $MODELS/image_classification/imagenet/model/mobilenet_v2_1.0_224_quant
    $ synap_cli -m model.synap -r 50 random
    Flush/invalidate: yes
    Loop period (ms): 0
    Network inputs: 1
    Network outputs: 1
    Input buffer: input_0 size: 150528 : random
    Output buffer: output_66 size: 1001
    
    Predict #0: 2.68 ms
    Predict #1: 1.81 ms
    Predict #2: 1.79 ms
    Predict #3: 1.79 ms
    .....
    Inference timings (ms):  load: 55.91  init: 3.84  min: 1.78  median: 1.82  max: 2.68  stddev: 0.13  mean: 1.85

.. note::
    Specifying a ``random`` input is the only way to execute models requiring secure inputs.


``synap_init`` application
--------------------------

The purpose of this application is not to execute a model but just to initialize and lock the NPU.
It can be used to simulate a process locking the NPU for his exclusive usage.

Example to lock NPU access::

    $ synap_init -i --lock

The lock is released when the program exits or is terminated.


.. note::
    This prevents any process from accessing the NPU via both NNAPI and direct SyNAP API.
    Please refer to the next section to disable NPU access only for NNAPI.

.. note::
    While the NPU is locked it is still possible to create a Network from another process, but any
    attempts to do inference will fail.
    When this occours, the appropriate error message is added to the system log::
    
        $ synap_cli_ic
        Loading network: /vendor/firmware/models/image_classification/imagenet/model/mobilenet_v2_1.0_224_quant/model.synap
        Inference failed
        $ dmesg | grep NPU
        [ 1211.651] SyNAP: cannot execute model because the NPU is reserved by another user


Troubleshooting
---------------

SyNAP libraries and command line applications generate logging messages to help troubleshooting
in case something goes wrong. On Android these messages appear in logcat, while on linux they are sent
directly to the console.

There are 4 logging levels:

    - 0: verbose
    - 1: info
    - 2: warning
    - 3: error


The default level is 3, so that only error logs are generated.
It is possible to select a different level by setting the SYNAP_NB_LOG_LEVEL environment variable
before starting the application, for example to enable logs up to ``info``::

    export SYNAP_NB_LOG_LEVEL=1
    logcat -c; synap_cli_ic; logcat -d | grep SyNAP
    Input image: /vendor/firmware/models/image_classification/imagenet/sample/space_shuttle_224x224.jpg
    Classification time: 3.16 ms
    Class  Confidence  Description
      812       19.48  space shuttle
      ...
    1-08 15:10:57.185 830 830 I SyNAP : get_network_attrs():70: Parsing network metadata
    1-08 15:10:57.185 830 830 I SyNAP : load_model():252: Network inputs: 1
    1-08 15:10:57.185 830 830 I SyNAP : load_model():253: Network outputs: 1
    1-08 15:10:57.191 830 830 I SyNAP : resume_cpu_access():65: Resuming cpu access on dmabuf: 5
    1-08 15:10:57.193 830 830 I SyNAP : set_buffer():208: Buffer set for tensor: input_0
    1-08 15:10:57.193 830 830 I SyNAP : resume_cpu_access():65: Resuming cpu access on dmabuf: 6
    1-08 15:10:57.193 830 830 I SyNAP : set_buffer():208: Buffer set for tensor: output_66
    1-08 15:10:57.193 830 830 I SyNAP : do_predict():83: Start inference
    1-08 15:10:57.193 830 830 I SyNAP : suspend_cpu_access():54: Suspending cpu access on dmabuf: 5
    1-08 15:10:57.195 830 830 I SyNAP : do_predict():95: Inference time: 2.33 ms
    1-08 15:10:57.195 830 830 I SyNAP : resume_cpu_access():65: Resuming cpu access on dmabuf: 6
    1-08 15:10:57.196 830 830 I SyNAP : unregister_buffer():144: Detaching buffer from input tensor input_0
    1-08 15:10:57.196 830 830 I SyNAP : set_buffer():177: Unset buffer for: input_0
    1-08 15:10:57.196 830 830 I SyNAP : unregister_buffer():150: Detaching buffer from output tensor output_66
    1-08 15:10:57.196 830 830 I SyNAP : set_buffer():177: Unset buffer for: output_66
