"""레벨1 '더 연습하기' 문제 은행 생성 공통 도구."""
import json, random, os
from fractions import Fraction as F
from math import gcd, isqrt

SITE = "/home/claude/site"
SUPD = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
def sup(n): return str(n).translate(SUPD)
def m(x):
    """화면 표기: 음수 부호를 −로"""
    return str(x).replace("-", "−")
def par(x):
    """음수면 괄호"""
    return f"({m(x)})" if x < 0 else str(x)
def fs(fr):
    fr = F(fr)
    return str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"
def fm(fr): return m(fs(fr))
def alts(x):
    s = str(x)
    out = [s]
    if s.startswith("-"): out.append("−" + s[1:])
    return out

def num(prompt, answer, expl, hint=None, fmt=None):
    if isinstance(answer, F):
        a = fs(answer); fmt = fmt or ("integer" if answer.denominator == 1 else "fraction")
    else:
        a = str(answer); fmt = fmt or "integer"
    return {"type": "question", "qtype": "numeric", "prompt": prompt, "answer": a,
            "answer_format": fmt, "tolerance": 0, "hint": hint, "explanation": expl}

def fill(prompt, blanks, expl, hint=None, unordered=None):
    n = prompt.count("{{")
    assert n == len(blanks), (prompt, blanks)
    for i in range(1, n + 1): assert "{{%d}}" % i in prompt, prompt
    q = {"type": "question", "qtype": "fill_blank", "prompt": prompt,
         "blanks": [{"id": i + 1, "answers": b if isinstance(b, list) else alts(b)} for i, b in enumerate(blanks)],
         "hint": hint, "explanation": expl}
    if unordered: q["unordered_groups"] = unordered
    return q

def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def fstr(f): return " × ".join(f"{p}{sup(e) if e > 1 else ''}" for p, e in sorted(f.items()))
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def is_prime(n): return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))

def build(templates, per=6, seed=1, tries=400):
    """templates: [(제목, 함수(rng)->question)] → 같은 문항 없이 per개씩"""
    pool = []
    for g, (title, fn) in enumerate(templates, 1):
        rng = random.Random(seed * 1000 + g); seen = set(); k = 0
        for _ in range(tries):
            q = fn(rng)
            if q is None or q["prompt"] in seen: continue
            seen.add(q["prompt"]); k += 1
            assert q["explanation"] and len(q["explanation"]) >= 20, q
            q["id"] = f"g{g}-{k}"; q["group"] = g; q["stage"] = "practice"
            pool.append(q)
            if k == per: break
        assert k == per, (title, k)
    return pool

def write(c, ch, l, templates, per=6, seed=1):
    d = f"{SITE}/content/level1/{c}/{ch}"
    lesson = json.load(open(f"{d}/{l}.json"))
    pool = build(templates, per, seed)
    out = {"schema_version": "1.0", "site": "math-arena", "level": 1,
           "course": lesson["course"], "chapter": lesson["chapter"], "lesson": lesson["lesson"],
           "practice": {"id": lesson["lesson"]["id"] + "-p", "set_size": 10,
                        "groups": [t for t, _ in templates]},
           "questions": pool}
    fn = "p" + l[1:] + ".json"
    json.dump(out, open(f"{d}/{fn}", "w"), ensure_ascii=False, indent=1)
    # chapter.json에 연결
    cj = f"{d}/chapter.json"; chap = json.load(open(cj))
    for les in chap["lessons"]:
        if les["file"] == l + ".json": les["practice"] = {"file": fn, "questions": len(pool)}
    json.dump(chap, open(cj, "w"), ensure_ascii=False, indent=2)
    return len(pool)

def _bat(n):
    n = abs(int(n))
    if n == 0: return True
    if n % 10: return n % 10 in (1, 3, 6, 7, 8)
    return True  # 십·백·천
def j(n, pair):
    """숫자 뒤 조사: j(12,'와과') → '12와'"""
    a, b = pair[0], pair[1:]
    return f"{n}{b if _bat(n) else a}"
def ro(n):
    k = abs(int(n))
    rieul = (k % 10 in (1, 7, 8)) if k % 10 else False
    return f"{n}{'로' if (not _bat(n) or rieul) else '으로'}"
bat = _bat
