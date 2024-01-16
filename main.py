from collections import defaultdict

from quantumtester.game import run_game
from quantumtester.reg import get_reg, set_reg

VALUES_DEC = (20, 21, 22, 24, 36, 37, 38, 40)
NUM_ITERATIONS = 2

accuracies = defaultdict(float)

if __name__ == "__main__":
    # Get the original Win32PrioritySeparation value
    original_value = get_reg()
    print(f"Saving original Win32PrioritySeparation value ({original_value})... OK")

    # Initialize accuracies with default values
    for value in VALUES_DEC:
        accuracies[value] = 0.0

    print("Setting values... OK")

    # Start
    input(
        "\nThis test will take about 5 minutes. Keep your cursor on the ball at all times. Once the test is complete, you'll see your accuracy with each quantum value.\n\n"
        "Press ENTER to begin."
    )

    try:
        progress = 0
        for value in VALUES_DEC:
            progress += 2

            print("Testing value: " + str(value))

            # Create the stats text with progress and accuracy
            stats = (
                f"Tests {progress - 1} & {progress} of {len(VALUES_DEC) * NUM_ITERATIONS}\n\nAccuracy:\n"
                + ("\n".join([f"{k}: {v:.2f}%" for k, v in accuracies.items()]))
            )

            accuracy = run_game(value, stats, NUM_ITERATIONS)
            accuracies[value] = accuracy

            print(f"Accuracy with value {value}: {accuracy:.2f}%")
    except:
        # Handle exceptions and restore original settings
        print("Fatal error. Restoring original settings.")
        set_reg(original_value)
        print(
            f"Restoring original Win32PrioritySeparation value ({original_value})... OK"
        )
        exit()

    # Restore the original Win32PrioritySeparation value
    set_reg(original_value)
    print(f"Restoring original Win32PrioritySeparation value ({original_value})... OK")
    print("\nTests complete.")

    # Sort the accuracies dictionary by accuracy value
    average_accuracy = sum(accuracies.values()) / len(accuracies)
    sorted_accuracies = dict(
        sorted(accuracies.items(), key=lambda item: item[1], reverse=True)
    )

    # Print sorted accuracies
    print("Accuracy per setting:\n")
    for k, v in sorted_accuracies.items():
        print(f"dec {k}: {v:.2f}%")

    print(f"\nAverage: {average_accuracy:.2f}%")
