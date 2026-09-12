# Codebook

Twelve codes over 76 screened items. One code per item: where an item could carry
two, it is coded for the thing it is *evidence of*, not everything it mentions.
`coded.csv` joins to `corpus/corpus.csv` on `item_id`.

Read the **threads** column before the **items** column. A code spread across many
threads is a pattern in the corpus; a code concentrated in one thread is one
argument that happened once, and is reported that way in `FINDINGS.md`.

| code | items | threads |
|---|---:|---:|
| `warning-cannot-be-satisfied` | 14 | 10 |
| `control-teaches-opposite` | 13 | 4 |
| `workaround-becomes-standard` | 8 | 6 |
| `trust-store-unmaintainable` | 7 | 3 |
| `sanctioned-mitm` | 7 | 2 |
| `informed-acceptance` | 6 | 6 |
| `habituation-by-design` | 5 | 4 |
| `org-friction-as-cause` | 4 | 2 |
| `control-as-liability-transfer` | 4 | 1 |
| `removing-the-warning-is-the-goal` | 3 | 2 |
| `designing-against-click-through` | 3 | 3 |
| `vendor-undermines-trust` | 2 | 2 |

---

### `warning-cannot-be-satisfied`

The warning names a condition the person has no way to resolve where they are
standing: a service on a LAN address, an IoT device, an internal hostname, an
air-gapped network. The public-CA path is structurally unavailable, not merely
inconvenient.

**Include** when the item describes the *unavailability* of a compliant option.
**Exclude** when a compliant option exists and was rejected on cost or effort —
that is `org-friction-as-cause` or `workaround-becomes-standard`.

### `habituation-by-design`

The participant states that the arrangement teaches people to ignore warnings.
The distinguishing feature is that this is said as a *predictable consequence of
the design*, not as a complaint about users.

**Include** statements of the form "this will train people to click through".
**Exclude** an individual reporting that they personally ignored one warning —
that is `informed-acceptance`.

### `org-friction-as-cause`

The employer's own process — tickets, forms, prohibitions, waiting periods — makes
the secure path impractical, and the insecure path is chosen as a result.

**Include** only when the process and the outcome are both stated. A complaint
about IT with no consequence attached is `no-account` at screening.

### `workaround-becomes-standard`

A workaround is described as the settled, normal practice rather than an
exception: self-signed certificates as policy, `insecureSkipVerify` in a committed
config, an internal CA installed on every device, a public domain bought to point
at private addresses.

### `removing-the-warning-is-the-goal`

The objective is the disappearance of the indicator rather than the security
property it indicates. This is the sharpest code in the set and the rarest; apply
it only where the item makes the substitution explicit.

### `sanctioned-mitm`

An employer, school or vendor deliberately intercepts TLS, so certificate warnings
become an expected feature of the working day and are resolved by installing the
interceptor's root certificate.

### `control-teaches-opposite`

A security control trains the behaviour it exists to prevent. The dominant instance
is phishing training delivered by emails that are themselves indistinguishable from
phishing, but the code is not specific to phishing.

**Include** when the mechanism is named. **Exclude** generalised dislike of
training, which is `no-account`.

### `control-as-liability-transfer`

The control is described as existing to move blame onto the individual rather than
to reduce risk. **All four items are in one thread** — treat as one argument, not a
finding about the corpus.

### `informed-acceptance`

The person understands the risk and proceeds deliberately, giving a reason. This is
the code that the study's original framing expected to dominate. It does not.

### `trust-store-unmaintainable`

The recommended fix — distribute your own CA — is reported as not surviving contact
with real device fleets: BYOD, mobile, VMs that do not inherit the host store, Java
keystores, per-language trust configuration.

### `vendor-undermines-trust`

A vendor installs its own root certificate, or ships a private key, to avoid
friction — transferring the cost from itself to the user's trust store.

### `designing-against-click-through`

Someone is explicitly trying to build or find a warning that *cannot* be dismissed,
treating dismissibility as the defect.

---

## What changed at review

*To be completed by the author.* The first pass was LLM-proposed (see `METHOD.md`);
this section should record which codes were renamed, merged, split or rejected on
human review, and how many items were recoded. Until it is filled in, the codebook
is a first pass that has not yet been corrected, and should be read as one.

Specific things worth arguing with:

- `removing-the-warning-is-the-goal` and `workaround-becomes-standard` may be one
  code. They were kept apart because the first is about *motive* and the second
  about *practice*, but only three items carry the first.
- `control-as-liability-transfer` sits in a single thread and may not deserve to be
  a code at all.
- `warning-cannot-be-satisfied` is the largest code and may be doing too much work;
  it could plausibly split into "no compliant option exists" and "a compliant option
  exists but not for this deployment shape".
