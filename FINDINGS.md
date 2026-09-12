# Findings

76 items, 372 threads retrieved, Hacker News, 2021–2026. Read `METHOD.md` first;
it says what this corpus cannot support, and the answer includes every frequency
claim you might be tempted to make from the counts below.

Every quote is verifiable: `python3 check_quotes.py` confirms that each one appears
in the corpus, attributed to the right pseudonym.

---

## 1. The warning that cannot be obeyed

The largest code in the corpus, and the most widely spread — 14 items across 10
threads — is not about people deciding to ignore a warning. It is about people
meeting a warning that has no compliant answer.

The condition recurs with a specific shape: a service on a LAN address, an IoT
device on someone's Wi-Fi, an internal hostname, an air-gapped registry. The
public-CA path these warnings presuppose is not expensive in these situations. It
is unavailable.

> It's becoming increasingly troublesome these days to run a service on insecure
> HTTP. Doubly so to run a service with a self signed certificate, which gets
> treated as a sign of evil intent by all browsers. Creating your own CA cert and
> installing it as a trust root is possible, but bothersome. It's implausible for
> non technical people to learn to do this.
> — A144 · [26584730](https://news.ycombinator.com/item?id=26584730)

"A sign of evil intent" is doing something precise. The browser's warning carries
one meaning — someone may be attacking you — and the situation has another —
this is my printer. The interface has no way to say the second, so it says the
first, and the person is left to reconcile the two.

This matters for how the resulting behaviour should be read. When someone proceeds
here, they are not discounting a risk they understand. They are resolving a
mismatch between what the warning can express and what is actually happening.

## 2. The organisation makes the secure path impractical, then the insecure one becomes policy

Where a compliant option does exist, the obstacle described is almost never
technical.

> Unfortunately, enterprises are intensely risk averse. I worked at a place where
> we could only generate proper certs by manually submitting a ticket to IT and
> waiting probably days to get it back, giving us zero hope of applying meaningful
> automation. Getting certs from a proper CA was absolutely forbidden, despite our
> lobbying, so in a lot of cases self-signed certs were the only option if we
> wanted to automate.
> — A117 · [36506195](https://news.ycombinator.com/item?id=36506195)

Immediately below it, in the same thread:

> Where I work it’s months, and fights, and maybe even several meetings. And that’s
> only if you fill out the correct form the exact right way. Any slight deviation
> and your ticket is closed weeks after you opened it with the field you got wrong.
> — A118 · [36506755](https://news.ycombinator.com/item?id=36506755)

Both describe a risk-averse security process producing a less secure outcome than
no process. The prohibition on proper certificates is what put self-signed
certificates into production. Note that this is two items in one thread, so read
it as an illustration rather than as a distribution.

## 3. Sometimes the goal is the absence of the warning, not the presence of security

The clearest item in the corpus, and the one that most deserves to be read twice:

> I have one supplier that uses letsencrypt to generate a wildcard certificate,
> then distributes it as part of a software update to thousands of machines in
> hundreds of companies across the world. The exact same certificate and key. But
> it gets rid of the red X in a browser so tick
> — A127 · [36508087](https://news.ycombinator.com/item?id=36508087)

A private key shipped to thousands of machines is worse than the self-signed
certificate it replaced — the same poster says so in the next sentence. What it
buys is a browser that stops complaining.

The indicator became the target. Everything downstream of that substitution looks
like compliance and is not, and no warning in the system is capable of noticing,
because from the browser's point of view nothing is wrong.

## 4. Practitioners predict the habituation themselves

The corpus does not need an outside analyst to point out that unsatisfiable
warnings train people to dismiss warnings. The participants say it, unprompted, as
an argument against a design:

> Second, it reduces your security because your users will inevitably learn to
> ignore certificate errors.  Thirdly, you'll never stop the certificate errors.
> — A122 · [36507168](https://news.ycombinator.com/item?id=36507168)

And observed in a specific product:

> the auto-generated self-signed RDP server certificates are only valid for 6
> months for some reason, so users eventually learn to just ignore these warnings.
> — A52 · [41436340](https://news.ycombinator.com/item?id=41436340)

"Six months for some reason" is the whole mechanism in five words. A default nobody
chose deliberately sets the frequency of an unavoidable warning, and the frequency
determines what the warning comes to mean.

The most useful statement of the general case arrived by analogy, about a daycare
rather than a network:

> There'll be a sign that says "Peanut free zone" and everyone will read it and
> respect it.  Then there'll be a sign that says "Please be sure to pick your kid
> up by x o'clock." And everyone will read it and respect it and silently stop
> looking at it cause they know.
> — A902 · [45533836](https://news.ycombinator.com/item?id=45533836)

## 5. The control that teaches the opposite lesson

The second-largest code, 13 items across 4 threads, is about security controls
training the behaviour they punish. Phishing training dominates it, and the
complaint is consistently mechanical rather than attitudinal.

> My university routinely sends notifications about required annual phishing
> training that violate almost every point in the training about how to avoid
> getting phished. Its been happening for years. Urgency. Appeals to authority.
> Grammatical errors. Mystery click-me links that go outside the domain to training
> service providers that we do not use in any other context.
> — A925 · [45534755](https://news.ycombinator.com/item?id=45534755)

The wider version of the same observation:

> Corporations outsource almost every single tool used by their employees and train
> them to cough up their corporate credentials no matter what url the browser
> identifies. In essence, they phish their employees 100 times a day.
> — A922 · [45532736](https://news.ycombinator.com/item?id=45532736)

This is the sharpest design claim available from the corpus. The advice —
*check the domain* — is not wrong. It is inapplicable, because the organisation has
already made its legitimate traffic indistinguishable from the attack. The training
asks people to apply a test that their employer has arranged to fail.

And the measurement is on the same footing as the advice:

> A couple of times, I got emails that seemed suspicious, but I figured I would
> click the link to investigate further. I was on high alert and would not have
> entered login credentials or opened an executable or anything like that, I just
> wanted to check it out and see.  Of course, it was a phishing audit and I failed.
> — A834 · [45532990](https://news.ycombinator.com/item?id=45532990)

Someone who investigated a suspicious email carefully and disclosed nothing is
recorded as a failure. Whatever that metric is counting, it is not the thing the
programme exists to prevent.

The end state, reported as an outcome rather than a prediction:

> The phishing training in my workplace is so odious, and the consequences for
> failing a test are high enough, that it's led to everyone just ignoring all
> unexpected communications. Better to ignore it all than to risk making a mistake.
> — A550 · [44941422](https://news.ycombinator.com/item?id=44941422)

One thread in this code argues that such programmes exist to move blame onto the
individual rather than to reduce risk. It is a coherent argument and it is **four
items in a single thread**, so it is recorded in the codebook and not presented
here as a finding.

## 6. What is almost absent

Worth stating because the study went looking for it. The framing this work started
from — competent people weighing a risk and choosing to proceed — is present, but
it is small and thin: 6 items, one per thread, no sustained discussion anywhere.

There are two readings and this corpus cannot separate them. Either the deliberate
risk calculus is rarer than the security literature's framing assumes, or it is
simply not the kind of thing people write posts about, while unsatisfiable warnings
and absurd training are. **The second is more likely than the first** — an
unremarkable decision generates no text — and no count here should be read as
evidence for the first.

What the corpus does support is narrower and, I think, more useful: when these
practitioners explain proceeding past a security warning, they overwhelmingly
explain it as a property of the situation they were placed in rather than as a
judgement they made.

---

## What this converges with

[`the-human-element`](https://github.com/uxrhimanshu/the-human-element) examined
10,042 public security incidents and found a large share running through
interfaces, defaults and warnings that set people up to fail. It could not say why
anyone proceeded, because incident records store outcomes.

These 76 items are an answer in practitioners' own words, and they point at the
same place from the other side. The quantitative study found that warnings fail at
scale. This one finds practitioners describing, without being asked, the mechanisms
by which that happens: a warning with no compliant answer, a process that forbids
the compliant answer, a fix whose actual objective is the silence of the indicator,
and a training programme that teaches the habit it punishes.

Neither study establishes a frequency. Together they do something more modest and
harder to dismiss: a pattern found in incident records is described independently,
and unprompted, by the people who work inside it.
