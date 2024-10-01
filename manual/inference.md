# Inference

## Introduction

1. The easiest way to get started is using the CLI commands.
2. For application development, a C++ library API etc.

The simplest way to start experimenting with *Synp* is to use the sample precompiled models and applications that come preinstalled on the board.

> **Important**: On Android the sample models can be found in `/vendor/firmware/models/` while on Yocto Linux they are in `/usr/share/synap/models/`. In this document we will refer to this directory as `$MODELS`.

The models are organized in broad categories according to the type of data they take in input and the information they generate in output. Inside each category, models are organized per topic (for example "imagenet") and for each topic a set of models and sample input data is provided.

For each category a corresponding command line test application is provided.

| **Category**          | **Input** | **Output**                                        | **Test App**        |
|-----------------------|-----------|--------------------------------------------------|---------------------|
| image_classification  | image     | probabilities (one per class)                    | synap_cli_ic        |
| object_detection      | image     | detections (bound.box+class+probability)         | synap_cli_od        |
| image_processing      | image     | image                                            | synap_cli_ip        |

In addition to the specific applications listed above `synap_cli` can be used to execute models of all categories. The purpose of this application is not to provide high-level outputs but to measure inference timings. This is the only sample application that can be used with models requiring secure inputs or outputs.

### `synap_cli_ic` application

This command line application allows to easily execute *image_classification* models.

It takes in input:
- the converted synap model (*.synap* extension)
- one or more images (*jpeg* or *png* format)

It generates in output:
- the top 5 most probable classes for each input image provided

> **Note**: The jpeg/png input image(s) are resized in SW to the size of the network input tensor. This is not included in the classification time displayed.

Example:
```sh
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
```

### `synap_cli_od` application

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

> **Note**: The jpeg/png input image(s) are resized in SW to the size of the network input tensor.

Example:
```sh
$ cd $MODELS/object_detection/people/model/mobilenet224_full1/
$ synap_cli_od -m model.synap ../../sample/sample001_640x480.jpg
Input image: ../../sample/sample001_640x480.jpg (w = 640, h = 480, c = 3)
Detection time: 26.94 ms
#   Score  Class  Position  Size     Description
0   0.95       0   94,193    62,143  person
```

> **Important**: The output of object detection models is not standardized, many different formats exist. The output format used has to be specified when the model is converted, see `model_conversion_tutorial`. If this information is missing or the format is unknown `synap_cli_od` doesn’t know how to interpret the result and so it fails with an error message: *"Failed to initialize detector"*.

### `synap_cli_ip` application

This command line application allows to execute *image_processing* models. The most common case is the execution of super-resolution models that take in input a low-resolution image and generate in output a higher resolution image.

It takes in input:
- the converted synap model (*.synap* extension)
- optionally the region of interest in the image (if supported by the model)
- one or more raw images with one of the following extensions: *nv12*, *nv21*, *rgb*, *bgr*, *bgra*, *gray*  or *bin*

It generates in output:
- a file containing the processed image in for each input file.

  The output file is called `outimage<i>_<W>x<H>.<ext>`, where `<i>` is the index of the corresponding input file, `<W>` and `<H>` are the dimensions of the image, and `<ext>` depends on the type of the output image, for example `nv12` or `rgb`. The output files are created in the current directory, and this can be changed with the `--out-dir` option.

> **Note**: The input image(s) are automatically resized to the size of the network input tensor. This is not supported for `nv12`: if the network takes in input an `nv12` image, the file provided in input must have the same format and the *WxH* dimensions of the image must correspond to the dimensions of the input tensor of the network.

> **Note**: Any `png` and `jpeg` image can be converted to `nv12` and rescaled to the required size using the `image_to_raw` command available in the *SyNAP* `toolkit` (for more info see `using-docker-label`). In the same way the generated raw `nv12` or `rgb` images can be converted to `png` or `jpeg` format using the `image_from_raw` command.

Example:
```sh
$ cd $MODELS/image_processing/super_resolution/model/sr_qdeo_y_uv_1920x1080_3840x2160
$ synap_cli_ip -m model.synap ../../sample/ref_1920x1080.nv12
Input buffer: input_0 size: 1036800
Input buffer: input_1 size: 2073600
Output buffer: output_13 size: 4147200
Output buffer: output_14 size: 8294400

Input image: ../../sample/ref_1920x1080.nv12
Inference time: 30.91 ms
Writing output to file: outimage0_3840x2160.nv12
```

### `synap_cli_ic2` application

This application executes two models in sequence, the input image is fed to the first model and its output is then fed to the second one which is used to perform classification as in `synap_cli_ic`. It provides an easy way to experiment with 2-stage inference, where for example the first model is a *preprocessing* model for downscaling and/or format conversion and the second is an *image_classification* model.

It takes in input:
- the converted synap *preprocessing* model (*.synap* extension)
- the converted synap *classification* model (*.synap* extension)
- one or more images (*jpeg* or *png* format)

It generates in output:
- the top 5 most probable classes for each input image provided

> **Note**: The shape of the output tensor of the first model must match that of the input of the second model.

Example:
```sh
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
```

The classification output is very close to what we get in `synap_cli_ic`, the minor difference is due to the difference in the image rescaled from NV12. The bigger overall inference time is due to the processing required to perform rescale and conversion of the input 1920x1080 image.

### `synap_cli` application

This command line application can be used to run models of all categories. The purpose of `synap_cli` is not to show inference results but to benchmark the network execution times. So it provides additional options that allow to run inference multiple times in order to collect statistics.

An additional feature is that `synap_cli` can automatically generate input images with random content. This