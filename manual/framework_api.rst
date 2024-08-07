Framework API
=============

The core functionality of the Synap framework is to execute a precompiled neural network.
This is done via the :code:`Network` class. The Network class has been designed to be simple to use
in the most common cases while still being flexible enough for most advanced use-cases.
The actual inference will take place on different HW units (NPU, GPU, CPU or a combination of them)
according to how the model has been compiled.


.. highlight:: cpp


Basic Usage
-----------

Network Class
~~~~~~~~~~~~~

The :code:`Network` class is extremely simple, as shown in the picture here below.

There are just two things that can be done with a network:

    - load a model, by providing the compiled model in ``.synap`` format
    
    - execute an inference

A network also has an array of input tensors where to put the data to be processed, 
and an array of output tensors which will contain the result(s) after each inference.

.. uml::
    :scale: 65%
    :caption: Network class
    
    skinparam monochrome true
    skinparam handwritten false
    class Network {
        bool load_model(model)
        bool predict()
        
        Tensor inputs[]
        Tensor outputs[]
    }

.. doxygenclass:: synaptics::synap::Network
    :members:




Using a Network
~~~~~~~~~~~~~~~
The prerequisite in order to execute a neural network is to create a *Network* object and load its
model in ``.synap`` format. This file is generated when the network is converted using the
Synap toolkit.
This has to be done only once, after a network has been loaded it is ready to be used for inference:

1. put the input data in the Network input tensor(s)
2. call network :code:`predict()` method
3. get the results from the Network input tensor(s)

.. uml::
    :scale: 60%
    :caption: Running inference

    skinparam monochrome true
    skinparam handwritten false
    hide footbox
    autoactivate on

    user -> Network : load(model)
    return true
    loop
        user -> Network : input[0].assign(data)
        return true
        user -> Network : predict
        return true
        user -> Network : read output[0].data()
    end


.. raw:: latex

    \clearpage


Example:

.. code-block::

    Network net;
    net.load_model("model.synap");
    vector<uint8_t> in_data = custom_read_input_data();
    net.inputs[0].assign(in_data.data(), in_data.size());
    net.predict();
    custom_process_result(net.outputs[0].as_float(), net.outputs[0].item_count());


Please note that:

    - all memory allocations and alignment for the weights and the input/ouput data are done
      automatically by the Network object
    
    - all memory is automatically deallocated when the Network object is destroyed
    
    - for simplicity all error checking has been omitted, methods typically return :code:`false` if
      something goes wrong. No explicit error code is returned since the error can often be too
      complex to be explained with a simple enum code and normally there is not much the caller code
      can do do to recover the situation. More detailed information on what went wrong can be found
      in the logs.

    - the routines named *custom...* are just placeholders for user code in the example.

    - In the code above there is a data copy when assigning the :code:`in_data` vector to the tensor.
      The data contained in the :code:`in_data` vector can't be used directly for inference because
      there is no guarantee that they are correcly aligned and padded as required by the HW.
      In most cases the cost of this extra copy is negligible, when this is not the case the copy
      can sometimes be avoided by writing directly inside the tensor data buffer, something like::
    
        custom_generate_input_data(net.inputs[0].data(), net.inputs[0].size());
        net.predict();

      For more details see section :ref:`access_tensor_data`
    
    - the type of the data in a tensor depends on how the network has been generated, common data types
      are `float16`, `float32` and quantized `uint8` and `int16`.
      The ``assign()`` and ``as_float()`` methods take care of all the required data conversions. 


By using just the simple methods shown in this section it is possible to perform inference with 
the NPU hardware accelerator. This is almost all that one needs to know in order to use SyNAP
in most applications. The following sections explain more details of what's going on behind the scenes:
this allows to take full advantage of the available HW for more demanding use-cases.


Advanced Topics
---------------

Tensors
~~~~~~~

We've seen in the previous section that all accesses to the network input and output data are done
via tensor objects, so it's worth looking in detail at what a :code:`Tensor` object can do.
Basically a tensor allows to:

    - get information and attributes about the contained data
    
    - access data
    
    - access the underlying :code:`Buffer` used to contain data. More on this in the next section.

Let's see a detailed description of the class and the available methods.

.. uml::
    :scale: 65%
    :caption: Tensor class
    
    skinparam monochrome true
    skinparam handwritten false
    class Tensor {
        string name()
        Shape shape() 
        Layout layout()
        SynapType data_type()
        size_t size()
        size_t item_count()
        ..
        bool assign(data_ptr, data_size)
        void* data()
        float* as_float()
        ..
        Buffer* buffer()
        bool set_buffer(Buffer* buffer)
    }


.. doxygenclass:: synaptics::synap::Tensor
    :members:

Here below a list of all the data types supported in a tensor:

.. doxygenenum:: synaptics::synap::DataType
   :outline:


Buffers
~~~~~~~

The memory used to store a tensor data has to satisfy the following requirements:

    - must be correctly aligned
    
    - must be correctly padded
    
    - in some cases must be contiguous
    
    - must be accessible by the NPU HW accelerator and by the CPU or other HW components 
    

Memory allocated with :code:`malloc()` or :code:`new` or :code:`std::vector` doesn't satisfy these
requirements so can't be used directly as input or output of a Network.
For this reason :code:`Tensor` objects use a special :code:`Buffer` class to handle memory. Each
tensor internally contains a default Buffer object to handle the memory used for the data.

