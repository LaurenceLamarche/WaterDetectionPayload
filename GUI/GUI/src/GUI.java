/**
 * GUI.java
 *
 * This code is meant to reproduce the OBC (On Board Computer) that will board the PEEKBot lunar rover.
 * This GUI controls the Water Detection Payload instrument
 * that was designed by the Carleton University CAPSTONE Team, consisting of:
 * Vlad Artychshuk, Nicholas Ficele, Declan McCoy, Laurence Lamarche-Cliche and Matthew Walsh
 * The main contacts regarding the code are:
 * Laurence (this GUI & the ground data-processing software) laurence.lamarchecliche@gmail.com
 * Matthew (Embedded Programming - code on the instrument)
 *
 * @author Laurence Lamarche-Cliche
 * Software Engineering Student
 * Carleton University
 * @version 1.0, March 18, 2024
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class GUI {

    private static Process currentProcess = null; // Global process reference

    // Method to stop the running script
    private static void stopScript() {
        if (currentProcess != null) {
            currentProcess.destroy();
            currentProcess = null;
        }
    }

    // Add action listeners for stop and change direction buttons
    private static void addStopButtonListeners(JButton stopButton, JButton changeDirectionButton, JFrame frame, JTextArea outputTextArea) {
        stopButton.addActionListener(e -> {
            stopScript();
            // Visual feedback for button click
            stopButton.setBackground(stopButton.getBackground().darker()); // Make button slightly darker when clicked
            new Thread(() -> {
                try {
                    currentProcess = Runtime.getRuntime().exec("python3.11 scripts/start_script.py stop");
                    BufferedReader reader = new BufferedReader(new InputStreamReader(currentProcess.getInputStream()));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        final String finalLine = line; // Create a final variable for use in lambda
                        SwingUtilities.invokeLater(() -> outputTextArea.append(finalLine + "\n"));
                    }
                } catch (IOException ex) {
                    ex.printStackTrace();
                    SwingUtilities.invokeLater(() -> JOptionPane.showMessageDialog(frame, "Error starting script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE));
                } finally {
                    SwingUtilities.invokeLater(() -> stopButton.setBackground(stopButton.getBackground().brighter())); // Reset button color after action
                }
            }).start();
        });
        changeDirectionButton.addActionListener(e -> {
            //stopScript(); we do NOT stop the running script because data collection must keep going.
            changeDirectionButton.setBackground(changeDirectionButton.getBackground().darker()); // Make button slightly darker when clicked
            new Thread(() -> {
                try {
                    currentProcess = Runtime.getRuntime().exec("python3.11 scripts/start_script.py reverse");
                    BufferedReader reader = new BufferedReader(new InputStreamReader(currentProcess.getInputStream()));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        final String finalLine = line; // Create a final variable for use in lambda
                        SwingUtilities.invokeLater(() -> outputTextArea.append(finalLine + "\n"));
                    }
                } catch (IOException ex) {
                    ex.printStackTrace();
                    SwingUtilities.invokeLater(() -> JOptionPane.showMessageDialog(frame, "Error starting script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE));
                } finally {
                    SwingUtilities.invokeLater(() -> changeDirectionButton.setBackground(changeDirectionButton.getBackground().brighter())); // Reset button color after action
                }
            }).start();
        });
    }

    private static void addActionButtonListeners(JButton button, JFrame frame, String scriptPath, JTextArea outputTextArea) {
        button.addActionListener(e -> {

            // Stop any currently running script
            stopScript();

            // Visual feedback for button click
            button.setBackground(button.getBackground().darker()); // Make button slightly darker when clicked
            new Thread(() -> {
                try {
                    currentProcess = Runtime.getRuntime().exec(scriptPath);
                    BufferedReader reader = new BufferedReader(new InputStreamReader(currentProcess.getInputStream()));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        final String finalLine = line; // Create a final variable for use in lambda
                        SwingUtilities.invokeLater(() -> outputTextArea.append(finalLine + "\n"));
                    }
                } catch (IOException ex) {
                    ex.printStackTrace();
                    SwingUtilities.invokeLater(() -> JOptionPane.showMessageDialog(frame, "Error starting script: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE));
                } finally {
                    SwingUtilities.invokeLater(() -> button.setBackground(button.getBackground().brighter())); // Reset button color after action
                }
            }).start();
        });
    }

    private static void addPlotButtonListener(JButton plotButton, JFrame frame, String plotScriptPath) {
        plotButton.addActionListener(e -> {
            // Visual feedback for button click
            plotButton.setBackground(plotButton.getBackground().darker()); // Make button slightly darker when clicked

            // Show custom dialog with options
            SwingUtilities.invokeLater(() -> {
                JPanel panel = new JPanel();
                JLabel descriptionLabel = new JLabel("<html>You can plot the latest data that was processed,<br>or look at model data</html>");
                panel.add(descriptionLabel);

                JButton okButton = new JButton("OK");
                okButton.addActionListener(event -> executePlottingScript(plotButton, plotScriptPath));

                JButton displayDataButton = new JButton("Display Model Data");
                displayDataButton.addActionListener(event -> displayModelData(frame));

                panel.add(okButton);
                panel.add(displayDataButton);

                JOptionPane.showOptionDialog(frame, panel, "Data Processing", JOptionPane.NO_OPTION, JOptionPane.PLAIN_MESSAGE, null, new Object[]{}, null);

                // Reset button color after showing dialog
                plotButton.setBackground(plotButton.getBackground().brighter());
            });
        });
    }

    private static void executePlottingScript(JButton plotButton, String plotScriptPath) {
        new Thread(() -> {
            try {
                Process process = Runtime.getRuntime().exec(plotScriptPath);
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            } finally {
                // Ensure button color is reset on the EDT
                SwingUtilities.invokeLater(() -> plotButton.setBackground(plotButton.getBackground().brighter()));
            }
        }).start();
        // Close the dialog after executing the script
        SwingUtilities.getWindowAncestor(plotButton).dispose();
    }

    private static void displayModelData(JFrame frame) {
        ImageIcon imageIcon = new ImageIcon("/Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/plots/simple_spectrum_plot.png");
        JOptionPane.showMessageDialog(frame, "", "Model Data", JOptionPane.INFORMATION_MESSAGE, imageIcon);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("WATER DETECTION PAYLOAD");
        frame.setSize(500, 500);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints constraints = new GridBagConstraints();
        constraints.insets = new Insets(10, 10, 10, 10);

        JTextArea outputTextArea = new JTextArea(20, 40);
        outputTextArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(outputTextArea);

        constraints.gridx = 0;
        constraints.gridy = 0;
        constraints.gridwidth = 2;
        constraints.fill = GridBagConstraints.BOTH;
        constraints.weightx = 1.0;
        constraints.weighty = 1.0;
        panel.add(scrollPane, constraints);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

        // Define more pale and user-friendly colors
        Color startButtonColor = new Color(102, 204, 153); // Pale green
        Color sleepButtonColor = new Color(102, 178, 255); // Pale blue
        Color plotButtonColor = new Color(255, 153, 153); // Pale red

        JButton startCollectionButton = createButton("Start Data Collection", startButtonColor);
        JButton sleepButton = createButton("Sleep Mode", sleepButtonColor);
        JButton plotButton = createButton("Plot Data", plotButtonColor);
        // Initialize the control buttons but set them invisible

        JPanel buttonPanel2 = new JPanel(new FlowLayout(FlowLayout.CENTER));

        JButton stopDataCollectionButton = createButton("Stop Data Collection", new Color(255, 102, 102));
        //stopDataCollectionButton.setVisible(false); // Initially invisible

        JButton reverseMotorDirectionButton = createButton("Change Direction", new Color(102, 204, 153)); // Pale green);
        //reverseMotorDirectionButton.setVisible(false); // Initially invisible

        // Refactored method to add action listeners
//        String startScriptPath = "python3.11 /Users/lola/Desktop/CU/CAPSTONE23-24/WaterDetectionPayload/WaterDetectionPayload/DATA_PROCESSING/receive_script.py";
        String startScriptPath = "python3.11 scripts/receive_script.py";
        String sleepScriptPath = "python3.11 scripts/start_script.py sleep";
        String plotScriptPath = "python3.11 scripts/data_processing.py --files 1";

        addActionButtonListeners(startCollectionButton, frame, startScriptPath, outputTextArea);
        addActionButtonListeners(sleepButton, frame, sleepScriptPath, outputTextArea);
        // Custom action for plotButton if necessary
        addPlotButtonListener(plotButton, frame, plotScriptPath);
        addStopButtonListeners(stopDataCollectionButton, reverseMotorDirectionButton, frame, outputTextArea);

        buttonPanel.add(startCollectionButton);
        buttonPanel.add(sleepButton);
        buttonPanel.add(plotButton);
        buttonPanel2.add(stopDataCollectionButton);
        buttonPanel2.add(reverseMotorDirectionButton);

        constraints.gridx = 0;
        constraints.gridy = 1;
        constraints.gridwidth = 2;
        panel.add(buttonPanel, constraints);

        constraints.gridx = 0;
        constraints.gridy = 3;
        constraints.gridwidth = 2;
        panel.add(buttonPanel2, constraints);

        frame.add(panel, BorderLayout.CENTER);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    private static JButton createButton(String text, Color bgColor) {
        JButton button = new JButton(text);
        button.setForeground(Color.WHITE);
        button.setBackground(bgColor);
        button.setOpaque(true);
        button.setBorderPainted(false);
        button.setFocusPainted(false);
        button.setFont(new Font("Arial", Font.BOLD, 16));
        button.setPreferredSize(new Dimension(200, 40));
        return button;
    }
}
