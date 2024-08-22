# NPU Operators

This section summarizes neural network operators supported by the SyNAP VS6x0/SL16x0 class of NPUs and accompanying software stack. For each operator type, the supported tensor types and execution engines are also documented. Designing networks that maximize the use of operators executed in the NN core will provide the best performance.

## 

### Execution Engines

| Acronym | Description                      |
|---------|----------------------------------|
| NN      | Neural Network Engine            |
| PPU     | Parallel Processing Unit         |
| TP      | Tensor Processor                 |

### Tensor Types

| Acronym | Description                      |
|---------|----------------------------------|
| asym-u8 | asymmetric affine uint8          |
| asym-i8 | asymmetric affine int8           |
| pc-sym-i8 | per channel symmetric int8     |
| fp32    | floating point 32 bits           |
| fp16    | floating point 16 bits           |
| h       | half                             |
| int16   | int16                            |
| int32   | int32                            |

> **Note:** 
> int16 dynamic fixed point convolution is supported by the NN Engine in their multiplication. Other layers follow the tables; if asym-u8 is not available in the NN column, int16 is also not available.

## Basic Operations


| Operator            | Input       | Kernel      | Output    | NN          | TP          | PPU         |
|---------------------|-------------|-------------|-----------|-------------|-------------|-------------|
| CONV2D              | asym-u8     | asym-u8     | asym-u8   | ✔           |             |             |
|                     | asym-i8     | pc-sym-i8   | asym-i8   | ✔           |             | ✔           |
|                     | fp32        | fp32        | fp32      |             |             | ✔           |
|                     | fp16        | fp16        | fp16      |             |             | ✔           |
| CONV1D              | asym-u8     | asym-u8     | asym-u8   | ✔           |             |             |
|                     | asym-i8     | pc-sym-i8   | asym-i8   | ✔           |             | ✔           |
|                     | fp32        | fp32        | fp32      |             |             | ✔           |
|                     | fp16        | fp16        | fp16      |             |             | ✔           |
| DECONVOLUTION       | asym-u8     | asym-u8     | asym-u8   | ✔           |             |             |
|                     | asym-i8     | pc-sym-i8   | asym-i8   | ✔           |             | ✔           |
|                     | fp32        | fp32        | fp32      |             |             | ✔           |
|                     | fp16        | fp16        | fp16      |             |             | ✔           |
| DECONVOLUTION1D     | asym-u8     | asym-u8     | asym-u8   | ✔           |             |             |
|                     | asym-i8     | pc-sym-i8   | asym-i8   | ✔           |             | ✔           |
|                     | fp32        | fp32        | fp32      |             |             | ✔           |
|                     | fp16        | fp16        | fp16      |             |             | ✔           |
| GROUPED_CONV2D      | asym-u8     | asym-u8     | asym-u8   | ✔           |             |             |
|                     | asym-i8     | pc-sym-i8   | asym-i8   | ✔           |             | ✔           |
|                     | fp32        | fp32        | fp32      |             |             | ✔           |
|                     | fp16        | fp16        | fp16      |             |             | ✔           |
| FULLY_CONNECTED     | asym-u8     | asym-u8     | asym-u8   |             | ✔           |             |
|                     | asym-i8     | pc-sym-i8   | asym-i8   |             | ✔           |             |
|                     | fp32        | fp32        | fp32      |             |             | ✔           |


> **Note:** 
> Convolutions are executed in the NN engine only if they satisfy the following conditions: `**stride == 1**, **kernel_size <= 15x15**, **dilation size + kernel size <= 15x15**`. If any of these conditions are not satisfied, the convolution will require support of the TP core and will run considerably slower.

## Activation Operations


| Operator      | Input    | Output    | NN            | TP            | PPU           |
|---------------|----------|-----------|---------------|---------------|---------------|
| ELU           | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               | ✔             | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| HARD_SIGMOID  | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               | ✔             | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| SWISH         | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| LEAKY_RELU    | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| PRELU         | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| RELU          | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| RELUN         | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| RSQRT         | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| SIGMOID       | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| SOFTRELU      | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| SQRT          | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| TANH          | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| ABS           | asym-u8  | asym-u8   |               | ✔             |               |
|               | asym-i8  | asym-i8   |               | ✔             |               |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             |               |
| CLIP          | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| EXP           | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| LOG           | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| NEG           | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| MISH          | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| SOFTMAX       | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| LOG_SOFTMAX   | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| SQUARE        | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| SIN           | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| LINEAR        | asym-u8  | asym-u8   |               |               | ✔             |
|               | asym-i8  | asym-i8   |               |               | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               |               | ✔             |
| ERF           | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |
| GELU          | asym-u8  | asym-u8   |               | ✔             | ✔             |
|               | asym-i8  | asym-i8   |               | ✔             | ✔             |
|               | fp32     | fp32      |               |               | ✔             |
|               | fp16     | fp16      |               | ✔             | ✔             |

