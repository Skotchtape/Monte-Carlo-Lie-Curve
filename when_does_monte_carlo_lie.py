#When Does Monte Carlo Lie?
#Author: Krishiv Makwana
#
#Description:
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


import random
import math

#-------------------
#BlackJack Mechanics
#-------------------

def draw_card():
    #Draw a random card value.
    #Face cards count as 10, Ace counts as 11 initially.
    #Infinite deck assumption.
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11]
    return random.choice(cards)

def hand_total(hand):
    #Compute the total value of a blackjack hand.
    #Adjusts Aces from 11 to 1 as needed to avoid busting.
    total = sum(hand)
    aces = hand.count(11)

    #Convert Aces from 11 to 1 if total exceeds 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def compare_hands(player_hand, dealer_hand):
    #Compare player and dealer hands.
    #Returns:
            #+1 if player wins
            #0 if tie
            #-1 if player loses
    player_total = hand_total(player_hand)
    dealer_total = hand_total(dealer_hand)

    #Bust rules
    if player_total > 21:
        return -1
    if dealer_total > 21:
        return 1

    #Compare totals
    if player_total > dealer_total:
        return 1
    elif player_total < dealer_total:
        return -1
    else:
        return 0

def play_turn_hit_to_threshold(threshold):
    #Play a blackjack turn where the player hits
    #until reaching a fixed threshold
    hand = [draw_card(), draw_card()]
    while hand_total(hand) < threshold:
        hand.append(draw_card())
    return hand


def play_one_round(player_threshold):
    #Simulate one round of blackjack.
    #Player follows a hit-to-threshold policy.
    #Dealer always hits to 17
    player_hand = play_turn_hit_to_threshold(player_threshold)
    dealer_hand = play_turn_hit_to_threshold(17)

    outcome = compare_hands(player_hand, dealer_hand)
    return outcome

#----------------------
#Monte Carlo estimation
#----------------------

def simulate(num_rounds, player_threshold):
    #Estimate expected value (EV) and uncertainty for a strategy
    #using Monte Carlo simulation.
    outcomes = []
    wins = 0
    losses = 0
    ties = 0

    for _ in range(num_rounds):
        outcome = play_one_round(player_threshold)
        outcomes.append(outcome)

        if outcome == 1:
            wins += 1
        elif outcome == -1:
            losses += 1
        else:
            ties += 1

    #Expected value (mean outcome)
    mean = sum(outcomes) / num_rounds

    #Sample variance and standard deviation
    variance = sum((x - mean) ** 2 for x in outcomes) / (num_rounds - 1)
    std = math.sqrt(variance)

    #Standard error of the mean
    se = std / math.sqrt(num_rounds)

    #95% confidence interval using normal approximation
    z = 1.96
    ci_low = mean - z * se
    ci_high = mean + z * se

    win_rate = wins / num_rounds
    loss_rate = losses / num_rounds
    tie_rate = ties / num_rounds

    return mean, (ci_low, ci_high), win_rate, loss_rate, tie_rate

def lie_probability(N, R, better_threshold):
    #Compute the probability that Monte Carlo estimation
    #selects the wrong strategy given N samples
    wrong = 0
    for _ in range(R):
        ev17, _, _, _, _ = simulate(N, 17)
        ev18, _, _, _, _ = simulate(N, 18)

        # Strategy chosen by finite-sample estimation
        est_winner = 18 if ev18 > ev17 else 17

        # Count incorrect selections
        if est_winner != better_threshold:
            wrong += 1

    return wrong / R

#-----------
#Experiments
#-----------

#Sanity check: single-round outcomes
print("Testing one round with hit-to-17:", play_one_round(17))
print("Testing one round with hit-to-18:", play_one_round(18))

#Monte Carlo estimation for hit-to-17
N = 10000
mean, (ci_low, ci_high), win_rate, loss_rate, tie_rate = simulate(N, 17)

print(f"Rounds: {N}")
print(f"EV (mean): {mean:.4f}")
print(f"95% CI: [{ci_low: .4f}, {ci_high: .4f}]")
print(f"Win rate: {win_rate: .3f}")
print(f"Loss rate: {loss_rate:.3f}")
print(f"Tie rate: {tie_rate:.3f}")

#Ground truth using large simulation
print("\n--- Ground truth (large N) ---")

M = 200000
ev17, _, _, _, _ = simulate(M, 17)
ev18, _, _, _, _ = simulate(M, 18)

print(f"M={M} EV17={ev17:.4f} EV18={ev18:.4f}")

better = 18 if ev18 > ev17 else 17
print("True better strategy (from large run): hit-to-", better)

#Lie probability curve
print("\n--- Lie curve ---")
R = 1000
Ns = [50, 100, 200, 500, 1000, 2000]

for N in Ns:
    p = lie_probability(N, R, better)
    print(f"N={N:4d} lie_prob={p:.3f}")

#Identify sample size where lie probability drops below threshold
threshold =0.25
for N in Ns:
    p = lie_probability(N, R, better)
    if p < threshold:
        print(f"Lie probability drops below {threshold} at N={N}")
        break
