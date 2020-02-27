# Run Training
nohup darknet/darknet detector train obj-23f-b2.data yolov3-tiny-23f-b2-832.cfg ./backup/yolov3-tiny-23f-832_10000.weights &

# Calculate mAP (Average Precision)

darknet/darknet detector map obj-23f-b2.data yolov3-tiny-23f-b2-832.cfg backup/yolov3-tiny-23f-b2-832_last.weights -iou_thresh 0.75

# Run batch process on data then save it to json file
darknet/darknet detector test obj-23f-b2.data  yolov3-tiny-23f-b2-832.cfg  backup/yolov3-tiny-23f-b2-832_last.weights -iou_thresh 0.70 -ext_output -dont_show -out result_23f_70iou.json <  test_23f_info.txt 

# Run batch process on data then save it to text file
darknet/darknet detector test obj-23f-b2.data  yolov3-tiny-23f-b2-832.cfg  backup/yolov3-tiny-23f-b2-832_last.weights -dont_show -ext_output < test_23f_info.txt  > result_23f.txt