## Elementwise Operations

| Operator      | Input    | Output    | NN              | TP              | PPU             |
|---------------|----------|-----------|-----------------|-----------------|-----------------|
| ADD           | asym-u8  | asym-u8   | ✔               |                 |                 |
|               | asym-i8  | asym-i8   | ✔               |                 |                 |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| SUBTRACT      | asym-u8  | asym-u8   | ✔               |                 |                 |
|               | asym-i8  | asym-i8   | ✔               |                 |                 |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| MULTIPLY      | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| DIVIDE        | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| MAXIMUM       | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| MINIMUM       | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| POW           | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| FLOORDIV      | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| MATRIXMUL     | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
| RELATIONAL_OPS| asym-u8  | bool8     |                 |                 | ✔               |
|               | asym-i8  | bool8     |                 |                 | ✔               |
|               | fp32     | bool8     |                 |                 | ✔               |
|               | fp16     | bool8     |                 |                 | ✔               |
|               | bool8    | bool8     |                 |                 | ✔               |
| LOGICAL_OPS   | bool8    | bool8     |                 |                 | ✔               |
| LOGICAL_NOT   | bool8    | bool8     |                 |                 | ✔               |
| SELECT        | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |
|               | bool8    | bool8     |                 |                 | ✔               |
| ADDN          | asym-u8  | asym-u8   |                 |                 | ✔               |
|               | asym-i8  | asym-i8   |                 |                 | ✔               |
|               | fp32     | fp32      |                 |                 | ✔               |
|               | fp16     | fp16      |                 |                 | ✔               |

## Normalization Operations

| Operator          | Input  | Output    | NN                | TP                | PPU               |
|-------------------|--------|-----------|-------------------|-------------------|-------------------|
| BATCH_NORM        | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |
| LRN2              | asym-u8| asym-u8   |                   | ✔                 |                   |
|                   | asym-i8| asym-i8   |                   | ✔                 |                   |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   | ✔                 |                   |
| L2_NORMALIZE      | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |
| LAYER_NORM        | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |
| INSTANCE_NORM     | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |
| BATCHNORM_SINGLE  | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |
| MOMENTS           | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |
| GROUP_NORM        | asym-u8| asym-u8   |                   |                   | ✔                 |
|                   | asym-i8| asym-i8   |                   |                   | ✔                 |
|                   | fp32   | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16      |                   |                   | ✔                 |

## Reshape Operations


| Operator                 | Input | Output  | NN                       | TP                       | PPU                      |
|--------------------------|-------|---------|--------------------------|--------------------------|--------------------------|
| EXPAND_BROADCAST         | asym-u8| asym-u8|                          |                          | ✔                        |
|                          | asym-i8| asym-i8|                          |                          | ✔                        |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          |                          | ✔                        |
| SLICE                    | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| SPLIT                    | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| CONCAT                   | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| STACK                    | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| UNSTACK                  | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| RESHAPE                  | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| SQUEEZE                  | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| PERMUTE                  | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| REORG                    | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| SPACE2DEPTH              | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| DEPTH2SPACE              | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
|                          | bool8 | bool8   |                          |                          |                          |
| BATCH2SPACE              | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| SPACE2BATCH              | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| PAD                      | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| REVERSE                  | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| STRIDED_SLICE            | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |
| REDUCE                   | asym-u8| asym-u8|                          |                          | ✔                        |
|                          | asym-i8| asym-i8|                          |                          | ✔                        |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          |                          | ✔                        |
| ARGMAX                   | asym-u8| asym-u8 / int16 / int32|           |                          | ✔                        |
|                          | asym-i8| asym-u8 / int16 / int32|           |                          | ✔                        |
|                          | fp32  | int32   |                          |                          | ✔                        |
|                          | fp16  | asym-u8 / int16 / int32|           |                          | ✔                        |
| ARGMIN                   | asym-u8| asym-u8 / int16 / int32|           |                          | ✔                        |
|                          | asym-i8| asym-u8 / int16 / int32|           |                          | ✔                        |
|                          | fp32  | int32   |                          |                          | ✔                        |
|                          | fp16  | asym-u8 / int16 / int32|           |                          | ✔                        |
| SHUFFLECHANNEL           | asym-u8| asym-u8|                          | ✔                        |                          |
|                          | asym-i8| asym-i8|                          | ✔                        |                          |
|                          | fp32  | fp32    |                          |                          | ✔                        |
|                          | fp16  | fp16    |                          | ✔                        |                          |

## RNN Operations