The API provided by the :code:`Buffer` is similar when possible to the one provided by
:code:`std::vector`. The main notable exeception is that a buffer content can't be indexed
since a buffer is just a container for raw memory, without a *data type*.
The data type is known by the tensor which is using the buffer. 
:code:`Buffer` is also taking care of disposing the allocated memory when it is destroyed (*RAII*)
to avoid all possible memory leakages. The actual memory allocation is done via an additional
:code:`Allocator` object. This allows to allocate memory with different attributes in different
memory area. When a buffer object is created it will use the default allocator unless a different
allocator is specified. The allocator can be specified directly in the constructor or later using the
:code:`set_allocator()` method.

.. uml::
    :scale: 65%
    :caption: Buffer class
    
    skinparam monochrome true
    skinparam handwritten false
    class Buffer {
        Buffer(size, allocator)
        ..
        bool resize(size)
        size_t size()
        ..
        bool assign(data_ptr, data_size)
        void* data()
        ..
        bool set_allocator(allocator)
        bool allow_cpu_access(allow)
    }


In order for the buffer data to be shared by the CPU and NPU hardware some extra operations have
to be done to ensure that the CPU caches and system memory are correcly aligned. All this
is done automatically when the buffer content is used in the Network for inference.
There are cases when the CPU is not going to read/write the buffer data directly,
for example when the data is generated by another HW component (eg. video decoder).
In these cases it's possible to have some performance improvements by disabling CPU access to the
buffer using the method provided.

.. note::

    it is also possible to create a buffer that refers to an existing memory area instead of using
    an allocator. In this case the memory area must have been registered with the TrustZone kernel
    and must be correctly aligned and padded. Furthermore the Buffer object will *not* free the
    memory area when it is destroyed, since the memory is supposed to be owned
    by the SW module which allocated it.

.. doxygenclass:: synaptics::synap::Buffer
    :members:


Allocators
~~~~~~~~~~

Two allocators are provided for use with buffer objects:

    - the *standard* allocator: this is the default allocator used by buffers created without
      explicitly specifying an allocator. The memory is paged (non-contiguous).

    - the *cma* allocator: allocates contiguous memory. Contiguous memory is required for some HW
      components and can provide some small performance improvement if the input/output buffers are very large
      since less overhead is required to handle memory pages.
      Should be used with great care since the contiguous memory available in the system is quite limited.


.. cpp:function:: Allocator* std_allocator()

    return a pointer to the system standard allocator.

.. cpp:function:: Allocator* cma_allocator()

    return a pointer to the system contiguous allocator.


.. important::

    The calls above return pointers to global objects,
    so they *must NOT be deleted* after use


.. raw:: latex

    \clearpage


Advanced Examples
-----------------

.. _access_tensor_data:

Accessing Tensor Data
~~~~~~~~~~~~~~~~~~~~~

Data in a Tensor is normally written using the ``Tensor::assign(const T* data, size_t count)`` method.
This method will take care of any required data normalization and data type conversion from
the type ``T`` to the internal representation used by the network.

Similarly the output data are normally read using the ``Tensor::as_float()`` method that
provides a pointer to the tensor data converted to floating point values from whatever internal
represention is used.

These conversions, even if quite optimized, present however a runtime cost that is proportional to
the size of the data. For input data this cost could be avoided by generating them directly in
the Tensor data buffer, but this is only possible when the tensor data type corresponds to
that of the data available in input and no additional normalization/quantization is required.
Tensor provides a type-safe ``data<T>()`` access method that will return a pointer to the data in the
tensor only if the above conditions are satisfied, for example:

.. code-block::

    uint8_t* data_ptr = net.inputs[0].data<uint8_t>();
    if (data_ptr) {
       custom_generate_data(data_ptr, net.inputs[0].item_count());
    }

If the data in the tensor is not ``uint8_t`` or normalization/[de]quantization is required, the returned
value will be ``nullptr``. In this case the direct write or read is not possible and ``assign()``
or ``as_float()`` is required.

It's always possible to access the data directly by using the raw ``data()`` access method which
bypasses all checks:

.. code-block::

    void* in_data_ptr = net.inputs[0].data();
    void* out_data_ptr = net.outputs[0].data();

In the same way it's also possible to assign raw data (without any conversion)
by using ``void*`` data pointer:

.. code-block::

    const void* in_raw_data_ptr = ....;
    net.inputs[0].assign(in_raw_data_ptr, size);

In these cases it's responsibility of the user to know how the data are represented and how to
handle them.


Setting Buffers
~~~~~~~~~~~~~~~

If the properties of the default tensor buffer are not suitable, the user can explicity create
a new buffer and use it instead of the default one. For example suppose we want to use a buffer
with contiguous memory:

.. code-block::

    Network net;
    net.load_model("model.synap");
    
    // Replace the default buffer with one using contiguous memory
    Buffer cma_buffer(net.inputs[0].size(), cma_allocator());
    net.inputs[0].set_buffer(&cma_buffer);

    // Do inference as usual
    custom_generate_input_data(net.inputs[0].data(), net.inputs[0].size());
    net.predict();


Settings Default Buffer Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simpler alternative to replacing the buffer used in a tensor as seen in the previous section
is to directly change the properties of the default tensor buffer.
This can only be done at the beginning, before the tensor data is accessed:

.. code-block::

    Network net;
    net.load_model("model.synap");
    
    // Use contiguous allocator for default buffer in input[0]
    net.inputs[0].buffer()->set_allocator(cma_allocator());

    // Do inference as usual
    custom_generate_input_data(net.inputs[0].data(), net.inputs[0].size());
    net.predict();


.. _buffer_sharing:

Buffer Sharing
~~~~~~~~~~~~~~

The same buffer can be shared among multiple networks if they need to process the same
input data. This avoids the need of redundant data copies:

