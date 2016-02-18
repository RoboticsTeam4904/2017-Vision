#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <dirent.h>
#define _USE_MATH_DEFINES
#include <math.h>

using namespace cv;
using namespace std;

Mat src, src_gray, subtracted;

int thresh = 200;
int max_thresh = 255;
int size_x = -1;
int size_y = -1;

int blob_size = 2;
int max_blob = 20;

struct rect_points {
    Point side_one;
    Point side_two;
    Point side_three;
    Point side_four;
};

bool gui = true;
bool detailedGUI = false;
bool test = false;
bool latest = false;
bool done = false;

void convex_callback(int, void* );
void blob_callback(int, void*);
void analyzeImage(Mat src);




int getdir (string dir, vector<string> &files) {
    DIR *dp;
    struct dirent *dirp;
    if ((dp = opendir(dir.c_str())) == NULL) {
        cout << "Error opening " << dir << endl;
        return -1;
    }

    while ((dirp = readdir(dp)) != NULL) {
        files.push_back(string(dirp->d_name));
    }
    closedir(dp);
    return 0;
}




int main(int argc, char** argv) {
    string image = "picture.jpg";

    if (argc == 1) {
        detailedGUI = true;
    }
    if (argc == 2) {
        if (strcmp(argv[1], "test") == 0) {
            gui = false;
            test = true;

            cout<<"*********************************"<<endl;
            cout<<"Testing mode"<<endl;
            cout<<"*********************************"<<endl<<endl;

        } else if (strcmp(argv[1], "latest")==0) {
            latest = true;
            image = "latest.jpg";
        } else {
            image = argv[1];
        }

    } else if (argc == 3) {

        if (strcmp(argv[1], "folder") == 0) {
            vector<string> files = vector<string>();
            string dir = argv[2];
            getdir(dir,files);
            cout<<"Reading directory"<<dir<<endl;

            for (unsigned int i = 0; i < files.size(); i++) {
                cout<<files[i]<<endl;
                if (files[i].length() < 4 || files[i].substr(files[i].length()-4, 4) != ".jpg") continue;
                string path = dir + files[i];

                src = imread(path, CV_LOAD_IMAGE_UNCHANGED);
                if (src.empty()) cout<<"error loading '"<<path<<"'"<<endl;
                analyzeImage(src);

                waitKey(0);
                done = true;
            }
        }

    }

    if (!done) {
        src = imread(image, CV_LOAD_IMAGE_UNCHANGED);
        if (src.empty()) {
            cout << "Error : Image cannot be loaded..!!" << endl;
            return -1;
        }
        analyzeImage(src);
    }

    return 0;
}


void analyzeImage(Mat src) {
    size_x = src.cols;
    size_y = src.rows;

    cvtColor( src, src_gray, CV_BGR2GRAY );
    blur( src_gray, src_gray, Size(3,3) );

    if (gui) namedWindow( "window", CV_WINDOW_AUTOSIZE );
    if (gui && detailedGUI) imshow("src_gray",src_gray);    
    if (gui) createTrackbar( " Threshold:", "window", &thresh, max_thresh, convex_callback );
    if (gui) createTrackbar( " BlobSize:", "window", &blob_size, max_blob, blob_callback );


    

    cvtColor( src, src_gray, CV_BGR2GRAY );
    blur( src_gray, src_gray, Size(3,3) ); 
    
    convex_callback(0,0);
    blob_callback(0,0);
    if (gui) waitKey(0);
}


void convex_callback(int, void* ) {
    Mat threshold_output, convex;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    threshold( src_gray, threshold_output, thresh, 255, THRESH_BINARY );
    if (gui && detailedGUI) imshow("threshold",threshold_output);
    findContours( threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

    vector<vector<Point> >hull( contours.size() );
    for( int i = 0; i < contours.size(); ++i ) {  convexHull( Mat(contours[i]), hull[i], false ); }

    convex = Mat::zeros( threshold_output.size(), CV_8UC1 );
    for (int i = 0; i<contours.size(); ++i) {
        drawContours(convex, hull, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() );
    }

    subtracted = Mat::zeros(convex.size(), CV_8UC1);

    if(convex.isContinuous()&&threshold_output.isContinuous()) {    uchar *p1, *p2, *p3;
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

    if (gui && detailedGUI) imshow("convex", convex);
    if (gui && detailedGUI) imshow("subtracted", subtracted);
    blob_callback(0,0);
}

void blob_callback(int, void*) {
    vector<vector<Point> > contours;
    vector<Point> poly;
    rect_points goal;
    vector<Vec4i> hierarchy;
    Mat blobed;
    Mat element = getStructuringElement(MORPH_ELLIPSE,Size( 2*blob_size + 1, 2*blob_size+1 ),Point( blob_size, blob_size ) );

    erode(subtracted, blobed, element);
    dilate(blobed, blobed, element);
    if (gui && detailedGUI) imshow("blobed", blobed);
    findContours(blobed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    Mat result=src.clone();// Mat::zeros(blobed.size(),CV_8UC3);

    for (int i = 0; i<contours.size(); ++i) {
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
        cout<<"angle"<<endl;
        //cout<<angle_measure(goal)<<endl;

    }

    if (gui) imshow("window",result);
}
