Model Compilation
=================

Model Conversion
----------------

The `SyNAP` toolkit allows you to compile a model from its original format to an internal representation optimized for the target hardware. The conversion tool and utilities can run on Linux, MacOS, or Windows hosts inside a *Docker* container. Only `Docker` and the `toolkit` image are required; no additional dependencies need to be installed.

## Supported formats

* Tensorflow Lite (`.tflite` extension)
* ONNX (`.onnx` extension)
* TorchScript (`.torchscript`, `.pt`, `.pth` extensions)
* Tensorflow (`.pb` extension)
* Caffe (`.prototxt` extension)

:::note

PyTorch models can be saved in different formats, only TorchScript format is supported. See [Working with PyTorch Models](/docs/synap/model_compilation#working-with-pytorch-models) for more information.

::: 

:::note

Only standard Caffe 1.0 models are supported. Custom variants such as *Caffe-SSD* or *Caffe-LSTM* models or legacy (pre-1.0) models require specific parsers which are currently not available in SyNAP toolkit. *Caffe2* models are not supported as well.

:::

:::warning

Support for `.pb` and `.prototxt` formats is deprecated.

:::

## Installing Docker

A few installation hints are provided below. Please note that these are not a replacement for the official [Docker] documentation. For more details, please refer to [Docker website](https://docs.docker.com/get-docker).

### Linux (Ubuntu)

```bash
apt-get install docker.io
```

To be able to run Docker without superuser privileges, also run the two commands below once after Docker installation (for more info, refer to [linux postinstall](https://docs.docker.com/engine/install/linux-postinstall):

```bash
# Create the docker group if it doesn't already exist
sudo groupadd docker
# Add the current user "$USER" to the docker group
sudo usermod -aG docker $USER
```

### macOS - Docker

The easiest way to install Docker on macOS is via the `brew` package manager. If you don’t have it installed yet, please follow the official [brew](https://brew.sh) website. After brew is installed, you can install Docker:

:::important

On macOS, the Docker GUI is not free for use in commercial applications. A valid alternative is [Colima](https://github.com/abiosoft/colima).

:::

```bash
brew install docker
```

See the note in the Linux installation above to run Docker without superuser privileges.

### macOS - Colima

[Colima](https://github.com/abiosoft/colima) is a free container runtime on macOS that can be used as a replacement for Docker. It doesn’t have a GUI but is easy to install and configure:

```bash
brew install colima
mkdir -p ~/.docker/cli-plugins
brew install docker-buildx
ln -sfn $(brew --prefix)/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
colima start --vm-type vz --mount-type virtiofs --cpu 4 --memory 8 --disk 80
```

After the above commands, you can use [Colima] to work with Docker containers. The settings are stored in a config file `~/.colima/default/colima.yaml` and can be modified by editing the file if needed. Colima has to be started after each restart of the Mac:

```bash
colima start
```

### Windows

The suggested way to run Docker on Windows is to install it inside a Linux Virtual Machine using *WSL2*, available from Windows 10.

**Important:**

Running Docker directly in Windows is incompatible with the presence of a VM. For this reason, using a Linux VM in WSL2 is usually the best option.

#### *WSL2* Installation Steps

1. Run *Windows PowerShell* App as Administrator and execute the following command to install WSL2:

   ```bash
   wsl --install
   ```

   When completed, restart the computer.

2. Run *Windows PowerShell* App as before and install *Ubuntu-22.04*:

   ```bash
   wsl --install -d Ubuntu-22.04
   ```

3. Run *Windows Terminal* App and select the *Ubuntu-22.04* distribution. From there, install Docker and the *SyNAP* toolkit following the instructions in `using-docker-ubuntu-label` above.

For more information on WSL2 installation and setup, please refer to the official Microsoft documentation:
[WSL Install](https://learn.microsoft.com/en-us/windows/wsl/install) and [WSL Environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).


Installing SyNAP Tools
----------------------

Before installing the SyNAP toolkit, please be sure that you have a working Docker installation The simplest way to do this is to run the
`hello-world` image:

``` 
$ docker run hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from libraryhello-world
...
...
Hello from Docker!
This message shows that your installation appears to be working correctly
```

If the above command doesn't produce the expected output please check the instructions in the previous section or refer to the official Docker
documentation for your platform If all is well you can proceed with the installation of the toolkit

The SyNAP toolkit is distributed as a Docker image, to install it just download the image from the SyNAP github repository:

``` 
docker pull ghcriosynaptics-synaptoolkit:#SyNAP_Version#
```

This image contains not only the conversion tool itself but also all the required dependencies and additional support utilities

You can find the latest version of the toolkit [here](https://github.com/synaptics-synap/toolkit/pkgs/container/toolkit).


Running SyNAP Tools
-------------------

Once Docker and the **SyNAP toolkit** image are installed, the model conversion tool can be executed directly inside a Docker container. The source and converted models can be accessed on the host filesystem by mounting the corresponding directories when running the container. For this reason, it is important to run the container using the same user/group that owns the files to be converted. To avoid manually specifying these options at each execution, it’s suggested to create a simple alias and add it to the user’s startup file (e.g., `.bashrc` or `.zshrc`):

```bash
alias synap='docker run -i --rm -u $(id -u):$(id -g) -v $HOME:$HOME -w $(pwd) ghcr.io/synaptics-synap/toolkit:3.1.0'
```

The options have the following meaning:


- **`-i`**:  
  Run the container interactively (required for commands that read data from `stdin`, such as `image_od`).

- **`--rm`**:  
  Remove the container when it exits (stopped containers are not needed anymore).

- **`-u $(id -u):$(id -g)`**:  
  Run the container as the current user (so files will have the correct access rights).

- **`-v $HOME:$HOME`**:  
  Mmount the user’s home directory so that its entire content is visible inside the container. If some models or data are located outside the home directory, additional directories can be mounted by repeating the `-v` option, for example add: `-v /mnt/data:/mnt/data`. It’s important to specify the same path outside and inside the container so absolute paths work as expected.

- **`-w $(pwd)`**:  
  Set the working directory of the container to the current directory, so that relative paths specified in the command line are resolved correctly.

With the above alias, the desired *SyNAP* tool command line is just passed as a parameter, for example:

```shell
$ synap help

SyNAP Toolkit

Docker alias:
    alias synap='docker run -i --rm -u $(id -u):$(id -g) -v $HOME:$HOME -w $(pwd) \
                 ghcr.io/synaptics-synap/toolkit:3.1.0'
    Use multiple -v options if needed to mount additional directories eg: -v /mnt/dat:/mnt/dat

Usage:
    synap COMMAND ARGS
    Run 'synap COMMAND --help' for more information on a command.

Commands:
    convert           Convert and compile model
    help              Show help
    image_from_raw    Convert image file to raw format
    image_to_raw      Generate image file from raw format
    image_od          Superimpose object-detection boxes to an image
    version           Show version
```

As already noted there is no need to be `root` to run docker. In case you get a Permission Denied error when executing the above command, please refer to [Linux (Ubuntu)](/docs/synap/model_compilation#linux-ubuntu).


The toolkit provides several tools to convert and manipulate models and images.

Model conversion can be performed using the `convert` command. It takes as input:

- A network model
- The target hardware for which to convert the model (e.g., VS680 or VS640)
- The name of the directory where to generate the converted model
- An optional YAML metafile that can be used to specify customized conversion options (mandatory for `.pb` models)

The output generates three files:

- **model.synap**: The converted network model
- **model_info.txt**: Additional information about the generated model for user reference, including:
  - Input/output tensors attributes
  - Subgraph splitting
  - Layer table
  - Operation table
  - Memory usage
- **quantization_info.txt**: Additional quantization information (only if the model is quantized using the toolkit)

An additional `cache` directory is also generated to speed up future compilations of the same model.

Example:

```shell
$ synap convert --model mobilenet_v1_quant.tflite --target VS680 --out-dir mnv1
$ ls mnv1
model_info.txt  model.synap  cache
```

In the case of `Caffe` models, the weights are not in the `.prototxt` file but stored in a separate file, generally with a `.caffemodel` extension. This file must be provided as input to the converter tool as well. Example:

```shell
$ synap convert --model mnist.prototxt --weights mnist.caffemodel --target VS680 --out-dir out
```

:::important

The model file and the output directory specified must be inside or below a directory mounted inside the Docker container (see `-v` option in the `synap` alias above).

:::

Preprocessing
-------------

The size, layout, format, and range of the data to be provided in the input tensor(s) of a network are defined when the network model is created and trained. For example, a typical `mobilenet-v1` `.tflite` model will expect an input image of size 224x224, with NHWC layout and channels organized in RGB order, with each pixel value normalized (rescaled) in the range [-1, 1].

Unfortunately, in real-world usage, the image to be processed is rarely available in this exact format. For example, the image may come from a camera in 1920x1080 YUV format. This image must then be converted to RGB, resized, and normalized to match the expected input. Many libraries exist to perform this kind of conversion, but the problem is that these computations are quite compute-intensive, so even if deeply optimized, doing this on the CPU will often require more time than that required by the inference itself.

Another option is to retrain the network to accept the same data format that will be available at runtime. This option, while sometimes a good idea, also presents its own problems. For example, it might not always be possible or practical to retrain a network, especially if the task has to be repeated for several input sizes and formats.

To simplify and speed up this task, the SyNAP Toolkit allows you to automatically insert input preprocessing code when a model is converted. This code is executed directly in the NPU and in some cases can be an order of magnitude faster than the equivalent operation in the CPU. An alternative to adding the preprocessing to the original model is to create a separate "preprocessing model" whose only purpose is to convert the input image to the desired format and size, and then execute the two models in sequence without any additional data copy, see [Buffer Sharing](/docs/synap/framework_api#buffer-sharing). This can be convenient if the original model is large and the input can come in a variety of possible formats. Preprocessing models for the most common cases already come preinstalled.

The available preprocessing options are designed for images and support five kinds of transformations:

- Format conversion (e.g., YUV to RGB, or RGB to BGR)
- Cropping
- Resize and downscale (without preserving proportions)
- Normalization to the required value range (e.g., normalize [0, 255] to [-1, 1])
- Data-type conversion (from uint8 to the data type of the network input layer, e.g., float16 or int16)

Preprocessing is enabled by specifying the `preprocess` section in the input specification in the `.yaml` file. This section contains the following fields (the fields marked `(*)` are mandatory). Note that the *mean* and *scale* used to normalize the input values don't appear here because they are the same used to quantize the model (see `means` and `scale` fields in the input specification).

### `type` (*)

This field specifies the format of the input data that will be provided to the network. Only image formats are supported at the moment. The SyNAP toolkit will add the required operations to convert the input data to the `format` and layout expected by the network input tensor. If the `format` of the network input tensor is not specified, it is assumed to be `rgb` by default. If this field is set to the empty string or to "none", no preprocessing is applied.

Not all conversions are supported: `gray` input can only be used if the input tensor has one channel. All the other input formats except `float32` can only be used if the input tensor has three channels.

Some input formats generate multiple data inputs for one network tensor. For example, if `nv12` is specified, the converted network will have two inputs: the first for the `y` channel, the second for the `uv` channels. The preprocessing code will combine the data from these two inputs to feed the single `rgb` or `bgr` input tensor of the network.

The following table contains a summary of all the supported input formats and for each the properties and meaning of each generated input tensor. Note that the layout of the input data is always `NHWC` except for the `rgb888-planar` and `float32` formats. In all cases, `H` and `W` represent the height and width of the input image. If the size of the input image is not explicitly specified, these are taken from the `H` and `W` of the network input tensor. In all cases, each pixel component is represented with 8 bits.

The `float32` type is a bit special in the sense that in this case the input is not considered to be an 8-bits image but raw 32-bits floating point values which are converted to the actual data type of the tensor. For this reason, any tensor shape is allowed and resizing via the `size` field is not supported.

| Preprocessing Type | Input# | Shape       | Format | Input Description           |
|--------------------|--------|-------------|--------|-----------------------------|
| yuv444             | 0      | NHW1        | y8     | Y component                 |
|                    | 1      | NHW1        | u8     | U component                 |
|                    | 2      | NHW1        | v8     | V component                 |
| yuv420             | 0      | NHW1        | y8     | Y component                 |
|                    | 1      | N(H/2)(W/2)1| u8     | U component                 |
|                    | 2      | N(H/2)(W/2)1| v8     | V component                 |
| nv12               | 0      | NHW1        | y8     | Y component                 |
|                    | 1      | N(H/2)(W/2)2| uv8    | UV components interleaved   |
| nv21               | 0      | NHW1        | y8     | Y component                 |
|                    | 1      | N(H/2)(W/2)2| vu8    | VU components interleaved   |
| gray               | 0      | NHW1        | y8     | Y component                 |
| rgb                | 0      | NHW3        | rgb    | RGB components interleaved  |
| bgra               | 0      | NHW4        | bgra   | BGRA components interleaved |
| rgb888p            | 0      | N3HW        | rgb    | RGB components planar       |
| rgb888p3           | 0      | NHW1        | r8     | Red component               |
|                    | 1      | NHW1        | g8     | Green component             |
|                    | 2      | NHW1        | b8     | Blue component              |
| float32            | 0      | any         |        | Floating point data         |

:::note

Specifying a *dummy* preprocessing (for example from `rgb` input to `rgb` tensor) can be a way to implement normalization and data-type conversion using the NPU hardware instead of doing the same operations in software.

:::

### `size`

This optional field allows you to specify the size of the input image as a list containing the H and W dimensions in this order. Preprocessing will rescale the input image to the size of the corresponding input tensor of the network. The proportions of the input image are not preserved. If this field is not specified, the `WxH` dimension of the input image will be the same as the W and H of the network tensor.

### `crop`

Enable cropping. If specified, four additional scalar input tensors are added to the model (they can be seen in the generated `model_info.txt`). These inputs contain a single 32-bit integer each and are used to specify at runtime the dimension and origin of the cropping rectangle inside the input image. If security is enabled, these additional inputs will have the security attribute "any" so that it is always possible to specify the cropping coordinates from the user application even if the model and the other input/output tensors are secure. The cropping inputs are added after the original model input in the following order:

- Width of the cropping rectangle
- Height of the cropping rectangle
- Left coordinate of the cropping rectangle
- Top coordinate of the cropping rectangle

These inputs should be written using the `Tensor` scalar `assign()` method, which accepts a value in pixels and converts it to the internal representation. Preprocessing will rescale the specified cropping rectangle to the size of the corresponding input tensor of the network. The proportions of the input image are not preserved. The area of the image outside the cropping rectangle is ignored. The cropping coordinates must be inside the dimension of the input image; otherwise, the content of the resulting image is undefined.


Heterogeneous Inference
-----------------------

In some cases, it can be useful to execute different parts of a network on different hardware. For example, consider an object detection network where the initial part contains a bunch of convolutions and the final part some postprocessing layer such as `TFLite_Detection_PostProcess`. The NPU is heavily optimized for executing convolutions but doesn't support the postprocessing layer, so the best approach would be to execute the initial part of the network on the NPU and the postprocessing on the CPU.

This can be achieved by specifying the delegate to be used on a per-layer basis, using the same syntax as we’ve seen for mixed quantization in section [Mixed quantization](/docs/synap/model_quantization#mixed-quantization). For example, considering again the Model in [Figure 4](/docs/synap/model_quantization#mixed-quantization), we can specify that all layers should be executed on the NPU, except `conv5` and the layers that follows it which we want to execute on the GPU:



```yaml
# Execute the entire model on the NPU, except conv5 and conv6
delegate:
  '*': npu
  conv5: gpu
  conv5...: gpu
```

Another advantage of distributing processing to different hardware delegates is that when the model is organized in multiple independent branches (so that a branch can be executed without having to wait for the result of another branch), and each is executed on a different HW unit then the branches can be executed in parallel.

In this way, the overall inference time can be reduced to the time it takes to execute the slowest branch. Branch parallelization is always done automatically whenever possible.

:::note

Branch parallelization should not be confused with in-layer parallelization, which is also always active when possible. In the example above, the two branches `(conv3, conv4)` and `(conv5, conv6)` are executed in parallel, the former on the NPU and the latter on the GPU. In addition, each convolution layer is parallelized internally by taking advantage of the parallelism available in the NPU and GPU hardware.

:::

Model Conversion Tutorial
-------------------------

Let's see how to convert and run a typical object-detection model.

1. Download the sample `ssd_mobilenet_v1_1_default_1.tflite` object-detection model:

   [https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/default/1](https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/default/1)

2. Create a conversion metafile `ssd_mobilenet.yaml` with the content below (Important: be careful that newlines and formatting must be respected but they are lost when doing copy-paste from a PDF):

  ```yaml
  outputs:
  - name: Squeeze
    dequantize: true
    format: tflite_detection_boxes y_scale=10 x_scale=10 h_scale=5 w_scale=5 anchors=${ANCHORS}
  - name: convert_scores
    dequantize: true
    format: per_class_confidence class_index_base=-1
  ```

   A few notes on the content of this file:

   - `name: Squeeze` and `name: convert_scores` explicitly specify the output tensors where we want model conversion to stop. The last layer (`TFLite_Detection_PostProcess`) is a custom layer not suitable for NPU acceleration, so it is implemented in software in the `Detector` postprocessor class.
   - `dequantize: true` performs conversion from quantized to float directly in the NPU. This is much faster than doing conversion in software.
   - `tflite_detection_boxes` and `convert_scores` represent the content and data organization in these tensors.
   - `y_scale=10`, `x_scale=10`, `h_scale=5`, `w_scale=5` correspond to the parameters in the `TFLite_Detection_PostProcess` layer in the network.
   - `${ANCHORS}` is replaced at conversion time with the `anchor` tensor from the `TFLite_Detection_PostProcess` layer. This is needed to be able to compute the bounding boxes during postprocessing.
   - `class_index_base=-1` indicates that this model has been trained with an additional background class as index 0, so we subtract 1 from the class index during postprocessing to conform to the standard `coco` dataset labels.

3. Convert the model (ensure that the model, meta, and output directory are in a directory visible in the container, see `-v` option):

  ```shell
  $ synap convert --model ssd_mobilenet_v1_1_default_1.tflite --meta ssd_mobilenet.yaml --target VS680 --out-dir compiled
  ```

4. Push the model to the board:

  ```shell
  $ adb root
  $ adb remount
  $ adb shell mkdir /data/local/tmp/test
  $ adb push compiled/model.synap /data/local/tmp/test
  ```

5. Execute the model:

  ```shell
  $ adb shell
  # cd /data/local/tmp/test
  # synap_cli_od -m model.synap $MODELS/object_detection/coco/sample/sample001_640x480.jpg
  ```

  Example output:

  ```
  Input image: /vendor/firmware/.../sample/sample001_640x480.jpg (w = 640, h = 480, c = 3)
  Detection time: 5.69 ms
  #   Score  Class  Position  Size     Description
  0   0.70       2  395,103    69, 34  car
  1   0.68       2  156, 96    71, 43  car
  2   0.64       1  195, 26   287,445  bicycle
  3   0.64       2   96,102    18, 16  car
  4   0.61       2   76,100    16, 17  car
  5   0.53       2  471, 22   167,145  car
  ```

Model Profiling
---------------

When developing and optimizing a model, it can be useful to understand how the execution time is distributed among the layers of the network. This provides an indication of which layers are executed efficiently and which represent bottlenecks.

To obtain this information, the network has to be executed step by step so that each single timing can be measured. For this to be possible, the network must be generated with additional profiling instructions by calling `synap_convert.py` with the `--profiling` option, for example:

```shell
$ synap convert --model mobilenet_v2_1.0_224_quant.tflite --target VS680 --profiling --out-dir mobilenet_profiling
```

:::note

Even if the execution time of each layer doesn't change between *normal* and *profiling* mode, the overall execution time of a network compiled with profiling enabled will be noticeably higher than that of the same network compiled without profiling, due to the fact that NPU execution has to be started and suspended several times to collect the profiling data. For this reason, profiling should normally be disabled and enabled only when needed for debugging purposes.

:::

When a model is converted using the SyNAP toolkit, layers can be fused, replaced with equivalent operations, and/or optimized away. Hence, it is generally not possible to find a one-to-one correspondence between the items in the profiling information and the nodes in the original network. For example, adjacent convolution, ReLU, and Pooling layers are fused together in a single *ConvolutionReluPoolingLayer* layer whenever possible. Despite these optimizations, the correspondence is normally not too difficult to find. The layers shown in the profiling correspond to those listed in the `model_info.txt` file generated when the model is converted.

After each execution of a model compiled in profiling mode, the profiling information will be available in `sysfs`, see [Statistics and Usage
](/docs/synap/statistics). Since this information is not persistent but goes away when the network is destroyed, the easiest way to collect it is by using the `synap_cli` program. The `--profiling [filename](filename)` option allows saving a copy of the `sysfs` `network_profile` file to a specified file before the network is destroyed:

```shell
$ adb push mobilenet_profiling $MODELS/image_classification/imagenet/model/
$ adb shell
# cd $MODELS/image_classification/imagenet/model/mobilenet_profiling
# synap_cli -m model.synap --profiling mobilenet_profiling.txt random

# cat mobilenet_profiling.txt
pid: 21756, nid: 1, inference_count: 78, inference_time: 272430, inference_last: 3108, iobuf_count: 2, iobuf_size: 151529, layers: 34
| lyr |   cycle | time_us | byte_rd | byte_wr | type
|   0 |  152005 |     202 |  151344 |       0 | TensorTranspose
|   1 |  181703 |     460 |    6912 |       0 | ConvolutionReluPoolingLayer2
|   2 |    9319 |      51 |    1392 |       0 | ConvolutionReluPoolingLayer2
|   3 |   17426 |      51 |    1904 |       0 | ConvolutionReluPoolingLayer2
|   4 |   19701 |      51 |    1904 |       0 | ConvolutionReluPoolingLayer2
...
|  28 |   16157 |      52 |    7472 |       0 | ConvolutionReluPoolingLayer2
|  29 |  114557 |     410 |  110480 |       0 | FullyConnectedReluLayer
|  30 |  137091 |     201 |    2864 |    1024 | Softmax2Layer
|  31 |       0 |       0 |       0 |       0 | ConvolutionReluPoolingLayer2
|  32 |       0 |       0 |       0 |       0 | ConvolutionReluPoolingLayer2
|  33 |     670 |      52 |    1008 |       0 | ConvolutionReluPoolingLayer2
```

Compatibility with SyNAP 2.x
----------------------------

SyNAP 3.x is fully backward compatible with SyNAP 2.x.

- It is possible to execute models compiled with the SyNAP 3.x toolkit with the SyNAP 2.x runtime. The only limitation is that in this case, heterogeneous compilation is not available, and the entire model will be executed on the NPU. This can be done by specifying the `--out-format nb` option when converting the model. In this case, the toolkit will generate the legacy `model.nb` and `model.json` files instead of the `model.synap` file:

  ```shell
  $ synap convert --model mobilenet_v2_1.0_224_quant.tflite --target VS680 --out-format nb --out-dir mobilenet_legacy
  ```

- It is possible to execute models compiled with the SyNAP 2.x toolkit with the SyNAP 3.x runtime.
- The SyNAP 3.x API is an extension of the SyNAP 2.x API, so all existing applications can be used without any modification.


## Working with PyTorch Models

PyTorch framework supports very flexible models where the architecture and behavior of the network are defined using Python classes instead of fixed graph layers (e.g., as in `TFLite`). When saving a model, normally only the `state_dict`, which includes the learnable parameters, is saved, and not the model structure itself. ([Saving and Loading Models in PyTorch](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-loading-model-for-inference)). 

The original Python code used to define the model is needed to reload and execute it. Therefore, it is not possible to directly import a PyTorch model from a `.pt` file containing only the learnable parameters.


### Saving PyTorch Models including Model Structure
When saving a PyTorch model in a `.pt` file, it is possible to include references to the Python classes defining the model. However, recreating the model still requires access to the exact Python source code used to generate it.

### Saving in TorchScript Format
A more portable alternative is to save the model in `TorchScript` format. This format includes both the learnable parameters and the model structure, allowing for direct import into other tools such as the SyNAP toolkit.

For details on how to save a model in `TorchScript` format, refer to the [official PyTorch documentation](https://pytorch.org/tutorials/beginner/saving_loading_models.html#export-load-model-in-torchscript-format).

#### Tracing vs Scripting
Saving a model in `TorchScript` format can be done via scripting or tracing:
- **Scripting**: Converts the model into a `torch.jit.ScriptModule` by analyzing its structure.
- **Tracing**: Records operations executed when running the model, useful for models with dynamic structures.

Both techniques produce the same format, and models saved using tracing can also be imported directly. A detailed comparison is available online by searching for "PyTorch tracing vs scripting."

### Example Code for Saving TorchScript Models
```python
import torch
import torchvision

# An instance of your model
model = torchvision.models.mobilenet_v2(pretrained=True)

# Switch the model to eval mode
model.eval()

# Generate a torch.jit.ScriptModule via scripting
mobilenet_scripted = torch.jit.script(model)
mobilenet_scripted.save("mobilenet_scripted.torchscript")

# Generate a torch.jit.ScriptModule via tracing
example = torch.rand(1, 3, 224, 224)
mobilenet_traced = torch.jit.trace(model, example)
mobilenet_traced.save("mobilenet_traced.torchscript")
```


:::important

Even if there exists multiple possible ways to save a PyTorch model to a file, there is no
agreed convention for the extension used in the different cases, and `.pt` or `.pth` extension is commonly used
no matter the format of the file. Only `TorchScript` models can be imported with the SyNAP toolkit,
if the model is in a different format the import will fail with an error message.

:::

:::note

Working with `TorchScript` models is not very convenient when performing mixed quantization or
heterogeneous inference, as the model layers sometimes don't have names or the name is modified during the
import process and/or there is not a one-to-one correspondence between the layers in the original
model and the layers in the imported one. The suggestion in this case is to compile the model
with the ``--preserve`` option and then look at the intermediate ``build/model.onnx`` file
inside the output directory.

:::


An even more portable alternative to exporting a model to TorchScript is to export it to ONNX format.
The required code is very similar to the one used to trace the model:

```python
import torch
import torchvision
    
# An instance of your model
model = torchvision.models.mobilenet_v2(pretrained=True)
    
# Switch the model to eval model
model.eval()
    
# Export the model in ONNX format
torch.onnx.export(model, torch.rand(1, 3, 224, 224), "mobilenet.onnx")
```


## Importing YOLO PyTorch Models


The popular YOLO library from `ultralytics` provides pretrained .pt models on their website.
All these models are not in `TorchScript` format and so can't be imported directly with the SyNAP toolkit.
nevertheless it's very easy to export them to `ONNX` or `TorchScript` so that they can be imported:

```python
from ultralytics import YOLO

# Load an official YOLO model
model = YOLO("yolov8s.pt")

# Export the model in TorchScript format
model.export(format="torchscript", imgsz=(480, 640))

# Export the model in ONNX format
model.export(format="onnx", imgsz=(480, 640))
```

More information on exporting YOLO models to ONNX in https://docs.ultralytics.com/modes/export/ 

Most public domain machine learning packages provide similar export functions for their PyTorch models.