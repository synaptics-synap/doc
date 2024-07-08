============================================= ======= ======= ======= ======= ======= ======= ==
Model                                         Online  Online  Online  Online  Offline Offline   
                                              CPU     GPU     NPU     NPU     NPU     NPU       
                                              Infer   Infer   Init    Infer   Init    Infer     
============================================= ======= ======= ======= ======= ======= ======= ==
inception_v4_299_quant                         500.54           13502   17.80  100.79   19.59   
mobilenet_v1_0.25_224_quant                      3.37             166    0.81    2.61    0.77 \*
mobilenet_v2_1.0_224_quant                      18.60             854    1.85    6.13    1.79 \*
posenet_mobilenet_075_float                     34.44   61.78                                 \*
posenet_mobilenet_075_quant                     28.60             382    6.01    1.84    2.32   
yolov8s-pose                                                                    14.61   30.79 \*
yolov5m-640x480                                                  6606  113.88   54.11  118.82   
yolov5s-640x480                                                  2672   72.27   22.17   75.83   
yolov5s_face_640x480_onnx_mq                                                    13.00   31.88 \*
============================================= ======= ======= ======= ======= ======= ======= ==
