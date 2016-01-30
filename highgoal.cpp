#include <opencv2/highgui.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

Mat src, src_gray, subtracted, result;
int thresh = 100;
int max_thresh = 255;

int blob_size = 20;
int max_blob = 1000;

void convex_callback(int, void* );
void blob_callback(int, void*);

int main(int argc, char** argv)
{
    src = imread("picture.jpg", CV_LOAD_IMAGE_UNCHANGED);
    cvtColor( src, src_gray, CV_BGR2GRAY );
    blur( src_gray, src_gray, Size(3,3) );
    
    namedWindow( "window", CV_WINDOW_AUTOSIZE );
    
    createTrackbar( " Threshold:", "window", &thresh, max_thresh, convex_callback );
    createTrackbar( " BlobSize:", "window", &blob_size, max_blob, blob_callback );
    
    convex_callback(0,0);
    blob_callback(0,0);
    
}

void convex_callback(int, void* )
{
    Mat threshold_output, convex;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    
    threshold( src_gray, threshold_output, thresh, 255, THRESH_BINARY );
    findContours( threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    
    vector<vector<Point> >hull( contours.size() );
    for( int i = 0; i < contours.size(); ++i )
    {  convexHull( Mat(contours[i]), hull[i], false ); }
    
    convex = Mat::zeros( threshold_output.size(), CV_8UC3 );
    for (int i = 0; i<contours.size(); ++i)
         {
             drawContours(convex, contours, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() );
         }
         
    subtract(convex, threshold_output, subtracted);
}

void blob_callback(int, void*)
    {
        vector<vector<Point> > contours, poly;
        vector<Vec4i> hierarchy;
        Mat element = getStructuringElement(MORPH_ELLIPSE,Size( 2*blob_size + 1, 2*blob_size+1 ),Point( blob_size, blob_size ) );
        erode(subtracted, result, element);
        dilate(subtracted, result, element);
        
        findContours(result, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
        for (int i = 0; i<contours.size(); ++i)
             {
                 approxPolyDP(contours[i], poly[i], 3, true);
                 if (poly[i].size() == 4){   //If it is a rectangle
                     line(result, poly[i][0],poly[i][1], Scalar(255,0,0),5);
                     line(result, poly[i][1],poly[i][2], Scalar(255,0,0),5);
                     line(result, poly[i][2],poly[i][3], Scalar(255,0,0),5);
                     line(result, poly[i][3],poly[i][0], Scalar(255,0,0),5);
                     cout<<"vertex 1: ("<<poly[i][0].x<<","<<poly[i][0].y<<")"<<endl;
                     cout<<"vertex 2: ("<<poly[i][1].x<<","<<poly[i][1].y<<")"<<endl;
                     cout<<"vertex 3: ("<<poly[i][2].x<<","<<poly[i][2].y<<")"<<endl;
                     cout<<"vertex 4: ("<<poly[i][3].x<<","<<poly[i][3].y<<")"<<endl;
                 }
             }
             
        imshow("window",result);
    }
