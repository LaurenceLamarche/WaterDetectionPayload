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
        JButton startCollectionButton = new JButton("Start Data Collection");
        startCollectionButton.setForeground(Color.WHITE); // Set text color to white
        startCollectionButton.setBackground(new Color(0, 128, 0)); // Set background color to green
        startCollectionButton.setOpaque(true);
        startCollectionButton.setBorderPainted(false);
        startCollectionButton.setFocusPainted(false); // Remove focus border
        startCollectionButton.setFont(new Font("Arial", Font.BOLD, 16)); // Set font and size

        // Set preferred size for the button
        startCollectionButton.setPreferredSize(new Dimension(200, 40)); // Adjust width and height as needed

        // Create the Sleep Mode JButton
        JButton sleepButton = new JButton("Sleep Mode");
        sleepButton.setForeground(Color.WHITE); // Set text color to white
        sleepButton.setBackground(Color.BLUE); // Set background color to green
        sleepButton.setOpaque(true);
        sleepButton.setBorderPainted(false);
        sleepButton.setFocusPainted(false); // Remove focus border
        sleepButton.setFont(new Font("Arial", Font.BOLD, 16)); // Set font and size
        // Set preferred size for the button
        sleepButton.setPreferredSize(new Dimension(200, 40)); // Adjust width and height as needed

        // create the PLot button
        JButton plotButton = new JButton("Plot Data");
        plotButton.setForeground(Color.WHITE); // Set text color to white
        plotButton.setBackground(Color.RED); // Set background color to green
        plotButton.setOpaque(true);
        plotButton.setBorderPainted(false);
        plotButton.setFocusPainted(false); // Remove focus border
        plotButton.setFont(new Font("Arial", Font.BOLD, 16)); // Set font and size
        // Set preferred size for the button
        plotButton.setPreferredSize(new Dimension(200, 40));

        // Add the buttons to the BorderLayout panel
        buttonPanel.add(startCollectionButton);
        buttonPanel.add(sleepButton);
        buttonPanel.add(plotButton);

        // Add the BorderLayout panel to the GridBagLayout panel
        constraints.gridx = 0;
        constraints.gridy = 1;
        constraints.gridwidth = 2;
        constraints.anchor = GridBagConstraints.CENTER;
        panel.add(buttonPanel, constraints);

        // Add an ActionListener to the start data collection button
        startCollectionButton.addActionListener(new ActionListener() {
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
            }
        });

        sleepButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Start the Python start script in a separate thread
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            Process process = Runtime.getRuntime().exec("python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/start_script.py");
                            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                            String line;
                            //outputTextArea.append("starting thread 2\n");
                            while ((line = reader.readLine()) != null) {
                                // Append the output to the JTextArea
                                outputTextArea.append(line + "\n");
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

        // Add ActionListener for the new button (example logic)
        plotButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                JOptionPane.showMessageDialog(frame, "When data is available, you can display it here", "Data Plots", JOptionPane.INFORMATION_MESSAGE);
            }
        });

        // Center the panel on the frame
        frame.add(panel, BorderLayout.CENTER);

        // Set the window to be visible
        frame.setLocationRelativeTo(null); // Center the frame on the screen
        frame.setVisible(true);
    }
}
