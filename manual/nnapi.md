# JIT Compilation

## Introduction

Just-in-time compilation enables the execution of TensorFlow Lite models directly. For applications that require portability (e.g., must be able to run on an Astra embedded board or an Android phone), the JIT compilation approach offers flexibility at the cost of performance.

For embedded applications, it is recommended you use ahead-of-time compilation instead.

:::note 
JIT compilation is flexible, but initialization time can take a few seconds, and additional optimization and secure media paths are not available.
:::

## Online Inference with NNAPI

![JIT Optimization and execution](images/online_conversion.png)

When a model is loaded and executed via NNAPI, it is automatically converted to the internal representation suitable for execution on the NPU. This conversion doesn't take place when the model is loaded but when the first inference is executed. This is because the size of the input(s) is needed to perform the conversion, and with some models, this information is available only at inference time. If the input size is specified in the model, then the provided input(s) must match this size. In any case, it is not possible to change the size of the input(s) after the first inference.

The model compilation has been heavily optimized, but even so, it can take several milliseconds up to a few seconds for typical models, so it is suggested to execute an inference once just after the model has been loaded and prepared. One of the techniques used to speed up model compilation is caching. Some results of the computations performed to compile a model are cached in a file so that they don't have to be executed again the next time the same model is compiled.

On Android, the cache file is saved by default to `/data/vendor/synap/nnhal.cache` and will contain up to 10,000 entries, which corresponds to a good setting for NNAPI utilization on an average system. The cache path and size can be changed by setting the properties `vendor.SYNAP_CACHE_PATH` and `vendor.SYNAP_CACHE_CAPACITY`. Setting the capacity to 0 will disable the cache. An additional possibility to speed up model compilation is to use the NNAPI cache, see [NNAPI Compilation Caching](/docs/synap/nnapi#nnapi-compilation-caching).

On Yocto Linux, there is no NNAPI cache, but we still have smaller per-process cache files named `synap-cache.[PROGRAM-NAME](PROGRAM-NAME)` in the `/tmp/` directory.

## Benchmarking Models with NNAPI

It is possible to benchmark the execution of a model with online conversion using the standard Android NNAPI tool `android_arm_benchmark_model` from [TensorFlow Performance Measurement](https://www.tensorflow.org/lite/performance/measurement).

A custom version of this tool optimized for SyNAP platforms called `benchmark_model` is already preinstalled on the board in `/vendor/bin`.

Benchmarking a model is quite simple:

1. Download the tflite model to be benchmarked, for example:
    ```
    https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_0.25_224_quant.tgz
    ```
2. Copy the model to the board, for example in the `/data/local/tmp` directory:
    ```
    $ adb push mobilenet_v1_0.25_224_quant.tflite /data/local/tmp
    ```
3. Benchmark the model execution on the NPU with NNAPI (android only):
    ```
    $ adb shell benchmark_model --graph=/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite --use_nnapi=true --nnapi_accelerator_name=synap-npu

    INFO: STARTING!
    INFO: Tensorflow Version : 2.15.0
    INFO: Log parameter values verbosely: [0]
    INFO: Graph: [/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite]
    INFO: Use NNAPI: [1]
    INFO: NNAPI accelerator name: [synap-npu]
    INFO: NNAPI accelerators available: [synap-npu,nnapi-reference]
    INFO: Loaded model /data/local/tmp/mobilenet_v1_0.25_224_quant.tflite
    INFO: Initialized TensorFlow Lite runtime.
    INFO: Created TensorFlow Lite delegate for NNAPI.
    INFO: NNAPI delegate created.
    WARNING: NNAPI SL driver did not implement SL_ANeuralNetworksDiagnostic_registerCallbacks!
    VERBOSE: Replacing 31 out of 31 node(s) with delegate (TfLiteNnapiDelegate) node, yielding 1 partitions for the whole graph.
    INFO: Explicitly applied NNAPI delegate, and the model graph will be completely executed by the delegate.
    INFO: The input model file size (MB): 0.497264
    INFO: Initialized session in 66.002ms.
    INFO: Running benchmark for at least 1 iterations and at least 0.5 seconds but terminate if exceeding 150 seconds.
    INFO: count=1 curr=637079

    INFO: Running benchmark for at least 50 iterations and at least 1 seconds but terminate if exceeding 150 seconds.
    INFO: count=520 first=2531 curr=2793 min=1171 max=9925 avg=1885.74 std=870

    INFO: Inference timings in us: Init: 66002, First inference: 637079, Warmup (avg): 637079, Inference (avg): 1885.74
    INFO: Note: as the benchmark tool itself affects memory footprint, the following is only APPROXIMATE to the actual memory footprint of the model at runtime. Take the information at your discretion.
    INFO: Memory footprint delta from the start of the tool (MB): init=7.40234 overall=7.83203
    ```

:::important

NNAPI is the standard way to perform online inference on the NPU in Android, but it isn't the most efficient or the most flexible one. The suggested way to perform online inference on Synaptics platforms is via the `timvx` delegate. For more information see section [Benchmarking Models with TimVx Delegate](/docs/synap/nnapi#benchmarking-models-with-timvx-delegate).

:::

If for any reason some of the layers in the model cannot be executed on the NPU, they will automatically fall back to CPU execution. This can occur, for example, in case of specific layer types, options, or data types not supported by NNAPI or SyNAP. In this case, the network graph will be partitioned into multiple delegate kernels as indicated in the output messages from `benchmark_model`, for example:
```
$ adb shell benchmark_model ...
...
INFO: Initialized TensorFlow Lite runtime.
INFO: Created TensorFlow Lite delegate for NNAPI.
Explicitly applied NNAPI delegate, and the model graph will be partially executed by the delegate w/ 2 delegate kernels.
...
```

Executing part of the network on the CPU will increase inference times, sometimes considerably. To better understand which are the problematic layers and where the time is spent, it can be useful to run `benchmark_model` with the option `--enable_op_profiling=true`. This option generates a detailed report of the layers executed on the CPU and the time spent executing them. For example, in the execution here below, the network contains a `RESIZE_NEAREST_NEIGHBOR` layer which falls back to CPU execution:
```
$ adb shell benchmark_model ... --enable_op_profiling=true
...
Operator-wise Profiling Info for Regular Benchmark Runs:
============================== Run Order ==============================
            [node type]  [first]  [avg ms]      [%]    [cdf%]  [mem KB] [times called] [Name]
    TfLiteNnapiDelegate    3.826     4.011  62.037%   62.037%     0.000         1      []:64
RESIZE_NEAREST_NEIGHBOR    0.052     0.058   0.899%   62.936%     0.000         1      []:38
    TfLiteNnapiDelegate    2.244     2.396  37.064%  100.000%     0.000         1      []:65
```

Execution of the model (or part of it) on the NPU can also be confirmed by looking at the SyNAP `inference_count` file in `sysfs` (see section [sysfs-inference-counter](/docs/synap/statistics#inference_count)).

For an even more in-depth analysis, it is possible to obtain detailed layer-by-layer inference timing by setting the profiling property before running `benchmark_model`:
```
$ adb shell setprop vendor.NNAPI_SYNAP_PROFILE 1
$ adb shell benchmark_model --graph=/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite --use_nnapi=true --nnapi_accelerator_name=synap-npu
```
On Android, the profiling information will be available in `/sys/class/misc/synap/device/misc/synap/statistics/network_profile` while `benchmark_model` is running. On Yocto Linux, the same information is in `/sys/class/misc/synap/statistics/network_profile`.

:::note
When `vendor.NNAPI_SYNAP_PROFILE` is enabled, the network is executed step-by-step, so the overall inference time becomes meaningless and should be ignored.
:::

## NNAPI Compilation Caching

NNAPI compilation caching provides even greater speedup than the default SyNAP cache by caching entire compiled models, but it requires some support from the application (see [Android Neural Networks API Compilation Caching](https://source.android.com/devices/neural-networks/compilation-caching)) and requires more disk space.

NNAPI caching support must be enabled by setting the corresponding android property:
```
$ adb shell setprop vendor.npu.cache.model 1
```

As explained in the official Android documentation, for NNAPI compilation cache to work, the user has to provide a directory to store the cached model and a unique key for each model. The unique key is normally determined by computing some hash on the entire model.

This can be tested using `benchmark_model`:
```
$ adb shell benchmark_model --graph=/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite --use_nnapi=true --nnapi_accelerator_name=synap-npu --delegate_serialize_dir=/data/local/tmp/nnapiacache --delegate_serialize_token='`md5sum -b /data/local/tmp/mobilenet_v1_0.25_224_quant.tflite`'
```

During the first execution of the above command, NNAPI will compile the model and add it to the cache:
```
INFO: Initialized TensorFlow Lite runtime.
INFO: Created TensorFlow Lite delegate for NNAPI.
NNAPI delegate created.
ERROR: File /data/local/tmp/nnapiacache/a67461dd306cfd2ff0761cb21dedffe2_6183748634035649777.bin couldn't be opened for reading: No such file or directory
INFO: Replacing 31 node(s) with delegate (TfLiteNnapiDelegate) node, yielding 1 partitions.
...
Inference timings in us: Init: 34075, First inference: 1599062, Warmup (avg): 1.59906e+06, Inference (avg): 1380.86
```

In all the following executions, NNAPI will load the compiled model directly from the cache, so the first inference will be faster:
```
INFO: Initialized TensorFlow Lite runtime.
INFO: Created TensorFlow Lite delegate for NNAPI.
NNAPI delegate created.
INFO: Replacing 31 node(s) with delegate (TfLiteNnapiDelegate) node, yielding 1 partitions.
...
Inference timings in us: Init: 21330, First inference: 90853, Warmup (avg): 1734.13, Inference (avg): 1374.59
```

## Disabling NPU Usage from NNAPI

It is possible to make the NPU inaccessible from NNAPI by setting the property `vendor.NNAPI_SYNAP_DISABLE` to 1. In this case, any attempt to run a model via NNAPI will always fall back to CPU.

NNAPI execution with NPU enabled:
```
$ adb shell setprop vendor.NNAPI_SYNAP_DISABLE 0
$ adb shell 'echo > /sys/class/misc/synap/device/misc/synap/statistics/inference_count'
$ adb shell benchmark_model --graph=/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite --use_nnapi=true --nnapi_accelerator_name=synap-npu
Inference timings in us: Init: 24699, First inference: 1474732, Warmup (avg): 1.47473e+06, Inference (avg): 1674.03
$ adb shell cat /sys/class/misc/synap/device/misc/synap/statistics/inference_count
1004
```

NNAPI execution with NPU disabled:
```
$ adb shell setprop vendor.NNAPI_SYNAP_DISABLE 1
$ adb shell 'echo > /sys/class/misc/synap/device/misc/synap/statistics/inference_count'
$ adb shell benchmark_model --graph=/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite --use_nnapi=true --nnapi_accelerator_name=synap-npu
Inference timings in us: Init: 7205, First inference: 15693, Warmup (avg): 14598.5, Inference (avg): 14640.3
$ adb shell cat /sys/class/misc/synap/device/misc/synap/statistics/inference_count
0
```

:::note
It will still be possible to perform online inference on the NPU using the *timvx* tflite delegate.
:::

## Online Inference with *TimVx* Delegate

NNAPI is not the only way to perform online inference on the NPU. It is possible to run a model without using NNAPI by loading it with the standard TensorFlow Lite API and then using the *timvx* tflite delegate. This delegate has been optimized to call directly the SyNAP API, so it can most often provide better performance and fewer limitations than the standard NNAPI.

Another advantage of the `timvx` delegate is that it is also available on Yocto Linux platforms which don't support NNAPI. The only limitation of this approach is that being a delegate for the standard TensorFlow runtime, it doesn't support the execution of other model formats such as ONNX.

*timvx* tflite delegate internal workflow is similar to that of NNAPI: when a tflite model is loaded, it is automatically converted to the internal representation suitable for execution on the NPU. This conversion doesn't take place when the model is loaded but when the first inference is executed.

## Benchmarking Models with *TimVx* Delegate

Synaptics `benchmark_model` tool provides built-in support for both the standard `nnapi` delegate and the optimized `timvx` delegate.

Benchmarking a model with `timvx` delegate is as simple as using NNAPI:

1. Download the tflite model to be benchmarked, for example:
    ```
    https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_0.25_224_quant.tgz
    ```
2. Copy the model to the board, for example in the `/data/local/tmp` directory:
    ```
    $ adb push mobilenet_v1_0.25_224_quant.tflite /data/local/tmp
    ```
3. Benchmark the model execution on the NPU with `timvx` delegate (both android and linux):
    ```
    $ adb shell benchmark_model --graph=/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite --external_delegate_path=libvx_delegate.so

    INFO: STARTING!
    INFO: Tensorflow Version : 2.15.0
    INFO: Log parameter values verbosely: [0]
    INFO: Graph: [/data/local/tmp/mobilenet_v1_0.25_224_quant.tflite]
    INFO: External delegate path: [/vendor/lib64/libvx_delegate.so]
    INFO: Loaded model /data/local/tmp/mobilenet_v1_0.25_224_quant.tflite
    INFO: Initialized TensorFlow Lite runtime.
    INFO: Vx delegate: allowed_cache_mode set to 0.
    INFO: Vx delegate: device num set to 0.
    INFO: Vx delegate: allowed_builtin_code set to 0.
    INFO: Vx delegate: error_during_init set to 0.
    INFO: Vx delegate: error_during_prepare set to 0.
    INFO: Vx delegate: error_during_invoke set to 0.
    INFO: EXTERNAL delegate created.
    VERBOSE: Replacing 31 out of 31 node(s) with delegate (Vx Delegate) node, yielding 1 partitions for the whole graph.
    INFO: Explicitly applied EXTERNAL delegate, and the model graph will be completely executed by the delegate.
    INFO: The input model file size (MB): 0.497264
    INFO: Initialized session in 25.573ms.
    INFO: Running benchmark for at least 1 iterations and at least 0.5 seconds but terminate if exceeding 150 seconds.
    type 54 str SoftmaxAxis0
    INFO: count=277 first=201009 curr=863 min=811 max=201009 avg=1760.78 std=11997

    INFO: Running benchmark for at least 50 iterations and at least 1 seconds but terminate if exceeding 150 seconds.
    INFO: count=876 first=1272 curr=1730 min=810 max=6334 avg=1096.48 std=476

    INFO: Inference timings in us: Init: 25573, First inference: 201009, Warmup (avg): 1760.78, Inference (avg): 1096.48
    INFO: Note: as the benchmark tool itself affects memory footprint, the following is only APPROXIMATE to the actual memory footprint of the model at runtime. Take the information at your discretion.
    INFO: Memory footprint delta from the start of the tool (MB): init=15.4688 overall=43.2852
    ```

Comparing the timings with those in section [online Benchmarking Models with NNAPI](/docs/synap/nnapi#benchmarking-models-with-nnapi), we can notice that even for this simple model, `timvx` delegate provides better performances than NNAPI (average inference time 1096 us vs 1885).
