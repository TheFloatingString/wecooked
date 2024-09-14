def match_count_score(matches: int, n_kp1: int, n_kp2: int) -> float:
    return 100 * (matches / min(n_kp1, n_kp2))
