import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class AutocalibrateRunnerSockets {

	private static final String HOSTNAME = "10.49.4.73";
	private static final int PORT_NUMBER = 5800;
	private static BufferedReader input;
	static ServerSocket listener = null;
	
	public static void main(String[] args) {

		try {
			listener = new ServerSocket(PORT_NUMBER, 100, InetAddress.getByName(HOSTNAME));
			Socket socket = listener.accept();
			BufferedReader in = new BufferedReader(new InputStreamReader(
					socket.getInputStream()));
			
			while (true) {
				String line = in.readLine();
				if(line != null) {
					if(line.contains("autocalibrate")) {
						Process p = Runtime.getRuntime().exec("python autocalibrate.py");
					}
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}