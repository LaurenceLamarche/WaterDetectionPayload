import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class TestGUI {

    public static void main(String[] args) {
        // Create a JFrame (window)
        JFrame frame = new JFrame("WATER DETECTION PAYLOAD");

        // Set the size of the window
        frame.setSize(300, 200);

        // Set the window to close when the close button is clicked
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create a JPanel (container) to hold components
        JPanel panel = new JPanel();

        // Create a JButton
        JButton button = new JButton("Start Data Collection");

        // Add an ActionListener to the button
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Start the Python script in a separate thread
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            // Start the Python script using the command line
                            Process process = Runtime.getRuntime().exec("python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/receive_script.py");
                            // Optional: You can add code here to capture and handle the process output

                            // Capture and display the output of the process
                            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                            String line;
                            while ((line = reader.readLine()) != null) {
                                System.out.println(line);
                            }
                        } catch (IOException ex) {
                            ex.printStackTrace();
                            // Handle any errors that occur while starting the script
                            JOptionPane.showMessageDialog(frame, "Error starting Python script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                        }
                    }
                }).start();

                // Send UART command to start data collection in a separate thread
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            // Start the Python script using the command line
                            Process process = Runtime.getRuntime().exec("python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/start_script.py");
                            // Optional: You can add code here to capture and handle the process output

                            // Capture and display the output of the process
                            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                            String line;
                            while ((line = reader.readLine()) != null) {
                                System.out.println(line);
                            }
                        } catch (IOException ex) {
                            ex.printStackTrace();
                            // Handle any errors that occur while starting the script
                            JOptionPane.showMessageDialog(frame, "Error starting 2nd Python script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                        }
                    }
                }).start();
            }
        });

        // Add the button to the panel
        panel.add(button);

        // Add the panel to the frame
        frame.add(panel);

        // Set the window to be visible
        frame.setVisible(true);
    }
}
