#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#define _USE_MATH_DEFINES
#include <math.h>

using namespace cv;
using namespace std;

Mat src, src_gray, subtracted;
int thresh = 200;
int max_thresh = 255;
int size_x = -1;
int size_y = -1;

int blob_size = 5;
int max_blob = 20;

struct rect_points {
  Point side_one;
  Point side_two;
  Point side_three;
  Point side_four;
};

void convex_callback(int, void* );
void blob_callback(int, void*);
float angle_measure(rect_points);
float rotationX(rect_points);
float rotationY(rect_points);


int main(int argc, char** argv)
{
    src = imread("picture.jpg", CV_LOAD_IMAGE_UNCHANGED);
        if (src.empty()) //check whether the image is loaded or not
     {
          cout << "Error : Image cannot be loaded..!!" << endl;
          //system("pause"); //wait for a key press
          return -1;
     }
    size_x = src.cols;
    size_y = src.rows;
    cvtColor( src, src_gray, CV_BGR2GRAY );
    blur( src_gray, src_gray, Size(3,3) );
    //namedWindow( "window", CV_WINDOW_AUTOSIZE );
    //imshow ("src_gray",src_gray);
    //createTrackbar( " Threshold:", "window", &thresh, max_thresh, convex_callback );
    //createTrackbar( " BlobSize:", "window", &blob_size, max_blob, blob_callback );

     convex_callback(0,0);
     blob_callback(0,0);

    //waitKey(0);
}

void convex_callback(int, void* )
{
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
        rect_points goal;
        vector<Vec4i> hierarchy;
        Mat blobed;
        Mat element = getStructuringElement(MORPH_ELLIPSE,Size( 2*blob_size + 1, 2*blob_size+1 ),Point( blob_size, blob_size ) );

        erode(subtracted, blobed, element);
        dilate(blobed, blobed, element);
        //imshow("blobed", blobed);
        findContours(blobed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
        Mat result=Mat::zeros(blobed.size(),CV_8UC3);

        for (int i = 0; i<contours.size(); ++i)
             {
                 approxPolyDP(Mat(contours[i]), poly, 3, true);
                 goal.side_one = poly[0];
                 goal.side_two = poly[1];
                 goal.side_three = poly[2];
                 goal.side_four = poly[3];

                 line(result, goal.side_one,goal.side_two, Scalar(255,0,0),5);
                 line(result, goal.side_two,goal.side_three, Scalar(255,0,0),5);
                 line(result, goal.side_three,goal.side_four, Scalar(255,0,0),5);
                 line(result, goal.side_four,goal.side_one, Scalar(255,0,0),5);
                 cout<<"vertex 1: ("<<goal.side_one.x<<","<<goal.side_one.y<<")"<<endl;
                 cout<<"vertex 2: ("<<goal.side_two.x<<","<<goal.side_two.y<<")"<<endl;
                 cout<<"vertex 3: ("<<goal.side_three.x<<","<<goal.side_three.y<<")"<<endl;
                 cout<<"vertex 4: ("<<goal.side_four.x<<","<<goal.side_four.y<<")"<<endl;
                 cout<<angle_measure(goal)<<endl;

             }

        //imshow("window",result);
    }

float angle_measure(rect_points goal)
    {
      float anglea;
      float angleb;
      anglea = atan((goal.side_three.y-goal.side_two.y)/(goal.side_two.x-goal.side_three.x))*(180/M_PI);
      angleb = atan((goal.side_four.y-goal.side_one.y)/(goal.side_four.x-goal.side_one.x))*(180/M_PI);
      return angleb-anglea;
    }
float rotationX(rect_points goal)
  {
    float xdiff;
    xdiff = (size_x/2)-(goal.side_two.x+goal.side_one.x+goal.side_three.x+goal.side_four.x)/4;
    return xdiff;
  }
float rotationY(rect_points goal)
    {
      float ydiff;
      ydiff = (size_y/2)-(goal.side_two.y+goal.side_one.y+goal.side_three.y+goal.side_four.y)/4;
      return ydiff;
    }
