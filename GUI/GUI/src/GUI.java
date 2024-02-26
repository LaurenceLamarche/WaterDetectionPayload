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
        frame.setSize(500, 500);

        // Set the window to close when the close button is clicked
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create a JPanel (container) to hold components
        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints constraints = new GridBagConstraints();
        constraints.insets = new Insets(10, 10, 10, 10);

        // Create a JTextArea to display the output
        JTextArea outputTextArea = new JTextArea(20, 40);
        outputTextArea.setEditable(false); // Make it read-only
        JScrollPane scrollPane = new JScrollPane(outputTextArea);

        // Center the JTextArea on the panel
        constraints.gridx = 0;
        constraints.gridy = 0;
        constraints.gridwidth = 2;
        constraints.weightx = 1.0; // Make it expand horizontally
        constraints.weighty = 1.0; // Make it expand vertically
        constraints.fill = GridBagConstraints.BOTH; // Fill both horizontally and vertically
        constraints.anchor = GridBagConstraints.CENTER;
        panel.add(scrollPane, constraints);

        // Create a JPanel with BorderLayout for the button
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

        // Create the start JButton
        JButton button = new JButton("Start Data Collection");
        button.setForeground(Color.WHITE); // Set text color to white
        button.setBackground(new Color(0, 128, 0)); // Set background color to green
        button.setOpaque(true);
        button.setBorderPainted(false);
        button.setFocusPainted(false); // Remove focus border
        button.setFont(new Font("Arial", Font.BOLD, 16)); // Set font and size

        // Set preferred size for the button
        button.setPreferredSize(new Dimension(200, 40)); // Adjust width and height as needed

        // Create the Sleep Mode JButton
        JButton button1 = new JButton("Sleep Mode");
        button1.setForeground(Color.WHITE); // Set text color to white
        button1.setBackground(Color.BLUE); // Set background color to green
        button1.setOpaque(true);
        button1.setBorderPainted(false);
        button1.setFocusPainted(false); // Remove focus border
        button1.setFont(new Font("Arial", Font.BOLD, 16)); // Set font and size

        // Set preferred size for the button
        button1.setPreferredSize(new Dimension(200, 40)); // Adjust width and height as needed


        // Add the button to the BorderLayout panel
        buttonPanel.add(button);
        buttonPanel.add(button1);

        // Add the BorderLayout panel to the GridBagLayout panel
        constraints.gridx = 0;
        constraints.gridy = 1;
        constraints.gridwidth = 2;
        constraints.anchor = GridBagConstraints.CENTER;
        panel.add(buttonPanel, constraints);

        // Add an ActionListener to the button
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Start the Python script in a separate thread
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            Process process = Runtime.getRuntime().exec("python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/receive_script.py");
                            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                            String line;
                            //outputTextArea.append("starting thread 1\n");
                            while ((line = reader.readLine()) != null) {
                                // Append the output to the JTextArea
                                outputTextArea.append(line + "\n");
                            }
                        } catch (IOException ex) {
                            ex.printStackTrace();
                            // Handle any errors that occur while starting the script
                            JOptionPane.showMessageDialog(frame, "Error starting Python script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                        }
                    }
                }).start();

//                // Send UART command to start data collection in a separate thread
//                new Thread(new Runnable() {
//                    @Override
//                    public void run() {
//                        try {
//                            Process process = Runtime.getRuntime().exec("python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/start_script.py");
//                            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
//                            String line;
//                            //outputTextArea.append("starting thread 2\n");
//                            while ((line = reader.readLine()) != null) {
//                                // Append the output to the JTextArea
//                                outputTextArea.append(line + "\n");
//                            }
//                        } catch (IOException ex) {
//                            ex.printStackTrace();
//                            // Handle any errors that occur while starting the script
//                            JOptionPane.showMessageDialog(frame, "Error starting 2nd Python script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
//                        }
//
//                    }
//                }).start();
            }
        });

        // Center the panel on the frame
        frame.add(panel, BorderLayout.CENTER);

        // Set the window to be visible
        frame.setLocationRelativeTo(null); // Center the frame on the screen
        frame.setVisible(true);
    }
}
