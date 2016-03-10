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

int thresh = 210;
int max_thresh = 255;
int size_x = -1;
int size_y = -1;

int blob_size = 5;
int max_blob = 20; //used only in gui

struct rect_points {
	Point side_one;
	Point side_two;
	Point side_three;
	Point side_four;
};

bool gui = false; //turn on for debugging
bool detailedGUI = false;
bool test = false;
bool latest = false;
bool done = false;
bool existingGoal = false;

void convex_callback(int, void* );
void blob_callback(int, void*);
void analyzeImage(Mat src);

pair<float,float> off_angle();

float mountAngleX = 0.0;
float mountAngleY = 45.0 * M_PI / 180;
int nativeResX = 2592;
int nativeResY = 1944;
float nativeAngleX = 53.5 * M_PI / 180;
float nativeAngleY = 41.41 * M_PI / 180;
// All distances are in milimeters
float shiftX = 336.55; // 13.25 inches
float shiftY = 57.15; // 2.5 inches
float goalHeight = 2292.35; // 7.5 feet
float cameraHeight = 296.0; // 296 milimeters
float milimetersPerInch = 25.4;

rect_points goal;
vector<vector<Point> > contours;

int getdir(string dir, vector<string> &files) {
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
	string image = "latest.jpg";

	if (argc == 1) {
		detailedGUI = true;
	} else if (argc == 2) {
		if (strcmp(argv[1], "test") == 0) {
			gui = false;
			test = true;

			cout << "*********************************" << endl;
			cout << "Testing mode" << endl;
			cout << "*********************************" << endl << endl;
		} else if (strcmp(argv[1], "latest") == 0) {
			latest = true;
			gui = false;
			image = "latest.jpg";
		} else {
			image = argv[1];
		}
	} else if (argc == 3) {
		if (strcmp(argv[1], "folder") == 0) {
			vector<string> files = vector<string>();
			string dir = argv[2];
			getdir(dir, files);
			cout << "Reading directory" << dir << endl;

			for (unsigned int i = 0; i < files.size(); i++) {
				cout << files[i] << endl;
				if (files[i].length() < 4 || files[i].substr(files[i].length() - 4, 4) != ".jpg") continue;
				string path = dir + files[i];

				src = imread(path, CV_LOAD_IMAGE_UNCHANGED);
				if (src.empty()) cout << "error loading '" << path << "'" << endl;
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
	float offAngle = 0.0;
	float distance = 0.0;
	size_x = src.cols;
	size_y = src.rows;

	cvtColor(src, src_gray, CV_BGR2GRAY);
	blur(src_gray, src_gray, Size(3, 3));

	if (gui) namedWindow("window", CV_WINDOW_AUTOSIZE);
	if (gui && detailedGUI) imshow("src_gray", src_gray);
	if (gui) createTrackbar(" Threshold:", "window", &thresh, max_thresh, convex_callback);
	if (gui) createTrackbar(" BlobSize:", "window", &blob_size, max_blob, blob_callback);

	convex_callback(0, 0);

	if (existingGoal) {
		pair<float,float> tempvar = off_angle();
		offAngle = tempvar.first;
		distance = tempvar.second;
	}
	cout << existingGoal << "::" << offAngle << "::" << distance << endl;
	if (gui) waitKey(0);
}


void convex_callback(int, void*) {
	Mat threshold_output, convex;
	vector<Vec4i> hierarchy;

	threshold(src_gray, threshold_output, thresh, max_thresh, THRESH_BINARY);
	if (gui && detailedGUI) imshow("threshold", threshold_output);
	findContours(threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));

	vector<vector<Point>> hull(contours.size());
	for(int i = 0; i < contours.size(); ++i) {
		convexHull(Mat(contours[i]), hull[i], false);
	}

	convex = Mat::zeros( threshold_output.size(), CV_8UC1 );
	for (int i = 0; i<contours.size(); ++i) {
		drawContours(convex, hull, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() );
	}

	subtracted = Mat::zeros(convex.size(), CV_8UC1);

	if (convex.isContinuous() && threshold_output.isContinuous()) {
		uchar *p1, *p2, *p3;
		p1 = convex.ptr<uchar>(0);
		p2 = threshold_output.ptr<uchar>(0);
		p3 = subtracted.ptr<uchar>(0);
		for (int i = 0; i < convex.rows * convex.cols; ++i) {
			if (*p2 != 0){
				*p3 = 0;
			} else if (*p1 != 0){
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
	blob_callback(0, 0);
}

void blob_callback(int, void*) {
	vector<Point> poly, largest_contour;
	vector<Vec4i> hierarchy;
	Mat blobed;
	Mat element = getStructuringElement(MORPH_ELLIPSE, Size(2 * blob_size + 1, 2 * blob_size + 1), Point(blob_size, blob_size));

	erode(subtracted, blobed, element);
	dilate(blobed, blobed, element);
	if (gui && detailedGUI) imshow("blobed", blobed);
	findContours(blobed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
	Mat result = src.clone();
	// Mat::zeros(blobed.size(), CV_8UC3);

	if (contours.size()!=0) {
		existingGoal = true;
		double largest_area = 0.0;
		for (int i = 0; i < contours.size(); i++) {
			// Find the area of contour
			double a = contourArea(contours[i], false);
			if (a > largest_area) {
				largest_contour = contours[i];
				largest_area = a;
			}
		}
	}
	approxPolyDP(Mat(largest_contour), poly, 3, true);
	goal.side_one = poly[0];
	goal.side_two = poly[1];
	goal.side_three = poly[2];
	goal.side_four = poly[3];

	if (gui) {
		line(result, goal.side_one, goal.side_two, Scalar(255, 0, 0), 5);
		line(result, goal.side_two, goal.side_three, Scalar(255, 0, 0), 5);
		line(result, goal.side_three, goal.side_four, Scalar(255, 0, 0), 5);
		line(result, goal.side_four, goal.side_one, Scalar(255, 0, 0), 5);
	}

	if (gui) imshow("window", result);
}

pair<float,float> off_angle() {
	float degPerPxlX = nativeAngleX / size_x;
	float degPerPxlY = nativeAngleY / size_y;
	float goalPixelY = size_y - (goal.side_two.y + goal.side_one.y + goal.side_three.y + goal.side_four.y) / 4;
	float goalAngleY = mountAngleY + degPerPxlY * (goalPixelY - size_y / 2);
	float goalPixelX = (goal.side_two.x + goal.side_one.x + goal.side_three.x + goal.side_four.x) / 4;
	float goalAngleX = mountAngleX + degPerPxlX * (goalPixelX - size_x / 2);
	float cameraDistance = (goalHeight - cameraHeight) / tan(goalAngleY);
	float shift = sqrt(shiftX * shiftX + shiftY * shiftY);
	float cameraAngle = M_PI - goalAngleX - atan(shiftX / shiftY);
	float distance = sqrt(cameraDistance * cameraDistance + shift * shift - 2 * cameraDistance * shift * cos(cameraAngle));
	float offAngle = asin(sin(cameraAngle) * cameraDistance / distance);
	offAngle = offAngle + atan(shiftY / shiftX)- M_PI / 2;
	distance = distance / milimetersPerInch;
	return make_pair(offAngle, distance);
}
