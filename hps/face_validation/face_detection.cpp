#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/face.hpp>
#include <opencv2/highgui.hpp>
#include "brighten.h"
#include "face_detection.h"

using namespace cv;

using namespace std;

const size_t inWidth = 300;
const size_t inHeight = 300;
const double inScaleFactor = 1.0;
const float confidenceThreshold = 0.7;
const cv::Scalar meanVal(104.0, 177.0, 123.0);

const std::string caffeConfigFile = "deploy.prototxt";
const std::string caffeWeightFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel";

cv::dnn::Net net = cv::dnn::readNetFromCaffe(caffeConfigFile, caffeWeightFile);





int detectFaceOpenCVDNN(cv::dnn::Net net_, Mat &frameOpenCVDNN,int choice=0){
	int frameHeight = frameOpenCVDNN.rows;
	int frameWidth = frameOpenCVDNN.cols;
	int x1,x2,y1,y2;
	cv::Mat inputBlob;
	inputBlob = cv::dnn::blobFromImage(frameOpenCVDNN, inScaleFactor, cv::Size(inWidth, inHeight), meanVal, false, false);
	net_.setInput(inputBlob, "data");
	cv::Mat detection = net_.forward("detection_out");

	cv::Mat detectionMat(detection.size[2], detection.size[3], CV_32F, detection.ptr<float>());

	for(int i = 0; i < detectionMat.rows; i++){
		float confidence = detectionMat.at<float>(i, 2);

		if(confidence > confidenceThreshold){
			int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameWidth);
			int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameHeight);
			int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameWidth);
			int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameHeight);

			cv::rectangle(frameOpenCVDNN, cv::Point(x1, y1), cv::Point(x2, y2), cv::Scalar(0, 255, 0),2, 4);
		}
		cv::Mat imgRoi = frameOpenCVDNN(cv::Rect(x1,y1,x2,y2));
		cv::imwrite("validate.png", imgRoi);
		return choice;
	}
	return choice+1;
}



void detector(cv::Mat &frame){

	// force CPU backend for OpenCV 3.x as CUDA backend is not supported there
	//                           net.setPreferableBackend(DNN_BACKEND_DEFAULT);
	net.setPreferableBackend(DNN_TARGET_CPU);
	int check = detectFaceOpenCVDNN(net, frame);
	if (check == 1){
		cv::Mat resultant_img = brighten(frame);
		check = detectFaceOpenCVDNN(net, resultant_img);
	}
	
}

