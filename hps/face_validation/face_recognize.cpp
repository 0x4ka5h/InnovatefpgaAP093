#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/face.hpp>
#include "face_detection.h"
#include "face_trainer.h"
using namespace std;
using namespace cv;

int main(int argc, char *argv[]){
	if (argv[1]=="y"){
		trainer();
		cout << "training completed"<< endl;
	}
	cout << "loading model"<< endl;
	cv::Ptr<cv::face::LBPHFaceRecognizer> model = cv::face::LBPHFaceRecognizer::create();
	model->read("model.yml");
	cout << "successfully model loaded"<< endl;
	cv::VideoCapture source;
	source.open(0, CAP_V4L);
	cv::Mat frame;
	
	while (true){
		source >> frame;
		if (frame.empty()){
			break;
		}
		detector(frame);
		cv::Mat img = cv::imread("validate.png",0);
		
		
		int label=-1; double confidence=0;
		model->predict(img,label,confidence);
		
		cout << "confidence: "<<confidence << "  lable: " << label << endl;
		
		int k = waitKey(5);
		if(k == 27){
			destroyAllWindows();
			break;
		}
	}
}
