# Conversion Metafile

When converting a model, it is possible to provide a YAML metafile to customize the generated model. For example, it is possible to specify:

- The data representation in memory (nhwc or nchw)
- Model quantization options
- Output dequantization
- Input preprocessing options
- Delegate to be used for inference (npu, gpu, cpu)

Example:

```sh
$ synap convert --model mobilenet_v1_quant.tflite --meta mobilenet.yaml --target VS680 --out-dir mnv1
```

This metafile is mandatory when converting a TensorFlow `.pb` model. It can be completely omitted when converting a quantized `.tflite` model.

The best way to understand the content of a metafile is probably to first look at an example. Here is one for a typical *mobilenet_v1* model, followed by a detailed description of each field. Most of the fields are optional; mandatory fields are explicitly marked.

```yaml
delegate: npu

data_layout: nhwc

security:
    secure: true
    file: ../security.yaml

inputs:
  - name: input
    shape: [1, 224, 224, 3]
    means: [128, 128, 128]
    scale: 128
    format: rgb
    security: any
    preprocess:
        type: nv21
        size: [1920, 1080]
        crop: true

outputs:
  - name: MobilenetV1/Predictions/Reshape_1
    dequantize: false
    format: confidence_array

quantization:
    data_type: uint8
    scheme: default
    mode: standard
    algorithm: standard
    options:
    dataset:
      - ../../sample/*_224x224.jpg
```

## Fields

### `delegate`

Select the delegate to use for inference. Available delegates are:

- `default` (default, automatically select delegate according to the target HW)
- `npu`
- `gpu`
- `cpu`

If not specified, the default delegate for the target hardware is used. It is also possible to specify the delegate on a layer-by-layer basis. See section `heterogeneous_inference`.

### `data_layout`

The data layout in memory. Allowed values are: `default`, `nchw`, and `nhwc`.

For TensorFlow and TensorFlow Lite models, the default is `nhwc`. Forcing the converted model to be `nchw` might provide some performance advantage when the input data is already in this format since no additional data reorganization is needed.

For Caffe and ONNX models, the default is `nchw`. In this case, it is not possible to force to `nhwc`.

### `input_format`

Format of the input tensors. This is an optional string that will be attached as an attribute to all the network input tensors for which a "format" field has not been specified.

### `output_format`

Format of the output tensors. This is an optional string that will be attached as an attribute to all the network output tensors for which a "format" field has not been specified.

### `security`

This section contains security configuration for the model. If this section is not present, security is disabled. Security is only supported with the `npu` delegate.

- `secure`: If true, enable security for the model. For secure models, it is also possible to specify the security policy for each input and output. A secure model is encrypted and signed at conversion time so that its structure and weights will not be accessible and its authenticity can be verified. This is done by a set of keys and certificates files whose path is contained in a security file.
- `file`: Path to the security file. This is a `yaml` file with the following fields:

```yaml
encryption_key: `<path-to-encryption-key-file>`
signature_key: `<path-to-signature-key-file>`
model_certificate: `<path-to-model-certificate-file>`
vendor_certificate: `<path-to-vendor-certificate-file>`
```

Both relative and absolute paths can be used. Relative paths are considered relative to the location of the security file itself. The same fields can also be specified directly in the model metafile in place of the 'file' field. For detailed information on the security policies and how to generate and authenticate a secure model, please refer to SyNAP_SyKURE.pdf.

### `inputs` (pb)

Must contain one entry for each input of the network. Each entry has the following fields:

- `name` (pb): Name of the input in the network graph. For `tflite` and `onnx` models, this field is not required but can still be used to specify a different input layer than the default input of the network. This feature allows converting just a subset of a network without having to manually edit the source model. For `.pb` models or when `name` is not specified, the inputs must be in the same order as they appear in the model. When this field is specified, the `shape` field is mandatory.
- `shape` (pb): Shape of the input tensor. This is a list of dimensions; the order is given by the layout of the input tensor in the model (even if a different layout is selected for the compiled model). The first dimension must represent by convention the number of samples *N* (also known as "batch size") and is ignored in the generated model, which always works with a batch-size of 1. When this field is specified, the `name` field is mandatory.
- `means`: Used to normalize the range of input values. A list of mean values, one for each channel in the corresponding input. If a single value is specified instead of a list, it will be used for all the channels. If not specified, a mean of `0` is assumed. The *i-th* channel of each input is normalized as: `norm = (in - means[i]) / scale`.
- `scale`: Used to normalize the range of input values. The scale is a single value for all the channels in the corresponding input. If not specified, a scale of `1` is assumed.
- `format`: Information about the type and organization of the data in the tensor. The content and meaning of this string are custom-defined. However, SyNAP Toolkit and SyNAP `Preprocessor` recognize by convention an initial format type optionally followed by one or more named attributes: `<format-type> [<key>=value]...`. Recognized types are `rgb` (default): 8-bits RGB or RGBA or grayscale image, `bgr`: 8-bits BGR image or BGRA or grayscale image. Recognized attributes are `keep_proportions=1` (default): preserve aspect-ratio when resizing an image using `Preprocessor` or during quantization, `keep_proportions=0`: don't preserve aspect-ratio when resizing an image using `Preprocessor` or during quantization. Any additional attribute if present is ignored by SyNAP.
- `preprocess`: Input preprocessing options for this input tensor. It can contain the following fields:
  - `type`: format of the input data (e.g. `rgb`, `nv12`)
  - `size`: size of the input image as a list [H, W]
  - `crop`: enable runtime cropping of the input image