.. code-block::

    Network net1;
    net1.load_model("nbg1.synap");
    Network net2;
    net2.load_model("nbg2.synap");

    // Use a common input buffer for the two networks (assume same input size)
    Buffer in_buffer;
    net1.inputs[0].set_buffer(&in_buffer);
    net2.inputs[0].set_buffer(&in_buffer);
    
    // Do inference as usual
    custom_generate_input_data(in_buffer.data(), in_buffer.size());
    net1.predict();
    net2.predict();


Another interesting case of buffer sharing is when the output of a network must be processed
directly by another network. For example the first network can do some preprocessing and the second
one the actual inference.
In this case setting the output buffer of the first network as the input buffer of the second
network allows to completely avoid data copying (the two tensors must have the same size of course).
Furthermore, since the CPU has no need to access this intermediate data, it is convenient to
disable its access to this buffer, this will avoid the un-necessary overhead of cache flushing
and provide an additional improvement in performance.

.. code-block::

    Network net1;
    net1.load_model("nbg1.synap");
    Network net2;
    net2.load_model("nbg2.synap");

    // Use net1 output as net2 input. Disable CPU access for better performance.
    net1.outputs[0].buffer()->allow_cpu_access(false);
    net2.inputs[0].set_buffer(net1.outputs[0].buffer()));

    // Do inference as usual
    custom_generate_input_data(net1.inputs[0].data(), net1.inputs[0].size());
    net1.predict();
    net2.predict();


One last case is when the output of the first network is smaller than the input of the second network,
and we still want to avoid copy. Imagine for example that the output of net1 is an image 640x360 that
we want to generate inside the input of net2 which expects an image 640x480.
In this case the buffer sharing technique shown above can't work due to the mismatch in size of the
two tensors. What we need instead is to share part of the memory used by the two Buffers.


.. code-block::

    Network net2;  // Important: this has to be declared first, so it is destroyed after net1
    net2.load_model("nbg2.synap");
    Network net1;
    net1.load_model("nbg1.synap");

    // Initialize the entire destination tensor now that we still have CPU access to it
    memset(net2.inputs[0].data(), 0, net2.inputs[0].size());

    // Replace net1 output buffer with a new one using (part of) the memory of net2 input buffer
    *net1.outputs[0].buffer() = Buffer(*net2.inputs[0].buffer(), 0, net2.outputs[0].size());

    // Disable CPU access for better performance
    net1.outputs[0].buffer()->allow_cpu_access(false);
    net2.inputs[0].buffer()->allow_cpu_access(false);

    // Do inference as usual
    custom_generate_input_data(net1.inputs[0].data(), net1.inputs[0].size());
    net1.predict();
    net2.predict();


.. note::

    Since net1 input tensor now uses the memory allocated by net2, it is important that net1 is destroyed
    before net2, otherwise it will be left pointing to unallocated memory.
    This limitation will be fixed in the next release.


Recycling Buffers
~~~~~~~~~~~~~~~~~

It is possible for the user to explicitly set at any time which buffer to use for each tensor
in a network. The cost of this operation is very low compared to the creation of a new buffer so
it is possible to change the buffer associated to a tensor at each inference if desired.

Despite this, the cost of *creating* a buffer and setting it to a tensor the first time is quite high
since it involves multiple memory allocations and validations. It is possible but deprecated to
create a new :code:`Buffer` at each inference, better to create the required buffers in advance
and then just use :code:`set_buffer()` to choose which one to use.

As an example consider a case where we want to do inference on the current data while at the same time
preparing the next data.
The following code shows how this can be done:

.. code-block::

    Network net;
    net.load_model("model.synap");
 
    // Create two input buffers
    const size_t input_size = net.inputs[0].size();
    vector<Buffer> buffers { Buffer(input_size), Buffer(input_size) };
    
    int current = 0;
    custom_start_generating_input_data(&buffers[current]);
    while(true) {
        custom_wait_for_input_data();

        // Do inference on current data while filling the other buffer
        net.inputs[0].set_buffer(&buffers[current]);
        current = !current;
        custom_start_generating_input_data(&buffers[current]);
        net.predict();
        custom_process_result(net.outputs[0]);
    }


Using BufferCache
~~~~~~~~~~~~~~~~~

There are situations where the data to be processed comes form other components that
provide each time a data block taken from a fixed pool of blocks. Each block can be uniquely identified
by an ID or by an address. This is the case for example of a video pipeline providing frames.
 
Processing in this case should proceed as follows:

    1. Get the next block to be processed
    2. If this is the first time we see this block, create a new :code:`Buffer` for it and add it to a collection
    3. Get the :code:`Buffer` corresponding to this block from the collection
    4. Set is as the current buffer for the input tensor
    5. Do inference and process the result
    
The collection is needed to avoid the expensive operation of creating a new :code:`Buffer` each time.
This is not complicate to code but steps 2 and 3 are always the same.
The :code:`BufferCache` template takes care of all this. The template parameter allows to specify
the type to be used to identify the received block, this can be for example a BlockID or directly
the address of the memory area.

.. note::

    In this case the buffer memory is not allocated by the :code:`Buffer` object.
    The user is responsible for ensuring that all data is properly padded and aligned.
    Futhermore the buffer cache is not taking ownership of the data block, it's responsibility
    of the user to deallocate them in due time after the :code:`BufferCache` has been deleted.


Copying and Moving
~~~~~~~~~~~~~~~~~~

:code:`Network`, :code:`Tensor` and :code:`Buffer` objects internally access to HW resources so
can't be copied. For example:

