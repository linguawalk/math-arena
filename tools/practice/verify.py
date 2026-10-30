"""생성된 연습 문항을 sympy로 독립 검산 (식으로 읽을 수 있는 문항만)"""
import json, re, sys, glob
import sympy as sp
x, y, a, b = sp.symbols("x y a b")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
def tosym(t):
    t = re.sub(r"÷\s*([\d]*[a-z]+[a-z⁰¹²³⁴⁵⁶⁷⁸⁹]*)", r"÷ (\1)", t)
    t = t.replace("−", "-").replace("×", "*").replace("÷", "/").replace("√", "sqrt")
    t = re.sub(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda mt: "**" + mt.group(1).translate(SUP), t)
    t = t.replace("^", "**")
    t = re.sub(r"(\d)\s*([a-z(])", r"\1*\2", t)
    t = re.sub(r"\)\s*\(", ")*(", t)
    t = re.sub(r"([xyab])\s*\(", r"\1*(", t)
    t = re.sub(r"([xyab])([xyab])", r"\1*\2", t); t = re.sub(r"([xyab])([xyab])", r"\1*\2", t)
    t = re.sub(r"\)([xyab\d])", r")*\1", t)
    return sp.sympify(t, locals={"x": x, "y": y, "a": a, "b": b})
ok = bad = skip = 0
for f in sorted(glob.glob(sys.argv[1])):
    d = json.load(open(f))
    for q in d["questions"]:
        p = q["prompt"]
        try:
            if q["qtype"] == "fill_blank" and p.count("=") == 1 and re.fullmatch(r"[\dxyab²³⁴⁵⁶⁷⁸⁹⁰¹+−\-×÷()/^{} ]+=[\dxyab²³⁴⁵⁶⁷⁸⁹⁰¹+−\-×÷()/^{} ]+", p):
                t = p
                for bl in q["blanks"]: t = t.replace("{{%d}}" % bl["id"], "(" + bl["answers"][0] + ")")
                L, R = t.split("=")
                if sp.simplify(tosym(L) - tosym(R)) == 0: ok += 1
                else: bad += 1; print("BAD", f, q["id"], p, t)
                continue
            mt = re.match(r"방정식 (.+?)의 해는\?$", p)
            if mt and "a" not in mt.group(1):
                L, R = mt.group(1).split("=")
                s = sp.solve(sp.Eq(tosym(L), tosym(R)), x)
                if len(s) == 1 and abs(float(s[0]) - float(sp.Rational(q["answer"]))) < 1e-9: ok += 1
                else: bad += 1; print("BAD", f, q["id"], p, s, q["answer"])
                continue
            mt = re.match(r"연립방정식 (.+?), (.+?)의 해는 x = \{\{1\}\}, y = \{\{2\}\}", p)
            if mt:
                eqs = [sp.Eq(tosym(e.split("=")[0]), tosym(e.split("=")[1])) for e in mt.groups()]
                s = sp.solve(eqs, [x, y])
                want = {x: sp.Rational(q["blanks"][0]["answers"][0]), y: sp.Rational(q["blanks"][1]["answers"][0])}
                if s == want: ok += 1
                else: bad += 1; print("BAD", f, q["id"], p, s)
                continue
            mt = re.match(r"f\(x\) = (.+?)일 때 f\((.+?)\)의 값은\?", p)
            if mt:
                v = tosym(mt.group(1)).subs(x, tosym(mt.group(2)))
                if v == sp.Rational(q["answer"]): ok += 1
                else: bad += 1; print("BAD", f, q["id"], p, v)
                continue
            skip += 1
        except Exception as e:
            skip += 1
print("검산", ok, "불일치", bad, "건너뜀", skip)