- `security`: Security policy for this input tensor. This field is only considered for secure models and can have the following values:
  - `any` (default): the input can be either in secure or non-secure memory
  - `secure`: the input must be in secure memory
  - `non-secure`: the input must be in non-secure memory

### `outputs` (pb)

Must contain one entry for each input of the network. Each entry has the following fields:

- `name` (pb): Name of the output in the network graph. For `tflite` and `onnx` models, this field is not required but can still be used to specify a different output layer than the default output of the network. This feature allows converting just a subset of a network without having to manually edit the source model. For `.pb` and `.onnx` models or when `name` is not specified, the outputs must be in the same order as they appear in the model.
- `dequantize`: The output of the network is internally dequantized and converted to `float`. This is more efficient than performing the conversion in software.
- `format`: Information about the type and organization of the data in the tensor. The content and meaning of this string are custom-defined. However, SyNAP `Classifier` and `Detector` postprocessors recognize by convention an initial format type optionally followed by one or more named attributes: `<format-type> [<key>=value]...`. All fields are separated by one or more spaces. No spaces are allowed between the key and the value. Example: `confidence_array class_index_base=0`. See the `Classifier` and `Detector` classes for a description of the specific attributes supported.
- `security`: Security policy for this output tensor. This field is only considered for secure models and can have the following values:
  - `secure-if-input-secure` (default): the output buffer must be in secure memory if at least one input is in secure memory
  - `any`: the output can be either in secure or non-secure memory

### `quantization` (q)

Quantization options are required when quantizing a model during conversion. They are not needed when importing a model that is already quantized. Quantization is only supported with the `npu` delegate.

- `data_type`: Data type used to quantize the network. The same data type is used for both activation data and weights. Available data types are:
  - `uint8` (default)
  - `int8`
  - `int16`
  - `float16`
- `scheme`: Select the quantization scheme. Available schemes are:
  - `default` (default)
  - `asymmetric_affine`
  - `dynamic_fixed_point`
  - `perchannel_symmetric_affine`
- `mode`: Select the quantization mode. Available modes are:
  - `standard` (default)
  - `full`
- `algorithm`: Select the quantization algorithm. Available algorithms are:
  - `standard` (default)
  - `kl_divergence`
  - `moving_average`
- `options`: Special options for fine-tuning the quantization in specific cases. Normally not needed.
- `dataset` (q): Quantization dataset(s), that is the set of input files to be used to quantize the model. In the case of multi-input networks, it is necessary to specify one dataset per input. Each dataset will consist of the sample files to be applied to the corresponding input during quantization. A sample file can be provided in one of two forms:
  1. As an image file (`.jpg` or `.png`)
  2. As a NumPy file (`.npy`)

Image files are suitable when the network inputs are images, that is 4-dimensional tensors (NCHW or NHWC). In this case, the `means` and `scale` values specified for the corresponding input are applied to each input image before it is used to quantize the model. Furthermore, each image is resized to fit the input tensor.

NumPy files can be used for all kinds of network inputs. A NumPy file shall contain an array of data with the same shape as the corresponding network input. In this case, it is not possible to specify a `means` and `scale` for the input; any preprocessing if needed has to be done when the NumPy file is generated.

To avoid having to manually list the files in the quantization dataset for each input, the quantization dataset is instead specified with a list of *glob expressions*, one glob expression for each input. This makes it very easy to specify as quantization dataset for one input the entire content of a directory, or a subset of it. For example, all the *jpeg* files in directory *samples* can be indicated with:

```sh
samples/*.jpg
```

Both relative and absolute paths can be used. Relative paths are considered relative to the location of the metafile itself. It is not possible to specify a mix of image and `.npy` files for the same input. For more information on the glob specification syntax, please refer to the Python documentation: https://docs.python.org/3/library/glob.html.

If the special keyword `random` is specified, a random data file will be automatically generated for this input. This option is useful for preliminary timing tests, but not for actual quantization.

If this field is not specified, quantization is disabled.

## Notes

- The fields marked `(pb)` are mandatory when converting `.pb` models.
- The fields marked `(q)` are mandatory when quantizing models.

The metafile also supports limited variable expansion: `${ENV:name}` anywhere in the metafile is replaced with the content of the environment variable *name* (or with the empty string if the variable doesn't exist). `${FILE:name}` in a format string is replaced with the content of the corresponding file (the file path is relative to that of the conversion metafile itself). This feature should be used sparingly as it makes the metafile not self-contained.