.. code-block::

    Network net1;
    net1.load_model("model.synap");
    Network net2;
    net2 = net1;  // ERROR, copying networks is not allowed

However :code:`Network` and :code:`Buffer` objects can be moved since this has no overhead and
can be convenient when the point of creation is not the point of use. Example:

.. code-block::

    Network my_create_network(string nb_name, string meta_name) {
        Network net;
        net.load(nb_name, meta_name);
        return net;
    }
    
    void main() {
        Network network = my_create_network("model.synap");
        ...
    }

The same functionality is not available for :code:`Tensor` objects, they can exist only inside
their own Network.


NPU Locking
-----------

An application can decide to reserve the NPU for its exclusive usage. This can be useful
in case of realtime applications that have strict requirements in terms of latency, for example
video or audio stream processing.

Locking the NPU can be done at two levels:

    1. reserve NPU access to the current process using :code:`Npu::lock()`
    2. reserve NPU for *offline use only* (that is disable NPU access from NNAPI)


NPU Locking
~~~~~~~~~~~

The NPU locking is done **by process**, this means that once the :code:`Npu::lock()` API
is called no other process will be able to run inference on the NPU.
Other processes will still be able to load networks, but if they try to do offline or online 
NNAPI inference or to :code:`lock()` the NPU again, they will fail.

The process which has locked the NPU is the only one which has the righs to unlock it. If a process 
with a different PID tries to unlock() the NPU, the operation will be ignored and have no effect.


.. note::

    There is currently no way for a process to test if the NPU has been locked by some other
    process. The only possibility is to try to lock() the NPU, if this operation fails it means
    that the NPU is already locked by another process or unavailable due to some failure.

.. note::

    If the process owning the NPU lock terminates or is terminated for any reason, the lock is 
    automatically released.


NNAPI Locking
~~~~~~~~~~~~~

A process can reserve the NPU for offline use only so that nobody will be able to run *online*
inference on the NPU via NNAPI.
Other processes will still be able to run *offline* inference on the NPU.
SyNAP has no dedicated API for this, NNAPI can be disabled by setting the property ``vendor.NNAPI_SYNAP_DISABLE``
to 1 using the standard Android API ``__system_property_set()`` or ``android::base::SetProperty()``.
Sample code in: https://android.googlesource.com/platform/system/core/+/master/toolbox/setprop.cpp

See also: :ref:`nnapi-locking`

.. note::

    It will still be possible to perform online inference on the NPU using the *timvx* tflite delegate.


Description
~~~~~~~~~~~

The :code:`Npu` class controls the locking and unlocking of the NPU.
Normally only one object of this class needs to be created when the applicaton start and destroyed
when the application is going to terminate.

.. uml::
    :scale: 65%
    :caption: Npu class
    
    skinparam monochrome true
    skinparam handwritten false
    class Npu {
        bool available()
        ..
        bool lock()
        bool unlock()
        bool is_locked()
    }


.. doxygenclass:: synaptics::synap::Npu
    :members:

.. note::

    The :code:`Npu` class uses the *RAII* technique, this means that when an object of this class is
    destroyed and it was locking the NPU, the NPU is automatically unlocked. This helps ensure
    that when a program terminates the NPU is in all cases unlocked.


Sample Usage
~~~~~~~~~~~~

The following diagrams show some example use of the NPU locking API.

.. uml::
    :scale: 60%
    :caption: Locking the NPU

    skinparam monochrome true
    skinparam handwritten false
    hide footbox
    box "Process 1" #WhiteSmoke
    participant main
    participant Npu
    end box
    box "Process 2" #LightGray
    participant "main "
    participant "Npu "
    end box
    
    main -> Npu ++ : lock
    return true
    == NPU locked by Process 1 ==
    "main " -> "Npu " ++ : lock
    return false
    main -> Npu ++ : is_locked
    return true
    "main " -> "Npu " ++ : is_locked
    return false
    main -> Npu ++ : unlock
    return true
    == NPU unlocked ==
    "main " -> "Npu " ++ : lock
    return true
    == NPU locked by Process 2 ==


.. uml::
    :scale: 60%
    :caption: Locking and inference

    skinparam monochrome true
    skinparam handwritten false
    hide footbox
    box "Process 1" #WhiteSmoke
    participant main
    participant Npu
    participant Network
    end box
    box "Process 2" #LightGray
    participant "main "
    participant "Network "
    end box
    box "Process 3" #Silver
    participant " main"
    participant "AndroidNNRuntime"
    end box

    main -> Npu ++ : lock
    return true
    == NPU locked by Process 1 ==
    main -> Network ++ : load
    return true
    main -> Network ++ : predict
    return true
    "main " -> "Network " ++ : load
    return true
    "main " -> "Network " ++ : predict
    note left of "Network " : inference from another process fails
    return false
    " main" -> "AndroidNNRuntime" ++ : ANeuralNetworksExecution_startCompute
    note left of AndroidNNRuntime: inference using NNAPI also fails
    return ANEURALNETWORKS_OP_FAILED
    main -> Npu ++ : unlock
    return true
    == NPU unlocked ==
    "main " -> "Network " ++ : predict
    return true


