============================================= ======= ======= ======= ======= ======= ======= ==
Model                                         Online  Online  Online  Online  Offline Offline   
                                              CPU     GPU     NPU     NPU     NPU     NPU       
                                              Infer   Infer   Init    Infer   Init    Infer     
============================================= ======= ======= ======= ======= ======= ======= ==
crnn_float                                     240.53  217.89                                   
crnn_quant                                     113.52           40641   22.54  217.19   23.03   
deeplab_v3_plus_float                         1181.26 1447.74                                   
deeplab_v3_plus_quant                          674.10            2381   97.98   16.68  103.05   
dped_float                                    4043.67 2353.72                                   
dped_instance_float                           2236.11 1386.78                                   
dped_instance_quant                           3422.17             288  229.41    5.43  953.44   
dped_quant                                    2249.53            3266  196.30   18.70  199.15   
efficientnet_b4_float                          432.00  579.98                                   
efficientnet_b4_quant                          228.86            9649  162.06   54.48  166.33   
esrgan_float                                  1445.08 1522.63                                   
esrgan_quant                                   770.69            2119   93.78    5.08  101.56   
imdn_float                                    2553.12 2382.78                                   
imdn_quant                                    1350.97            3215  165.92    8.63  155.46   
inception_v3_float                             371.39  437.60                                   
inception_v3_quant                             221.61            7254   10.26   76.98   11.38   
mobilenet_v2_b8_float                          152.22  203.15                                   
mobilenet_v2_b8_quant                           91.44             889   25.91   14.69   27.18   
mobilenet_v2_float                              20.98   36.08                                   
mobilenet_v2_quant                              12.28             968    2.11   10.04    2.07   
mobilenet_v3_b4_float                          351.62  461.38                                   
mobilenet_v3_b4_quant                          359.39            1497   97.86   20.36  101.09   
mobilenet_v3_float                              91.33  114.77                                   
mobilenet_v3_quant                              97.05            1706   19.82   15.14   20.92   
mv3_depth_float                                132.65  194.37                                   
mv3_depth_quant                                218.06            1513   71.09   15.74   90.96   
punet_float                                   2612.87 1796.33                                   
punet_quant                                   1660.59            2019  155.60   14.06  149.79   
pynet_float                                   2836.85 1620.06                                   
pynet_quant                                   2100.18            3441  137.39   15.80  135.94   
resnet_float                                     0.10    2.86                                   
resnet_quant                                     0.41             132    0.13    3.95    0.12   
srgan_float                                   6192.96 2921.47                                   
srgan_quant                                   4220.89           12224  200.90   29.85  208.23   
unet_float                                    2909.00 2132.16                                   
unet_quant                                    1710.41             775   69.08   19.11   95.29   
vsr_float                                      820.35  974.12                                   
vsr_quant                                      580.30            2124  155.28   20.45  133.86   
xlsr_float                                     518.61  532.46                                   
xlsr_quant                                     470.63            1700   36.20    3.93   31.38   
yolo_v4_tiny_float                             187.81  157.75                                   
yolo_v4_tiny_quant                             311.65            1406    6.62    4.69    6.03   
============================================= ======= ======= ======= ======= ======= ======= ==
