#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <dirent.h>

using namespace cv;
using namespace std;

Mat src, src_gray, subtracted;

int thresh = 200;
int max_thresh = 255;

int blob_size = 2;
int max_blob = 20;

void convex_callback(int, void* );
void blob_callback(int, void*);
void analyzeImage(Mat src);

int getdir (string dir, vector<string> &files)
{
DIR *dp;
struct dirent *dirp;
if((dp = opendir(dir.c_str())) == NULL) {
cout << "Error(" << errno << ") opening " << dir << endl;
return errno;
}

while ((dirp = readdir(dp)) != NULL) {
files.push_back(string(dirp->d_name));
}
closedir(dp);
return 0;
}


int main(int argc, char* argv[]) {

	
		cout<<"argc: "<<argc<<endl;
	if (argc == 2) {
		cout<<"using '"<<argv[1]<<"' as source"<<endl<<endl;
		src = imread(argv[1], CV_LOAD_IMAGE_UNCHANGED);
	} else {
		


     vector<string> files = vector<string>();
		string dir = "pics/";
     getdir(dir,files);
     cout<<"reading"<<endl;

	for (unsigned int i = 0; i < files.size(); i++) {

		
		cout<<files[i]<<endl;
		if (files[i].length() < 4 || files[i].substr(files[i].length()-4, 4) != ".jpg") continue;
		string path = dir + files[i];

		src = imread(path, CV_LOAD_IMAGE_UNCHANGED);
		if (src.empty()) cout<<"error loading '"<<path<<"'"<<endl;
     	analyzeImage(src);
     	
     	waitKey(0);
     }
 	}

	return 0;
}

void analyzeImage(Mat src) {
    cvtColor( src, src_gray, CV_BGR2GRAY );
    blur( src_gray, src_gray, Size(3,3) ); 
    
     convex_callback(0,0);
     blob_callback(0,0);    
}

void convex_callback(int, void* ) {
    Mat threshold_output, convex;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    
    threshold( src_gray, threshold_output, thresh, 255, THRESH_BINARY );
    //imshow("threshold",threshold_output);
    findContours( threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    
    vector<vector<Point> >hull( contours.size() );
    for( int i = 0; i < contours.size(); ++i )
    {  convexHull( Mat(contours[i]), hull[i], false ); }
    
    convex = Mat::zeros( threshold_output.size(), CV_8UC1 );
    for (int i = 0; i<contours.size(); ++i)
         {
             drawContours(convex, hull, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() );
         }
         
    subtracted = Mat::zeros(convex.size(), CV_8UC1);

    if(convex.isContinuous()&&threshold_output.isContinuous())
    {    uchar *p1, *p2, *p3;
         p1 = convex.ptr<uchar>(0);  
         p2 = threshold_output.ptr<uchar>(0);
         p3 = subtracted.ptr<uchar>(0);
         for (int i=0; i<convex.rows*convex.cols; ++i){
             if (*p2 != 0){
                 *p3 = 0;
             }
             else if(*p1 != 0){
                 *p3 = 255;
             }
             p1++;
             p2++;
             p3++;
         }

    }
   // subtract(convex, threshold_output, subtracted);
    //imshow("convex", convex);
    //imshow("subtracted", subtracted);
    blob_callback(0,0);
}

void blob_callback(int, void*)
    {   vector<vector<Point> > contours;
    	vector<Point> poly;
        vector<Vec4i> hierarchy;
        Mat blobed;
        Mat element = getStructuringElement(MORPH_ELLIPSE,Size( 2*blob_size + 1, 2*blob_size+1 ),Point( blob_size, blob_size ) );

        erode(subtracted, blobed, element);
        dilate(blobed, blobed, element);
        //imshow("blobed", blobed);
        findContours(blobed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
        Mat result=src.clone();// Mat::zeros(blobed.size(),CV_8UC3);

        for (int i = 0; i<contours.size(); ++i)
             {
                 approxPolyDP(Mat(contours[i]), poly, 3, true);
                 if (poly.size() == 4){   //If it is a rectangle
                     line(result, poly[0],poly[1], Scalar(255,0,0),5);
                     line(result, poly[1],poly[2], Scalar(255,0,0),5);
                     line(result, poly[2],poly[3], Scalar(255,0,0),5);
                     line(result, poly[3],poly[0], Scalar(255,0,0),5);
                     cout<<"vertex 1: ("<<poly[0].x<<","<<poly[0].y<<")"<<endl;
                     cout<<"vertex 2: ("<<poly[1].x<<","<<poly[1].y<<")"<<endl;
                     cout<<"vertex 3: ("<<poly[2].x<<","<<poly[2].y<<")"<<endl;
                     cout<<"vertex 4: ("<<poly[3].x<<","<<poly[3].y<<")"<<endl;
                 }
             }
             
        imshow("window",result);
    }