.. uml::
    :scale: 60%
    :caption: Locking NNAPI

    skinparam monochrome true
    skinparam handwritten false
    hide footbox
    box "Process 1" #WhiteSmoke
    participant main
    participant Android
    participant Network
    end box
    box "Process 2" #LightGray
    participant "main "
    participant "Network "
    end box
    box "Process 3" #Silver
    participant " main"
    participant "AndroidNNRuntime"
    end box
    
    main -> Android ++ : setprop vendor.NNAPI_SYNAP_DISABLE 1
    return true
    == NNAPI locked by Process 1 ==
    main -> Network ++ : load
    return true
    main -> Network ++ : predict
    return true
    "main " -> "Network " ++ : load
    return true
    "main " -> "Network " ++ : predict
    note left of "Network " : inference from another process still allowed
    return true
    " main" -> "AndroidNNRuntime" ++ : ANeuralNetworksExecution_startCompute
    note left of AndroidNNRuntime: inference using NNAPI fails
    return ANEURALNETWORKS_OP_FAILED
    main -> Android ++ : setprop vendor.NNAPI_SYNAP_DISABLE 0
    return true
    == NNAPI unlocked ==
    "main " -> "Network " ++ : predict
    return true



.. uml::
    :scale: 60%
    :caption: Automatic lock release

    skinparam monochrome true
    skinparam handwritten false
    hide footbox
    box "Process 1" #WhiteSmoke
    participant main
    participant Npu
    end box
    box "Process 2" #LightGray
    participant "main "
    participant "Network "
    end box
    box "Process 3" #Silver
    participant " main"
    participant "AndroidNNRuntime"
    end box
    
    main -> Npu ** : new
    "main " -> "Network " ++ : predict
    return true
    main -> Npu ++ : lock
    return true
    == NPU locked by Process 1 ==
    "main " -> "Network " ++ : predict
    return false
    " main" -> "AndroidNNRuntime" ++ : ANeuralNetworksExecution_startCompute
    return ANEURALNETWORKS_OP_FAILED
    main -> Npu !! : delete
    == NPU unlocked ==
    main -> main !! : exit
    "main " -> "Network " ++ : predict
    return true
    " main" -> "AndroidNNRuntime" ++ : ANeuralNetworksExecution_startCompute
    return ANEURALNETWORKS_NO_ERROR

.. raw:: latex

    \clearpage


Preprocessing and Postprocessing
--------------------------------

When using neural networks the input and output data are rarely used in their raw format.
Most often data conversion has to be performed on the input data in order make them match
the format expected by the network, this step is called *preprocessing*.

Example of preprocessing in the case of an image are:

- scale and/or crop the input image the the size expected by the network
- convert planar to interleaved or vice-versa
- convert RGB to BGR or vicerversa
- apply mean and scale normalization

These operations can be performed using the NPU at inference time by enabling preprocessing when
the model is converted using the SyNAP Toolkit, or they can be performed in SW when the data
is assigned to the Network.

Similarly the inference results contained in the network output tensor(s) normally
require further processing to make the result usable. This step is called *postprocessing*.
In some cases postprocessing can be a non-trivial step both in complexity and computation time.

Example of post-processing are:

- convert quantized data to floating point representation
- analyze the network output to extract the most significant elements
- combine the data from multiple output tensor to obtain a meaningful result

The classes in this section are not part of the SyNAP API, they are intented mainly as utility
classes that can help writing SyNAP applications by combining the three usual steps of 
preprocess-inference-postprocess just explained.

Full source code is provided, so they can be used as a reference implementation for the user to extend.

.. _InputData-class:


InputData Class
~~~~~~~~~~~~~~~

The main role of the ``InputData`` class is to wrap the actual input data and complement it with additional
information to specify what the data represents and how it is organized.
The current implementation is mainly focused on image data.

``InputData`` functionality includes:

- reading raw files (binary)
- reading and parsing images (jpeg or png) from file or memory
- getting image attributes, e.g. dimensions and layout.

The input filename is specified directly in the constructor and can't be changed.
In alternative to a filename it is also possible to specify a memory address in case the content
is already available in memory.

.. note::
    No data conversion is performed, even for jpeg or png images the data is kept in its original form.


.. uml::
    :scale: 65%
    :caption: InputData class
    
    skinparam monochrome true
    skinparam handwritten false
    class InputData {
        InputData(filename)
        InputData(buffer, size, type, shape, layout)
        ..
        bool empty()
        void* data()
        size_t size()
        InputType type()
        Layout layout()
        Shape shape()
        Dimensions dimensions()
    }


Example:

.. code-block::

    Network net;
    net.load_model("model.synap");
    InputData image("sample_rgb_image.dat");
    net.inputs[0].assign(image.data(), image.size());
    net.predict();
    custom_process_result(net.outputs[0]);


Preprocessor Class
~~~~~~~~~~~~~~~~~~

This class takes in input an ``InputData`` object and assigns its content to the input Tensor(s)
of a network by performing all the necessary conversions.
The conversion(s) required are determined automatically by reading the attributes of the tensor itself.

Supported conversions include:

- image decoding (jpeg, png or nv21 to rgb)
- layout conversion: *nchw* to *nhwc* or vice-versa
- format conversion: *rgb* to *bgr* or *grayscale*
- image cropping (if preprocessing with cropping enabled in the compiled model)
- image rescaling to fit the tensor dimensions


The conversion (if needed) is performed when an ``InputData`` object is assigned to a ``Tensor``.

Cropping is only performed if enabled in the compiled model and the multi-tensor assign API is used:
``Preprocessor::assign(Tensors& ts, const InputData& data)``.

Rescaling by default preserves the aspect ratio of the input image.
If the destination tensor is taller than the rescaled input image, gray bands are added at the top
and bottom.
If the destination tensor is wider than then the rescaled input image, gray bands are added at the
left and right. It is possible to configure the gray level of the fill using the ``fill_color=N`` option
in the format string of the input tensor, where `N` is an integer between 0 (black) and 255 (white).

