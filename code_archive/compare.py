# Logical algorithms to compare benchmarking indices
def compare_indices(company_indices, competitor_indices):
    # Example logic: calculate difference in indices
    comparison_results = {}
    for index, value in company_indices.items():
        comparison_results[index] = value - competitor_indices.get(index, 0)
    return comparison_results
