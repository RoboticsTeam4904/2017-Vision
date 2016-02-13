#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>

using namespace cv;
using namespace std;

Mat src, src_gray, subtracted;
int thresh = 200;
int max_thresh = 255;

int blob_size = 5;
int max_blob = 20;

void convex_callback(int, void* );
void blob_callback(int, void*);

struct rectangle {
  Vector side_one;
  Vector side_two;
  Vector side_three;
  Vector side_four;

}

int main(int argc, char** argv)
{
    src = imread("picture.jpg", CV_LOAD_IMAGE_UNCHANGED);
        if (src.empty()) //check whether the image is loaded or not
     {
          cout << "Error : Image cannot be loaded..!!" << endl;
          //system("pause"); //wait for a key press
          return -1;
     }

    cvtColor( src, src_gray, CV_BGR2GRAY );
    blur( src_gray, src_gray, Size(3,3) );
    namedWindow( "window", CV_WINDOW_AUTOSIZE );
    imshow ("src_gray",src_gray);
    createTrackbar( " Threshold:", "window", &thresh, max_thresh, convex_callback );
    createTrackbar( " BlobSize:", "window", &blob_size, max_blob, blob_callback );

     convex_callback(0,0);
     blob_callback(0,0);

    waitKey(0);
}

void convex_callback(int, void* )
{
    Mat threshold_output, convex;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    threshold( src_gray, threshold_output, thresh, 255, THRESH_BINARY );
    imshow("threshold",threshold_output);
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
    imshow("convex", convex);
    imshow("subtracted", subtracted);
    blob_callback(0,0);
}

void blob_callback(int, void*)
    {   vector<vector<Point> > contours;
    	rectangle poly;
        vector<Vec4i> hierarchy;
        Mat blobed;
        Mat element = getStructuringElement(MORPH_ELLIPSE,Size( 2*blob_size + 1, 2*blob_size+1 ),Point( blob_size, blob_size ) );

        erode(subtracted, blobed, element);
        dilate(blobed, blobed, element);
        imshow("blobed", blobed);
        findContours(blobed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
        Mat result=Mat::zeros(blobed.size(),CV_8UC3);

        for (int i = 0; i<contours.size(); ++i)
             {
                 approxPolyDP(Mat(contours[i]), poly, 3, true);

                 line(result, poly.side_one,poly.side_two, Scalar(255,0,0),5);
                 line(result, poly.side_two,poly.side_three, Scalar(255,0,0),5);
                 line(result, poly.side_three,poly.side_four, Scalar(255,0,0),5);
                 line(result, poly.side_four,poly.side_one2, Scalar(255,0,0),5);
                 cout<<"vertex 1: ("<<poly.side_one.x<<","<<poly.side_one.y<<")"<<endl;
                 cout<<"vertex 2: ("<<poly.side_two.x<<","<<poly.side_two.y<<")"<<endl;
                 cout<<"vertex 3: ("<<poly.side_three.x<<","<<poly.side_three.y<<")"<<endl;
                 cout<<"vertex 4: ("<<poly.side_four.x<<","<<poly.side_four.y<<")"<<endl;

             }

        imshow("window",result);
    }

void angle_measure(int, void*)
    {

    }
