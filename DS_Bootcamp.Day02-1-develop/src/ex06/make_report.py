import sys
import logging
from config import num_of_steps, report_template
from analytics import Research, Analytics

def generate_report(data, num_of_steps):
    analytics = Analytics(data)
    head_count, tail_count = analytics.counts()
    head_fraction, tail_fraction = analytics.fractions(head_count, tail_count)
    random_predictions = analytics.predict_random(num_of_steps)
    predicted_heads = sum(1 for pred in random_predictions if pred[0] == 1)
    predicted_tails = num_of_steps - predicted_heads
    report = report_template.format(
        observations=len(data),
        tails=tail_count,
        heads=head_count,
        tail_prob=tail_fraction,
        head_prob=head_fraction,
        num_of_steps=num_of_steps,
        predicted_tails=predicted_tails,
        predicted_heads=predicted_heads
    )
    return report

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError("Incorrect number of arguments is given")
        research = Research(sys.argv[1])
        data = research.file_reader(flag_header=True)
        report = generate_report(data, num_of_steps)
        print(report)
        analytics = Analytics(data)
        analytics.save_file(report, "report", "txt")
        research.send_telegram_message("The report has been successfully created")
    except Exception as e:
        logging.error(f"Error: {e}")
        research.send_telegram_message("The report hasn’t been created due to an error")