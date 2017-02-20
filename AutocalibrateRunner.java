package org.usfirst.frc.team4904.robot;

import java.io.IOException;

import edu.wpi.first.wpilibj.networktables.NetworkTable;

public class AutocalibrateRunner {

	double numCalibrations = 0;

	public static void main(String[] args) {
		new AutocalibrateRunner2().run();
	}
	
	public void run() {
		NetworkTable.setClientMode();
		NetworkTable.setIPAddress("tegra-ubuntu.local");
		NetworkTable table = NetworkTable.getTable("autocalibration");
		double calibrate = table.getNumber("autocalibrate");
		if(calibrate > numCalibrations) {
			numCalibrations += 1;
			Process p;
			try {
				p = Runtime.getRuntime().exec("python autocalibrate.py");
				p.waitFor();
				System.out.println("Finished Autocalibrating!");
			} catch (IOException e) {
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
		}
	}
}
