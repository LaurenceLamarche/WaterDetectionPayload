import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class GUI {

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
        button.setBackground(new Color(0, 128, 0)); // Set background color to green
        button.setOpaque(true);
        button.setBorderPainted(false);
        button.setFocusPainted(false); // false removes focus border
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
                // Code to start the Python script
                try {
                    // Start the Python script using the command line
                    Process process = Runtime.getRuntime().exec("python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/receive_script.py");

                    // Read the process output asynchronously
                    Thread thread = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            try {
                                // Capture and display the output of the process
                                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                                String line;
                                while ((line = reader.readLine()) != null) {
                                    System.out.println(line);
                                }
                            } catch (IOException ex) {
                                ex.printStackTrace();
                                // Handle any errors that occur while reading the process output
                            }
                        }
                    });
                    thread.start(); // Start the thread
                } catch (IOException ex) {
                    ex.printStackTrace();
                    // Handle any errors that occur while starting the script
                    JOptionPane.showMessageDialog(frame, "Error starting Python script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        // Add the button to the panel
        //panel.add(button, constraints);

        // Center the panel on the frame
        frame.add(panel, BorderLayout.CENTER);

        // Set the window to be visible
        frame.setLocationRelativeTo(null); // Center the frame on the screen
        frame.setVisible(true);
    }
}
