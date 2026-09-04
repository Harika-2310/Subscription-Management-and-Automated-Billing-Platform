# =========================================================
# TAX RATES
# =========================================================

TAX_RATES = {
    "IN": {
        "default": 18.0
    },
    "US": {
        "default": 0.0,
        "CA": 7.25,
        "NY": 8.875,
        "TX": 6.25
    },
    "UK": {
        "default": 20.0
    },
    "AU": {
        "default": 10.0
    },
    "CA": {
        "default": 5.0,
        "ON": 13.0,
        "QC": 14.975
    }
}


# =========================================================
# GET TAX RATE
# =========================================================

def get_tax_rate(
    country: str,
    region: str = None
):
    """
    Return tax rate based on country and region.
    """

    country = country.upper()

    if country not in TAX_RATES:
        return 0.0

    country_rates = TAX_RATES[country]

    if region:
        region = region.upper()

        if region in country_rates:
            return country_rates[region]

    return country_rates.get("default", 0.0)


# =========================================================
# CALCULATE TAX
# =========================================================

def calculate_tax(
    amount: float,
    country: str,
    region: str = None
):
    """
    Calculate tax amount for a given price.
    """

    if amount < 0:
        raise ValueError("Amount cannot be negative")

    tax_rate = get_tax_rate(
        country=country,
        region=region
    )

    tax_amount = amount * (tax_rate / 100)

    total_amount = amount + tax_amount

    return {
        "subtotal": round(amount, 2),
        "tax_rate": tax_rate,
        "tax_amount": round(tax_amount, 2),
        "total": round(total_amount, 2)
    }