The preservation of the aspect-ratio can be disabled by specifying the ``keep_proportions=0`` option
in the format string of the input tensor. In this case the input image is simply resized to match
the size of the tensor.

.. note::

    The ``Preprocessor``  class performs preprocessing using the CPU. If the conversion to be done
    is known in advance it may be convenient to perform it using the NPU by adding
    a preprocessing layer when the network is converted, see :ref:`Preprocessing`


ImagePostprocessor Class
~~~~~~~~~~~~~~~~~~~~~~~~

``ImagePostprocessor`` functionality includes:

- reading the content of a set of Tensors
- converting the raw content of the Tensors to a standard representation (currently only ``nv21`` is supported)
  The format of the raw content is determined automatically by reading
  the attributes of the tensors themselves. For example in some super-resolution network, the different
  component of the output image (*y*, *uv*) are provided in separate outputs.
  The converted data is made available in a standard vector.

.. uml::
    :scale: 65%
    :caption: ImagePostprocessor class
    
    skinparam monochrome true
    skinparam handwritten false
    class ImagePostprocessor {
        ImagePostprocessor()
        ..
        Result process(tensors)
    }


Example:

.. code-block::

    Preprocessor preprocessor
    Network net;
    ImagePostprocessor postprocessor;

    net.load_model("model.synap");
    InputData image("sample_image.jpg");
    preprocessor.assign(net.inputs[0], image);
    net.predict();
    // Convert to nv21
    ImagePostprocessor::Result out_image = postprocessor.process(net.outputs);
    binary_file_write("out_file.nv21", out_image.data.data(), out_image.data.size());


Classifier Class
~~~~~~~~~~~~~~~~

The :code:`Classifier` class is a postprocessor for the common use case of image 
classification networks.

There are just two things that can be done with a classifier:

    - initialize it
    
    - process network outputs: this will return a list of possible classifications sorted in order
      of decreasing confidence, each containing the following information:

      - class_index
      - confidence


.. uml::
    :scale: 65%
    :caption: Classifier class
    
    skinparam monochrome true
    skinparam handwritten false
    class Classifier {
        Classifier(top_count)
        Result process(tensors)
    }

.. doxygenclass:: synaptics::synap::Classifier
    :members:

Example:

.. code-block::

    Preprocessor preprocessor
    Network net;
    Classifier classifier(5);
    net.load_model("model.synap");
    InputData image("sample_image.jpg");
    preprocessor.assign(net.inputs[0], image);
    net.predict();
    Classifier::Result top5 = classifier.process(net.outputs);


The standard content of the output tensor of a classification network is a list of probabilities,
one for each class on which the model has been trained (possibly including an initial element to
indicate a "background" or "unrecognized" class). In some cases the final *SoftMax* layer of the
model is cut away to improve inference time: in this case the output values can't be interpreted
as probabilities anymore but since *SoftMax* is monotonic this doesn't change the result of the
classification.
The postprocessing can be parametrized using the *format* field of the corresponding
output in the conversion metafile (see :ref:`conversion-metafile`):

+------------------------------+------+-------------+----------------------------------------+
| Format Type                  | Out# | Shape       | Description                            |
+==============================+======+=============+========================================+
| confidence_array             | 0    | NxC         | List of probabilities, one per class   |
+------------------------------+------+-------------+----------------------------------------+

+------------------------------+---------+---------------------------------------------------------------------+
| Attribute                    | Default | Description                                                         |
+==============================+=========+=====================================================================+
| class_index_base             | 0       | Class index corresponding to the first element of the output vector |
+------------------------------+---------+---------------------------------------------------------------------+

Where:

    - N: Number of samples, must be 1
    - C: number of recognized classes

.. raw:: latex

    \clearpage


Detector Class
~~~~~~~~~~~~~~

The :code:`Detector` class is a postprocessor for the common use case of object detection networks.
Here *object* is a generic term that can refer to actual objects or people or anything used to 
train the network.

There are just two things that can be done with a detector:

    - initialize it
    
    - run a detection: this will return a list of detection items, each containing
      the following information:

      - class_index
      - confidence
      - bounding box
      - landmarks (optional)


.. uml::
    :scale: 65%
    :caption: Detector class
    
    skinparam monochrome true
    skinparam handwritten false
    class Detector {
        Detector(threshold, n_max, nms, iou_threshold, iou_with_min)
        Result process(tensors, input_rect)
    }

.. doxygenclass:: synaptics::synap::Detector
    :members:


Example::

    Preprocessor preprocessor
    Network net;
    Detector detector;
    net.load_model("model.synap");
    InputData image("sample_image.jpg");
    Rect image_rect;
    preprocessor.assign(net.inputs[0], image, &image_rect);
    net.predict();
    Detector::Result objects = detector.process(net.outputs, image_rect);


The rectangle argument passed to the ``process()`` method is needed so that is can compute
bounding boxes and landmarks in coordinates relative to the original image, even if the image
has been resized and/or cropped during the assignment to the network input tensor.

