# Pipeline map — QuantLib edition

> Exercise 1, Phase 0.1 (Quant Mentor). The 7-stage model research→production pipeline, mapped to
> real QuantLib types — what check each stage gives me for free, what gap I have to fill myself.
> Public-library references only (clean-room rule) — no work-system references.
>
> Reference lesson: `knowledge/lessons/P0-quant-roles-and-pipeline.md` in the Quant Mentor vault.

## 1. Model spec / choice

**QuantLib type(s):**
Alternative pricing engine for the same instrument (e.g Balck vs tree and Monte Carlo and etc)
**Check I get free:**
Nothing is free but we can use Quantlib model

**Gap I fill myself:**
I need to decide what pricing engine I need to assign to the ISIN, we can assign wrong model but it is financially wrong but technically correct

## 2. Market data

**QuantLib type(s):**
Calender, Daycounter, simple quote

**Check I get free:**
It is well tested, not need break your head to test these.

**Gap I fill myself:**
Nothing checks that a quote was genuinely available as of the evaluation date — I could accidentally feed in a rate from the future and QuantLib wouldn't object. That discipline is on me.

## 3. Curve / model construction

**QuantLib type(s):**
We can use RateHelper, DepositRateHelperm swapratehelper

**Check I get free:**
I dont have to check whether my curve reproduce 4.50% 1 year correcly, it will taken care by Quantlib.

**Gap I fill myself:**
It can't do whether the curve is correct inbetween those points.

## 4. Instrument pricing

**QuantLib type(s):**
fixedrate bond
DiscountingBondEngine

**Check I get free:**
We can choose which curve to be discounted

**Gap I fill myself:**
We need to decide.

## 5. Risk & Greeks

**QuantLib type(s):**
simpleQuote.setValue() + re-read NPV()
**Check I get free:**
Bump and revalue is nearly automatic
**Gap I fill myself:**
Not built in 

## 6. P&L explain / validation

**QuantLib type(s):**
None

**Check I get free:**
Nothing

**Gap I fill myself:**
I have to figure out myself later

## 7. Production

**QuantLib type(s):**
Settings.instance().evaluationDate

**Check I get free:**
not sure

**Gap I fill myself:**
No golden value