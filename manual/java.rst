Direct access in Android Applications
=====================================

In Android, in addition to NN API, SyNAP can be directly accessed by applications. Direct access
to SyNAP main benefits are zero-copy input/output and execution of optimized models compiled ahead
of time with the SyNAP toolkit.

Access to SyNAP can be performed via custom JNI C++ code using the ``synapnb`` library. The library
can be used as usual, the only constraint is to use the Synap allocator, which can be
obtained with ``synap_allocator()``.

Another option, is to use custom JNI C code using the ``synap_device`` library. In this case there
are no constraints. The library allows to create new I/O buffers with the function
``synap_allocate_io_buffer``. It is also possible to use existing DMABUF handles obtained for
instance from gralloc with ``synap_create_io_buffer``. The DMABUF can be accessed with standard
Linux DMABUF APIs (i.e. mmap/munmap/ioctls).

SyNAP provides a sample JNI library that shows how to use the ``synap_device`` library in a Java
application. The code is located in ``java`` and can be included in an existing Android application
by adding the following lines to the ``settings.gradle`` of the application::

    include ':synap'
    project(':synap').projectDir = file("[absolute path to synap]/java")

The code can then be used as follows:

.. literalinclude:: ../../framework/java/src/main/java/com/synaptics/synap/InferenceEngine.java
   :language: java

.. note::

    To simplify application development by default VSSDK allows untrusted applications (such as
    application sideloaded or downloaded from Google Play store) to use the SyNAP API. Since the
    API uses limited hardware resources this can lead to situations in which a 3rd party
    application interferes with platform processes. To restrict access to SyNAP only to
    platform applications remove the file ``vendor/vsi/sepolicy/synap_device/untrusted_app.te``.
