from model import train_from_csv, predict_single, WEIGHTS_FILE
import os


def validate_range(value, min_val, max_val, name):
    if not (min_val <= value <= max_val):
        print(f"{name} must be between {min_val} and {max_val}.")
        return False
    return True


def main():
    print("Student Marks Predictor")
    print("Please train the `model` before making predictions.")
    print("\nCommands:")
    print("  train   - Train model from CSV")
    print("  predict - Predict student score")
    print("  exit    - Quit program")

    while True:
        cmd = input("\n>>> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "train":
            this_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.normpath(
                os.path.join(this_dir, "..", "data", "student_marks.csv")
            )

            if not os.path.exists(csv_path):
                print(f"CSV file not found at: {csv_path}")
                continue

            try:
                mae, w = train_from_csv(csv_path)
                print("Training completed.")
                print(f"MAE: {mae:.2f}")
                print(f"Weights saved to: {WEIGHTS_FILE}")
            except Exception as e:
                print("Training failed:", e)

        elif cmd == "predict":
            if not os.path.exists(WEIGHTS_FILE):
                print("Model not trained yet. Run 'train' first.")
                continue

            try:
                a = float(input("assignments_avg (out of 10): "))
                q = float(input("quiz_avg (out of 10): "))
                att = float(input("attendance_percent (0-100): "))
                p = float(input("project_score (out of 20): "))
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                continue

            if not validate_range(a, 0, 10, "Assignments average"):
                continue
            if not validate_range(q, 0, 10, "Quiz average"):
                continue
            if not validate_range(att, 0, 100, "Attendance percent"):
                continue
            if not validate_range(p, 0, 20, "Project score"):
                continue

            try:
                pred = predict_single(a, q, att, p)
                print(f"Predicted Final Score (out of 45): {pred:.2f}")
            except Exception as e:
                print("Prediction failed:", e)

        else:
            print("Unknown command. Please use: train, predict, or exit.")


if __name__ == "__main__":
    main()