| Operator          | Input  | Kernel   | Output    | NN                | TP                | PPU               |
|-------------------|--------|----------|-----------|-------------------|-------------------|-------------------|
| LSTMUNIT_OVXLIB   | asym-u8| asym-u8  | asym-u8   |                   | ✔                 | ✔                 |
|                   | asym-i8| pc-sym-i8| asym-i8   |                   | ✔                 | ✔                 |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   | ✔                 | ✔                 |
| CONV2D_LSTM       | asym-u8| asym-u8  | asym-u8   | ✔                 |                   |                   |
|                   | asym-i8| pc-sym-i8| asym-i8   | ✔                 |                   |                   |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   |                   | ✔                 |
| CONV2D_LSTM_CELL  | asym-u8| asym-u8  | asym-u8   | ✔                 |                   |                   |
|                   | asym-i8| pc-sym-i8| asym-i8   | ✔                 |                   |                   |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   |                   | ✔                 |
| LSTM_OVXLIB       | asym-u8| asym-u8  | asym-u8   |                   | ✔                 | ✔                 |
|                   | asym-i8| pc-sym-i8| asym-i8   |                   | ✔                 | ✔                 |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   | ✔                 | ✔                 |
| GRUCELL_OVXLIB    | asym-u8| asym-u8  | asym-u8   |                   | ✔                 | ✔                 |
|                   | asym-i8| pc-sym-i8| asym-i8   |                   | ✔                 | ✔                 |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   | ✔                 | ✔                 |
| GRU_OVXLIB        | asym-u8| asym-u8  | asym-u8   |                   | ✔                 | ✔                 |
|                   | asym-i8| pc-sym-i8| asym-i8   |                   | ✔                 | ✔                 |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   | ✔                 | ✔                 |
| SVDF              | asym-u8| asym-u8  | asym-u8   |                   | ✔                 | ✔                 |
|                   | asym-i8| pc-sym-i8| asym-i8   |                   | ✔                 | ✔                 |
|                   | fp32   | fp32     | fp32      |                   |                   | ✔                 |
|                   | fp16   | fp16     | fp16      |                   | ✔                 | ✔                 |

## Pooling Operations

| Operator        | Input  | Output | NN              | TP              | PPU             |
|-----------------|--------|--------|-----------------|-----------------|-----------------|
| POOL            | asym-u8| asym-u8| ✔               | ✔               |                 |
|                 | asym-i8| asym-i8| ✔               | ✔               |                 |
|                 | fp32   | fp32   |                 |                 | ✔               |
|                 | fp16   | fp16   |                 | ✔               |                 |
| ROI_POOL        | asym-u8| asym-u8|                 | ✔               | ✔               |
|                 | asym-i8| asym-i8|                 | ✔               | ✔               |
|                 | fp32   | fp32   |                 |                 | ✔               |
|                 | fp16   | fp16   |                 | ✔               | ✔               |
| POOLWITHARGMAX  | asym-u8| asym-u8|                 |                 | ✔               |
|                 | asym-i8| asym-i8|                 |                 | ✔               |
|                 | fp32   | fp32   |                 |                 | ✔               |
|                 | fp16   | fp16   |                 |                 | ✔               |
| UPSAMPLE        | asym-u8| asym-u8|                 |                 | ✔               |
|                 | asym-i8| asym-i8|                 |                 | ✔               |
|                 | fp32   | fp32   |                 |                 | ✔               |
|                 | fp16   | fp16   |                 |                 | ✔               |

## Miscellaneous Operations

| Operator          | Input| Output| NN                | TP                | PPU               |
|-------------------|------|-------|-------------------|-------------------|-------------------|
| PROPOSAL          | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| VARIABLE          | asym-u8| asym-u8|               | ✔                 |                   |
|                   | asym-i8| asym-i8|               | ✔                 |                   |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   | ✔                 |                   |
| DROPOUT           | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| RESIZE            | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| DATACONVERT       | asym-u8| asym-u8|               | ✔                 |                   |
|                   | asym-i8| asym-i8|               | ✔                 |                   |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   | ✔                 |                   |
| FLOOR             | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| EMBEDDING_LOOKUP  | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| GATHER            | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| GATHER_ND         | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| SCATTER_ND        | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| GATHER_ND_UPDATE  | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| TILE              | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| ELTWISEMAX        | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| SIGNAL_FRAME      | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| CONCATSHIFT       | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| UPSAMPLESCALE     | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| ROUND             | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| CEIL              | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| SEQUENCE_MASK     | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| REPEAT            | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| ONE_HOT           | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |
| CAST              | asym-u8| asym-u8|               |                   | ✔                 |
|                   | asym-i8| asym-i8|               |                   | ✔                 |
|                   | fp32   | fp32  |                   |                   | ✔                 |
|                   | fp16   | fp16  |                   |                   | ✔                 |