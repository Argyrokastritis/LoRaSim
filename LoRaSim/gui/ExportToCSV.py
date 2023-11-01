import csv
import os

class ExportToCSV:
    """
    A class representing a CSV exporter for Markov models.
    """

    def ExportMarkovToCSV(self):
        """
        Reads all the existing Markov models and exports them to a CSV file named 'Markov models.csv'.
        """

        # Constructs path to Models directory
        gui_dir = os.path.dirname(os.path.realpath(__file__))
        sim_dir = os.path.dirname(gui_dir)
        mod_dir = os.path.join(sim_dir, 'Models')

        # Gets list of all files in Models directory
        files = sorted(os.listdir(mod_dir))

        # Creates CSV file and writes header row
        with open('Markov models.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Description', 'TX Time (ms)', 'P00', 'P01', 'P10', 'P11'])

            # Writes data for each Markov model to CSV file
            for f in files:
                file_path = os.path.join(mod_dir, f)
                with open(file_path, mode='r') as model_file:
                    lines = model_file.readlines()
                    title = lines[0].split('=')[1].strip()
                    description = lines[1].split('=')[1].strip()
                    tx_time = lines[2].split('=')[1].strip()
                    p00 = (lines[3].split('=')[1].strip())
                    p01 = (lines[4].split('=')[1].strip())
                    p10 = (lines[5].split('=')[1].strip())
                    p11 = (lines[6].split('=')[1].strip())

                    writer.writerow([title, description, tx_time, p00, p01, p10, p11])

        print("Markov models exported to 'Markov models.csv' and may contain negative values!")

        with open('Markov models.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Read the header row
            rows = []
            for row in reader:
                if float(row[3]) < 0:
                    row[3] = '0.001'  # Set P00 to a small positive value
                if float(row[4]) < 0:
                    row[4] = '0.001'  # Set P01 to a small positive value
                rows.append(row)

        with open('Markov models.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

        print("Markov models exported to the changed'Markov models.csv' and DON'T contain negative values anymore!")
