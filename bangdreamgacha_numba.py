import argparse
import sys
import time

import numpy as np
from numba import njit, prange

# 5★ 单卡阈值 0.005 累积；4★ 0.0075
STEP_5 = 0.005
STEP_4 = 0.0075

@njit(cache=False)
def simulate_one_round_numba(total_5, want_5, want_4, normal, rng_state):
    # rng_state: 128-bit xoroshiro like simple PRNG (we'll implement xorshift64*)
    def rand01(state):
        # xorshift64*
        x = state[0]
        x ^= (x << 13) & 0xFFFFFFFFFFFFFFFF
        x ^= (x >> 7)
        x ^= (x << 17) & 0xFFFFFFFFFFFFFFFF
        state[0] = x
        return (x & 0xFFFFFFFFFFFFFFFF) / 18446744073709551616.0
    def rand_int(state, a, b):
        r = rand01(state)
        return a + int(r * (b - a + 1))

    mask5 = 0
    mask4 = 0
    have5 = 0
    have4 = 0
    draws = 0
    step5_total = STEP_5 * want_5
    step4_total = STEP_4 * want_4

    while True:
        draws += 1
        if normal == 1 and (draws % 50 == 0) and want_5 > 0:
            if total_5 > 0:
                roll = rand_int(rng_state, 1, total_5)
                if 1 <= roll <= want_5:
                    bit = 1 << (roll - 1)
                    if (mask5 & bit) == 0:
                        mask5 |= bit
                        have5 += 1
        else:
            if want_5 > 0:
                r = rand01(rng_state)
                if r < step5_total:
                    idx = int(r / STEP_5)
                    bit = 1 << idx
                    if (mask5 & bit) == 0:
                        mask5 |= bit
                        have5 += 1
            else:
                if want_4 > 0:
                    r = rand01(rng_state)
                    if r < step4_total:
                        idx = int(r / STEP_4)
                        bit = 1 << idx
                        if (mask4 & bit) == 0:
                            mask4 |= bit
                            have4 += 1
                choose = (draws + 100) // 300
                if (have5 + have4 + choose >= want_5 + want_4 and
                    have5 + choose >= want_5 and
                    have4 + choose >= want_4):
                    break
                continue
            if want_4 > 0:
                r = rand01(rng_state)
                if r < step4_total:
                    idx = int(r / STEP_4)
                    bit = 1 << idx
                    if (mask4 & bit) == 0:
                        mask4 |= bit
                        have4 += 1
        choose = (draws + 100) // 300
        if (have5 + have4 + choose >= want_5 + want_4 and
            have5 + choose >= want_5 and
            have4 + choose >= want_4):
            break
    return draws

@njit(parallel=True, cache=False)
def simulate_batch_numba(total_5, want_5, want_4, normal, simulations, seed):
    # 预分配结果
    out = np.empty(simulations, dtype=np.int32)
    # 为每个并行迭代生成独立种子（简单可重复）
    for i in prange(simulations):
        # 简单 splitmix64 派生
        s = seed + 0x9E3779B97F4A7C15 * (i + 1)
        s ^= (s >> 30)
        s *= 0xBF58476D1CE4E5B9
        s &= 0xFFFFFFFFFFFFFFFF
        s ^= (s >> 27)
        s *= 0x94D049BB133111EB
        s &= 0xFFFFFFFFFFFFFFFF
        s ^= (s >> 31)
        rng_state = np.array([s & 0xFFFFFFFFFFFFFFFF], dtype=np.uint64)
        out[i] = simulate_one_round_numba(total_5, want_5, want_4, normal, rng_state)
    return out

def summarize(counts: np.ndarray):
    counts.sort()
    n = counts.size
    total = int(counts.sum())
    exp = total / n
    med = int(counts[n//2])
    p90 = int(counts[int(n*0.9)])
    worst = int(counts[-1])
    return exp, med, p90, worst

def parse_args():
    ap = argparse.ArgumentParser(description='抽卡期望模拟器 - Numba 高速版')
    ap.add_argument('--t5', '--total5', dest='total5', type=int, required=True)
    ap.add_argument('--w5', '--want5', dest='want5', type=int, required=True)
    ap.add_argument('--w4', '--want4', dest='want4', type=int, required=True)
    ap.add_argument('-n', '--normal', type=int, choices=[0,1], default=1)
    ap.add_argument('-s', '--sims', type=int, default=100000)
    ap.add_argument('--seed', type=np.int64, default=123456789)
    return ap.parse_args()

class Namespace:
    def __init__(self, **kw):
        self.__dict__.update(kw)

def interactive_inputs():
    print('欢迎使用抽卡期望模拟器(Numba版, 交互模式)!')
    total5 = int(input('请输入当期5星卡的总数量: '))
    if total5 < 0: raise SystemExit('必须>=0')
    want5 = 0
    if total5 > 0:
        want5 = int(input('请输入想要抽取的当期5星卡数量: '))
        if want5 < 0 or want5 > total5:
            raise SystemExit('范围非法')
    want4 = int(input('请输入想要抽取的当期4星卡数量: '))
    if want4 < 0: raise SystemExit('必须>=0')
    normal = int(input('是否为常驻池（是否有50小保底）（1: 是，0: 否）: '))
    if normal not in (0,1): raise SystemExit('输入错误')
    sims = int(input('请输入模拟次数（推荐10000000次以上）: '))
    if sims < 100: raise SystemExit('>=100')
    seed = int(time.time() * 1000) & 0x7FFFFFFF
    return Namespace(total5=total5, want5=want5, want4=want4, normal=normal, sims=sims, seed=seed)

def main():
    if len(sys.argv) == 1:
        args = interactive_inputs()
    else:
        args = parse_args()
    if args.want5 > args.total5: raise SystemExit('想要5星不能超过总数')
    print('----------------输入参数----------------')
    print(f'当期5星数量: {args.total5}')
    print(f'想要的当期5星数量: {args.want5}')
    print(f'想要的当期4星数量: {args.want4}')
    print('50小保底: {}'.format('是' if args.normal==1 else '否'))
    print(f'模拟次数: {args.sims}')
    print(f'随机种子: {args.seed}')
    start = time.time()
    arr = simulate_batch_numba(args.total5, args.want5, args.want4, args.normal, args.sims, int(args.seed))
    exp, med, p90, worst = summarize(arr)
    dur = time.time()-start
    print('----------------模拟结果----------------')
    print(f'期望抽卡次数: {exp}')
    print(f'中位数抽卡次数: {med}')
    print(f'90%玩家在以下抽数内集齐: {p90}')
    print(f'非酋至多抽卡次数: {worst}')
    print(f'总耗时: {dur:.3f} 秒')

if __name__ == '__main__':
    try:
        main()
    except ModuleNotFoundError:
        print('需要先安装 numba: pip install numba')
