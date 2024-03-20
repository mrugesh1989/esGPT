# Report generation with ratings
def generate_report(comparison_results):
    # Example logic: assign ratings based on comparison results
    ratings = {}
    for index, diff in comparison_results.items():
        if diff > 0:
            ratings[index] = "Above Average"
        elif diff < 0:
            ratings[index] = "Below Average"
        else:
            ratings[index] = "Average"
    return ratings

# Verbose report generation with improvement suggestions
def generate_verbose_report(comparison_results):
    verbose_report = {}
    for index, diff in comparison_results.items():
        if diff > 0:
            verbose_report[index] = "The target company outperforms competitors in this area."
        elif diff < 0:
            verbose_report[index] = "The target company underperforms competitors in this area. Suggestions for improvement needed."
        else:
            verbose_report[index] = "The target company performs similarly to competitors in this area."
    return verbose_report
