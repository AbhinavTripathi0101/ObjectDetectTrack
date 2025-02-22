import pandas as pd
import os
import config  # Import configuration


def generate_report():
    """Generate traffic congestion and summary report."""

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(config.OUTPUT_CSV_PATH):
        print(" Error: Output CSV file not found. Run `main.py` first.")
        return

    df = pd.read_csv(config.OUTPUT_CSV_PATH)

    if df.empty:
        print("⚠ No data found in output.csv. Skipping report generation.")
        return

    vehicle_count = df["Object ID"].nunique()
    avg_left_ROI = df["Total Left ROI"].mean()
    avg_right_ROI = df["Total Right ROI"].mean()
    traffic_status_counts = df["Traffic Status"].value_counts()

    # **Determine Overall Traffic Condition**
    avg_vehicles_per_frame = (avg_left_ROI + avg_right_ROI) / 2
    if avg_vehicles_per_frame < 3:
        overall_traffic_condition = "Light Traffic"
    elif avg_vehicles_per_frame < 7:
        overall_traffic_condition = "Moderate Traffic"
    else:
        overall_traffic_condition = "Heavy Traffic - Consider Traffic Control Measures"

    # Write the report file
    with open(config.OUTPUT_REPORT_PATH, "w") as f:
        f.write(f"Total Unique Vehicles Detected: {vehicle_count}\n")

        # **ROI Analysis**
        f.write("\nTraffic Flow by ROI:\n")
        f.write(f"Average Vehicles in Left ROI: {avg_left_ROI:.2f}\n")
        f.write(f"Average Vehicles in Right ROI: {avg_right_ROI:.2f}\n")

        # **Traffic Status Summary**
        f.write("\nOverall Traffic Status Distribution:\n")
        for status, count in traffic_status_counts.items():
            f.write(f"{status}: {count} frames\n")

        # **Overall Traffic Condition**
        f.write("\nOverall Traffic Condition: " + overall_traffic_condition + "\n")

    print(f" Traffic report generated successfully: {config.OUTPUT_REPORT_PATH}")


if __name__ == "__main__":
    generate_report()
