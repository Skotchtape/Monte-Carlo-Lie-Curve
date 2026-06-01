# Monte-Carlo-Lie-Curve
#This program investigates the reliability of Monte Carlo
#estimation under finite data constraints using a simplified
#blackjack environment. Two player strategies are evaluated
#through repeated simulations to estimate their expected
#values and uncertainty.
#
#Although Monte Carlo methods converge to the correct result
#asymptotically, this project demonstrates that with limited
#samples they can frequently select the wrong strategy.
#The program computes confidence intervals, ground-truth
#expected values via large-scale simulation, and a "lie
#probability" curve that quantifies how often finite-sample
#Monte Carlo estimation leads to incorrect conclusions.
#
#The project highlights the gap between asymptotic correctness
#and practical reliability in stochastic decision-making.
