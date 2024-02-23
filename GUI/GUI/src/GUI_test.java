import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;

public class GUI_test {

    public static void main(String[] args) {
        // Create a JFrame (window)
        JFrame frame = new JFrame("WATER DETECTION PAYLOAD");

        // Set the size of the window
        frame.setSize(500, 300);

        // Set the window to close when the close button is clicked
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create a JPanel (container) to hold components
        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints constraints = new GridBagConstraints();
        constraints.insets = new Insets(10, 10, 10, 10);

        // Create a JButton
        JButton button = new JButton("Start Data Collection");
        button.setForeground(Color.WHITE); // Set text color to white
        button.setBackground(Color.GREEN); // Set background color to green
        button.setFocusPainted(false); // Remove focus border
        button.setFont(new Font("Arial", Font.BOLD, 16)); // Set font and size

        // Center the button on the panel
        constraints.gridx = 0;
        constraints.gridy = 0;
        constraints.gridwidth = 2;
        constraints.anchor = GridBagConstraints.CENTER;
        panel.add(button, constraints);

        // Add an ActionListener to the button
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Disable the button
                button.setEnabled(false);

                // Show a popup message
                JOptionPane.showMessageDialog(frame, "Data collection has started", "Info", JOptionPane.INFORMATION_MESSAGE);

                // Code to start the Python script
                try {
                    // Start the Python script using the command line and redirect output to a file
                    ProcessBuilder processBuilder = new ProcessBuilder("python3.11", "/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/receive_script.py");
                    processBuilder.redirectErrorStream(true);
                    Process process = processBuilder.start();

                    // Read and display the output of the process
                    BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        System.out.println(line); // Print output to console
                        // You can also append 'line' to a JTextArea to display in the GUI
                    }

                    // Enable the button after the script is done executing
                    button.setEnabled(true);
                } catch (IOException ex) {
                    ex.printStackTrace();
                    // Handle any errors that occur while starting the script
                    JOptionPane.showMessageDialog(frame, "Error starting Python script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        // Center the panel on the frame
        frame.add(panel, BorderLayout.CENTER);

        // Set the window to be visible
        frame.setLocationRelativeTo(null); // Center the frame on the screen
        frame.setVisible(true);
    }
}

