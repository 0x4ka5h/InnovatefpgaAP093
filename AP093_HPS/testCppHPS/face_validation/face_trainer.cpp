#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <stdlib.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/face.hpp>
#include <opencv2/highgui.hpp>
#include "face_trainer.h"
using namespace std;
using namespace cv;

static void dbread(vector<Mat> &images,vector<int> &labels){
	vector<cv::String> fn;
	string path = "faces/";
	glob(path,fn,false);
	
	size_t count = fn.size();
	for(size_t i=0;i<count;i++){
		string s="";
		char s_='/';
		size_t j=fn[i].rfind(s_,fn[i].length());
		if(j!=string::npos){
			s=(fn[i].substr(j+1,fn[i].length()-j-6));
		}
		images.push_back(cv::imread(fn[i],0));
		labels.push_back(atoi(s.c_str()));
	}
}

void trainer(){
	vector<cv::Mat> images;
	vector<int> labels;
	dbread(images,labels);
	
	cout << "training begins" << endl;
	
	cv::Ptr<cv::face::LBPHFaceRecognizer> model = cv::face::LBPHFaceRecognizer::create();
	model->train(images,labels);
	
	model->save("model.yml");
	cout << "\nTraining completed" << endl;
}
