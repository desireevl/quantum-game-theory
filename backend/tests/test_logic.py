from backend.logic import PayoffTable

# User prisoner's dilemma payoff
sample_payoff_table = {'00': (-1, -1),
                       '01': (-3, 0),
                       '10': (0, -3),
                       '11': (-2, -2)}

def test_PayoffTable():
    payoff_table = PayoffTable(n_players=2, n_choices=2, payoff=sample_payoff_table)
    assert payoff_table.get_payoff_table() == sample_payoff_table