Postprocessing consist of the following steps:

    - for each possible position in the input grid compute the score of the highest class there
    - if this score is too low nothing is detected at that position
    - if above the detection threshold then there is something there, so compute the actual bounding
      box of the object by combining information about the anchors location, the regressed deltas
      from the network and the actual size of the input image
    - once all the detections have been computed, filter them using Non-Min-Suppression algorithm
      to discard spurious overlapping detections and keep only the one with highest score at each position.
      The NMS filter applies only for bounding boxes which have an overlap above a minimum threshold.
      The overlap itself is computed using the *IntersectionOverUnion* formula
      (ref: https://medium.com/analytics-vidhya/iou-intersection-over-union-705a39e7acef).
      In order to provide more filtering for boxes of different sizes, the "intersection" area
      is sometimes replaced by the "minimum" area in the computation. SyNAP Detector implements both formula.

The content of the output tensor(s) from an object detection network is not standardized.
Several formats exist for the major families of detection networks, with variants inside each family.
The information contained is basically always the same, what changes is the way they are organized.
The ``Detector`` class currently supports the following output formats:

    - ``retinanet_boxes``
    - ``tflite_detection_input``
    - ``tflite_detection``
    - ``yolov5``
    - ``yolov8``

The desired label from the above list has to be put in the "format" field of the first output tensor of the
network in the conversion metafile (see :ref:`conversion-metafile`) so the ``Detector`` knows how to interpret the output.

``retinanet_boxes`` is the output format used by Synaptics sample detection networks
(mobilenet224_full80 for COCO detection and mobilenet224_full1 for people detection).

``tflite_detection_input`` is the format of the input tensors of the ``TFLite_Detection_PostProcess``
layer, used for example in the  `ssd_mobilenet_v1_1_default_1.tflite` object-detection model:

       https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/default/1

This format is used when the ``TFLite_Detection_PostProcess`` layer is removed from the network at
conversion time and the corresponding postprocessing algorithm is performed in software.

In both cases above the model has two output tensors: the first one is a regression tensor, and contains
the bounding box deltas for the highest-score detected object in each position of the input grid. The second one
is the classification tensor and for each class contains the score of that class, that is the confidence
that this class is contained in the corresponding position of the input grid.

``tflite_detection`` is the format of the *output* tensors of the ``TFLite_Detection_PostProcess``
layer, used for example in the  `ssd_mobilenet_v1_1_default_1.tflite` object-detection model.

``yolov5`` is the output format used by models derived from the well-kown *yolov5* arcitecture.
In this case the model has a single output 3D tensor organized as a list of detections, where each
detection contains the following fields:

    - bounding box deltas (x, y, w, h)
    - overall confidence for this detection
    - landmarks deltas (x, y) if supported by the model
    - confidence vector, one entry per class

``yolov8`` is the output format used by models derived from the *yolov8* arcitecture, the most recent
update to the *yolo* family. The organization of the output tensor is very similar to that for
yolov5 here above, the only difference is that the *overall confidence* field is missing.

In some cases the final layers in the model can be executed more efficiently in the CPU, so they are
cut away when the model is generated or compiled with the SyNAP Toolkit. In this case the network
will have one output tensor for each item of the image pyramid (normally 3) and each output will
be a 4D or 5D tensor, whose layout depends on where exacly the model has been cut.

SyNAP Detector is able to automatically deduce the layout used, it just requires an indication 
if the information in the tensor are transposed.


+------------------------------+------+-------------+-----------------------------------+-----------------------------+
| Format Type                  | Out# | Shape       | Description                       | Notes                       |
+==============================+======+=============+===================================+=============================+
| retinanet_boxes              | 0    | Nx4         | bounding box deltas               |                             |
|                              +------+-------------+-----------------------------------+-----------------------------+
|                              | 1    | NxC         | Per-class probability             |                             |
+------------------------------+------+-------------+-----------------------------------+-----------------------------+
| tflite_detection_input       | 0    | Nx4         | bounding box deltas               |                             |
|                              +------+-------------+-----------------------------------+-----------------------------+
| tflite_detection_boxes       | 1    | NxC         | Per-class probability             |                             |
+------------------------------+------+-------------+-----------------------------------+-----------------------------+
| tflite_detection             | 0    | NxMx4       | Bounding boxes                    |                             |
|                              +------+-------------+-----------------------------------+-----------------------------+
|                              | 1    | NxM         | Index of detected class           |                             |
|                              +------+-------------+-----------------------------------+-----------------------------+
|                              | 2    | NxM         | Score of detected class           |                             |
|                              +------+-------------+-----------------------------------+-----------------------------+
|                              | 3    | 1           | Actual number of detections       |                             |
+------------------------------+------+-------------+-----------------------------------+-----------------------------+
| yolov5                       |0..P-1| NxTxD       | Processing done in the model      |                             |
|                              |      +-------------+-----------------------------------+-----------------------------+
|                              |      | NxHxWxAxD   | One 5D tensor per pyramid element |                             |
|                              |      +-------------+-----------------------------------+-----------------------------+
|                              |      | NxHxWx(A*D) | One 4D tensor per pyramid element |                             |
|                              |      +-------------+-----------------------------------+-----------------------------+
|                              |      | NxAxHxWxD   | One 5D tensor per pyramid element |                             |
|                              |      +-------------+-----------------------------------+-----------------------------+
|                              |      | NxAxDxHxW   | One 5D tensor per pyramid element | Requires "``transposed=1``" |
|                              |      +-------------+-----------------------------------+-----------------------------+
|                              |      | Nx(A*D)xHxW | One 4D tensor per pyramid element | Requires "``transposed=1``" |
+------------------------------+------+-------------+-----------------------------------+-----------------------------+
| yolov8                       | 0    | NxTxD       | Processing done in the model      | Overall confidence missing  |
+------------------------------+------+-------------+-----------------------------------+-----------------------------+


Where:

    - N: number of samples, must be 1
    - C: number of classes detected
    - T: total number of detections
    - M: maximum number of detections
    - D: detection size (includes: bounding box deltas xywh, confidence, landmarks, per-class confidences)
    - A: number of anchors
    - H: heigth of the image in the pyramid
    - W: width of the image in the pyramid
    - P: number of images in the pyramid


Attributes for ``retinanet_boxes`` and ``tflite_detection_input`` formats:

+------------------------------+---------+-------------------------------------------------------------------------------+
| Attribute                    | Default | Description                                                                   |
+==============================+=========+===============================================================================+
| class_index_base             | 0       | Class index corresponding to the first element of the output vector           |
+------------------------------+---------+-------------------------------------------------------------------------------+
| transposed                   | 0       | Must be 1 if the output tensor uses the transposed format                     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| anchors                      |         | Anchor points                                                                 |
+------------------------------+---------+-------------------------------------------------------------------------------+
| x_scale                      | 10      | See ``x_scale`` parameter in the ``TFLite_Detection_PostProcess`` layer       |
+------------------------------+---------+-------------------------------------------------------------------------------+
| y_scale                      | 10      | See ``y_scale`` parameter in the ``TFLite_Detection_PostProcess`` layer       |
+------------------------------+---------+-------------------------------------------------------------------------------+
| h_scale                      | 5       | See ``h_scale`` parameter in the ``TFLite_Detection_PostProcess`` layer       |
+------------------------------+---------+-------------------------------------------------------------------------------+
| w_scale                      | 5       | See ``w_scale`` parameter in the ``TFLite_Detection_PostProcess`` layer       |
+------------------------------+---------+-------------------------------------------------------------------------------+

In this case, the anchor points can be defined using the build-in
variable ``${ANCHORS}``:

.. code-block:: none

    anchors=${ANCHORS}

This variable is replaced at conversion time with the content of the ``anchor`` tensor
from the ``TFLite_Detection_PostProcess`` layer (if present in the model).

Attributes for ``tflite_detection`` format:

+------------------------------+---------+-------------------------------------------------------------------------------+
| Attribute                    | Default | Description                                                                   |
+==============================+=========+===============================================================================+
| class_index_base             | 0       | Class index corresponding to the first element of the output vector           |
+------------------------------+---------+-------------------------------------------------------------------------------+
| h_scale                      | 0       | Vertical scale of the detected boxes (normally the H of the input tensor)     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| w_scale                      | 0       | Horizontal scale of the detected boxes (normally the W of the input tensor)   |
+------------------------------+---------+-------------------------------------------------------------------------------+


Attributes for ``yolov5`` and ``yolov8`` formats:

+------------------------------+---------+-------------------------------------------------------------------------------+
| Attribute                    | Default | Description                                                                   |
+==============================+=========+===============================================================================+
| class_index_base             | 0       | Class index corresponding to the first element of the output vector           |
+------------------------------+---------+-------------------------------------------------------------------------------+
| transposed                   | 0       | Must be 1 if the output tensor uses the transposed format                     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| landmarks                    | 0       | Number of landmark points                                                     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| anchors                      |         | Anchor points. Not needed if processing done in the model                     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| h_scale                      | 0       | Vertical scale of the detected boxes                                          |
|                              |         +-------------------------------------------------------------------------------+
|                              |         | (normally the H of the input tensor when processing is done in the model)     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| w_scale                      | 0       | Horizontal scale of the detected boxes                                        |
|                              |         +-------------------------------------------------------------------------------+
|                              |         | (normally the W of the input tensor when processing is done in the model)     |
+------------------------------+---------+-------------------------------------------------------------------------------+
| bb_normalized                | 0       | Must be 1 if the bounding box deltas are normalized (only for `yolov8``)      |
|                              |         +-------------------------------------------------------------------------------+
|                              |         | Indicates that bounding boxes are normalized to the range [0, 1]              |
|                              |         +-------------------------------------------------------------------------------+
|                              |         | while landmarks are in the range h_scale, wscale                              |
+------------------------------+---------+-------------------------------------------------------------------------------+


For ``yolov5`` format, the ``anchors`` attribute  must contain one entry for each pyramid element
from P0, where each entry is a list of the ``x,y`` anchor  deltas.
For example for yolov5s-face, the anchors are defined in
https://github.com/deepcam-cn/yolov5-face/blob/master/models/yolov5s.yaml :

.. code-block:: none

    - [4,5,  8,10,  13,16]  # P3/8
    - [23,29,  43,55,  73,105]  # P4/16
    - [146,217,  231,300,  335,433]  # P5/32

The corresponding outputs in the metafile can be defined as follows:

.. code-block:: none

    outputs:
      - format: yolov5 landmarks=5 anchors=[[],[],[],[4,5,8,10,13,16],[23,29,43,55,73,105],[146,217,231,300,335,433]]
        dequantize: true
      - dequantize: true
      - dequantize: true



Building Sample Code
--------------------

The source code of the sample applications (e.g. ``synap_cli``, ``synap_cli_ic``, etc) is included
in the SyNAP release, together with that of the SyNAP libraries. Users based on the *ASTRA* distribution
can build SyNAP using the provided Yocto recipe.

For other users building SyNAP code requires the following components installed: 

1. VSSDK tree
2. cmake


Build steps:

.. code-block:: none

    cd synap/src
    mkdir build
    cd build
    cmake -DVSSDK_DIR=/path/to/vssdk-directory -DCMAKE_INSTALL_PREFIX=install ..
    make install


The above steps will create the binaries for the sample applications in
``synap/src/build/install/bin``. The binaries can then be pushed to the board
using ``adb``:

.. code-block:: none

    cd synap/src/build/install/bin
    adb push synap_cli_ic /vendor/bin


Users are free to change the source code provided to adapt it to their specific requirements.

