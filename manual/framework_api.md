# Framework API

## Network Class

The `Network` class is extremely simple, as shown in the picture below.

There are just two things that can be done with a network:

- Load a model by providing the compiled model in `.synap` format.
- Execute an inference.

A network also has an array of input tensors where the data to be processed is placed, and an array of output tensors which will contain the result(s) after each inference.

**Figure 5**: Network class

## Class `synaptics::synap::Network`

Load and execute a neural network on the NPU accelerator.

### Summary

| Function | Description |
|----------|-------------|
| `bool load_model(const std::string &model_file, const std::string &meta_file = "")` | Load model from file. |
| `bool load_model(const void *model_data, size_t model_size, const char *meta_data = nullptr)` | Load model from memory. |
| `bool predict()` | Run inference. |

### Public Functions

```cpp
bool load_model(const std::string &model_file, const std::string &meta_file = "")
```
- Load model.
- If another model was previously loaded, it is disposed of before loading the specified one.
- **Parameters**:
  - `model_file`: Path to `.synap` model file. Can also be the path to a legacy `.nb` model file.
  - `meta_file`: For legacy `.nb` models, must be the path to the model’s metadata file (JSON-formatted). In all other cases, must be an empty string.
- **Returns**: `true` if successful.

```cpp
bool load_model(const void *model_data, size_t model_size, const char *meta_data = nullptr)
```
- Load model.
- If another model was previously loaded, it is disposed of before loading the specified one.
- **Parameters**:
  - `model_data`: Model data, as from e.g. `fread()` of `model.synap`. The caller retains ownership of the model data and can delete them at the end of this method.
  - `model_size`: Model size in bytes.
  - `meta_data`: For legacy `.nb` models, must be the model’s metadata (JSON-formatted). In all other cases, must be `nullptr`.
- **Returns**: `true` if successful.

```cpp
bool predict()
```
- Run inference.
- Input data to be processed are read from input tensor(s). Inference results are generated in output tensor(s).
- **Returns**: `true` if successful, `false` if inference failed or network not correctly initialized.

### Public Members

- `Tensors inputs`
  - Collection of input tensors that can be accessed by index and iterated.

- `Tensors outputs`
  - Collection of output tensors that can be accessed by index and iterated.
