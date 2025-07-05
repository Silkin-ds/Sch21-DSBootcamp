num_of_steps = 3
report_template = """Report

We have made {observations} observations from tossing a coin: {tails} of them were tails and {heads} of them were heads. The probabilities are {tail_prob:.2f}% and {head_prob:.2f}%, respectively. Our forecast is that in the next {num_of_steps} observations we will have: {predicted_tails} tail(s) and {predicted_heads} head(s)."""