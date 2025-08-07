


import unittest
from algebra.lll import lll_reduction


class TestLLL(unittest.TestCase):

    def gram_schmidt(self, B):
        import numpy as np
        B = [np.array(b, dtype=float) for b in B]
        n = len(B)
        d = len(B[0])
        B_star = []
        mu = np.zeros((n, n))
        for i in range(n):
            b_star = B[i].copy()
            for j in range(i):
                mu[i, j] = np.dot(B[i], B_star[j]) / np.dot(B_star[j], B_star[j])
                b_star -= mu[i, j] * B_star[j]
            B_star.append(b_star)
        return B_star, mu

    def is_lll_reduced(self, B, delta=0.75, places=6):
        import numpy as np
        B_star, mu = self.gram_schmidt(B)
        n = len(B)
        print("Checking LLL-reduced basis:", B)
        print("mu matrix:\n", mu)
        # Size reduction: |mu[i, j]| <= 0.5 for i > j
        for i in range(n):
            for j in range(i):
                print(f"mu[{i},{j}] = {mu[i,j]}")
                self.assertLessEqual(abs(mu[i, j]), 0.5 + 10**-places, f"Size reduction failed at mu[{i},{j}]={mu[i,j]}")
        # Lovász condition: delta * ||b*_k-1||^2 <= ||b*_k||^2 + mu[k, k-1]^2 * ||b*_{k-1}||^2
        for k in range(1, n):
            norm_km1 = np.dot(B_star[k-1], B_star[k-1])
            norm_k = np.dot(B_star[k], B_star[k])
            lhs = delta * norm_km1
            rhs = norm_k + mu[k, k-1]**2 * norm_km1
            print(f"Lovasz: k={k}, lhs={lhs}, rhs={rhs}")
            self.assertLessEqual(lhs - rhs, 10**-places, f"Lovász condition failed at k={k}: {lhs} > {rhs}")


    def test_lll(self):
        # Test 1
        m = lll_reduction([[1, 1, 1], [-1, 0, 2], [3, 5, 6]], 0.75)
        print("Reduced basis after LLL:", m)
        m = [list(map(float, v)) for v in m]
        self.is_lll_reduced(m, delta=0.75)
        # Test 2
        m = [[105, 821, 404, 328], [881, 667, 644, 927], [181, 483, 87, 500], [893, 834, 732, 441]]
        m = lll_reduction(m, 0.75)
        print("Reduced basis after LLL:", m)
        m = [list(map(float, v)) for v in m]
        self.is_lll_reduced(m, delta=0.75)


if __name__ == '__main__':
    unittest.main()
