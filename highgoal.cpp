#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <dirent.h>
#include <math.h>
// For availability of M_PI
#define _USE_MATH_DEFINES

using namespace cv;
using namespace std;

// Declare vars
Mat src, src_gray, subtracted;
int size_x = -1;
int size_y = -1;
struct rect_points {
	Point side_one;
	Point side_two;
	Point side_three;
	Point side_four;
};
rect_points goal;
vector<vector<Point> > contours;
void convex_callback(int, void*);
void blob_callback(int, void*);
void analyzeImage(Mat src);
pair<float,float> angle_and_dist();

// Create min and max variables for optimal detection based on environment
int thresh = 210;
int max_thresh = 255;

int blob_size = 5;
int max_blob = 20; // Used only in gui

bool gui = false; // Turn on for debugging
bool detailedGUI = false;
bool test = false;
bool latest = false;
bool done = false;
bool foundGoal = false;

// CONSTANTS
// Distances are in inches, angles are in degrees
const float millimetersPerInch = 25.4;
const float mountAngleX = 0.0;
const float mountAngleY = 45.0 * M_PI / 180;
const int nativeResX = 2592;
const int nativeResY = 1944;
const float nativeAngleX = 53.5 * M_PI / 180;
const float nativeAngleY = 41.41 * M_PI / 180;
const float shiftX = 13.25 * millimetersPerInch; // 13.25 inches
const float shiftY = 2.5 * millimeters; // 2.5 inches
const float goalHeight = 8 * 12 * millimetersPerInch; // 8 feet
const float cameraHeight = 296.0; // 296 millimeters

// Access a specified directory, used in one of main's options
int getdir(string dir, vector<string> &files) {
	DIR *dp;
	struct dirent *dirp;
	if ((dp = opendir(dir.c_str())) == NULL) {
		cout << "Error opening directory '" << dir << "'" << endl;
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
	// Different args determine different modes, so we can debug or run with ease
	// Modes are (in order): GUI, testing, using latest.jpg (on RPi), or other directory (uses getDir)
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
			if (dir.substr(dir.size() - 1, 1) != "/") {
				dir += "/";
			}

			int status = getdir(dir, files);

			if (status >= 0) {
				cout << "Reading directory '" << dir << "'" << endl;
			} else {
				return status;
			}

			for (unsigned int i = 0; i < files.size(); i++) {
				if (files[i].length() < 4 || files[i].substr(files[i].length() - 4, 4) != ".jpg") continue;
				string path = dir + files[i];

				src = imread(path, CV_LOAD_IMAGE_UNCHANGED);
				if (src.empty()) {
					cout << "Error: Image '" << path << "' cannot be loaded" << endl;
					return -1;
				}
				cout << "Loaded image '" << files[i] << "'" << endl;
				analyzeImage(src);

				waitKey(0);
				done = true;
			}
		}
	}

	// If no mode is specified, run the defualt image
	if (!done) {
		src = imread(image, CV_LOAD_IMAGE_UNCHANGED);
		if (src.empty()) {
			cout << "Error: Image '" << image << "' cannot be loaded" << endl;
			return -1;
		}
		analyzeImage(src);
	}
	return 0;
}

// Process the image specified in main for angle and distance
void analyzeImage(Mat src) {
	float offAngle = 0.0;
	float distance = 0.0;
	size_x = src.cols;
	size_y = src.rows;

	// Convert to 1 channel (gray) for use by other operators
	cvtColor(src, src_gray, CV_BGR2GRAY);
	// Blur image as to round any small errors
	blur(src_gray, src_gray, Size(3, 3));

	if (gui) {
		namedWindow("window", CV_WINDOW_AUTOSIZE);
		if (detailedGUI) imshow("src_gray", src_gray);
		createTrackbar(" Threshold:", "window", &thresh, max_thresh, convex_callback);
		createTrackbar(" BlobSize:", "window", &blob_size, max_blob, blob_callback);
	}

	convex_callback(0, 0);

	// Calculate angle and distance if goal is found
	if (foundGoal) {
		pair<float,float> tempvar = angle_and_dist();
		offAngle = tempvar.first;
		distance = tempvar.second;
	}
	// Print results for debugging or communication with RIO
	cout << foundGoal << "::" << offAngle << "::" << distance << endl;
	if (gui) waitKey(0);
}


