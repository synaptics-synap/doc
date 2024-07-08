============================================= ======= ======= ======= ======= ======= ======= ==
Model                                         Online  Online  Online  Online  Offline Offline   
                                              CPU     GPU     NPU     NPU     NPU     NPU       
                                              Infer   Infer   Init    Infer   Init    Infer     
============================================= ======= ======= ======= ======= ======= ======= ==
deeplab_v3_plus_quant                          231.76            4090   60.73    7.68   59.81   
dped_quant                                     335.63            1019    8.93    4.74    8.82   
inception_v3_float                             370.95  436.74                                   
inception_v3_quant                             267.95            7210    9.47   59.55   10.22   
mobilenet_v2_b4_quant                           53.54             875   12.50   11.53   13.63   
mobilenet_v2_float                              20.84   35.40                                   
mobilenet_v2_quant                              18.72             886    2.02    9.27    1.98   
mobilenet_v3_quant                              51.89            1089    9.76   13.15   10.15   
pynet_quant                                    976.61            3175   18.56   24.45   19.30   
srgan_quant                                   1513.86            3517   54.58   14.72   56.95   
unet_quant                                     265.51             487    9.34    7.73   14.80   
vgg_quant                                     1641.18            2177   29.77   10.74   30.07   
============================================= ======= ======= ======= ======= ======= ======= ==