void convex_callback(int, void*) {
	Mat threshold_output, convex;
	vector<Vec4i> hierarchy;

	// Convert to only black and white pixels using threshold for use by findcontours
	threshold(src_gray, threshold_output, thresh, max_thresh, THRESH_BINARY);
	if (gui && detailedGUI) imshow("threshold", threshold_output);
	// Find shapes for use by other operators
	findContours(threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));

	// Blob Filter for pre conxev hull?

	// Create convex hulls of contours for detecting the high goal's U shape
	vector<vector<Point> > hull(contours.size());
	for(int i = 0; i < contours.size(); ++i) {
		convexHull(Mat(contours[i]), hull[i], false);
	}

	convex = Mat::zeros( threshold_output.size(), CV_8UC1 );
	for (int i = 0; i<contours.size(); ++i) {
		drawContours(convex, hull, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() );
	}

	// Subtract the original contours from convex hulls, remaining with the inner part of the U
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

	if (gui && detailedGUI) {
		imshow("convex", convex);
		imshow("subtracted", subtracted);
	}
	// Detect highgoal from what's left and create a goal object
	blob_callback(0, 0);
}

void blob_callback(int, void*) {
	vector<Point> poly, largest_contour;
	vector<Vec4i> hierarchy;
	Mat blobbed;
	Mat element = getStructuringElement(MORPH_ELLIPSE, Size(2 * blob_size + 1, 2 * blob_size + 1), Point(blob_size, blob_size));

	// Grow and shrink shape to get better edges
	erode(subtracted, blobbed, element);
	dilate(blobbed, blobbed, element);
	if (gui && detailedGUI) imshow("blobbed", blobbed);
	findContours(blobbed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
	Mat result = src.clone();
	// Mat::zeros(blobbed.size(), CV_8UC3);

	// Filter for largest
	if (contours.size()!=0) {
		foundGoal = true;
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
	// Create goal
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
		imshow("window", result);
	}
}

// Calculate angle and distance based off of pixel coordinates. Return radians (straight ahead - 0, right - positive, left - negative), distance (on the floor from shooter to middle of U on highgoal)
pair<float,float> angle_and_dist() {
	float degPerPxlX = nativeAngleX / size_x;
	float degPerPxlY = nativeAngleY / size_y;
	float goalPixelY = size_y - (goal.side_two.y + goal.side_one.y + goal.side_three.y + goal.side_four.y) / 4;
	float goalAngleY = mountAngleY + degPerPxlY * (goalPixelY - size_y / 2);
	float goalPixelX = (goal.side_two.x + goal.side_one.x + goal.side_three.x + goal.side_four.x) / 4;
	float goalAngleX = mountAngleX + degPerPxlX * (goalPixelX - size_x / 2);
	float cameraDistance = (goalHeight - cameraHeight) / tan(goalAngleY);
	float shift = sqrt(shiftX * shiftX + shiftY * shiftY);
	float cameraAngle = M_PI - goalAngleX - atan(shiftX / shiftY);
	cameraAngle = M_PI/2 + goalAngleX - atan(shiftX / shiftY);
	float distance = sqrt(cameraDistance * cameraDistance + shift * shift - 2 * cameraDistance * shift * cos(cameraAngle));
	float offAngle = asin(sin(cameraAngle) * cameraDistance / distance);
	offAngle += atan(shiftY / shiftX) - M_PI / 2;
	distance /= millimetersPerInch;
	return make_pair(offAngle, distance);
}
