def orion_agent(change_5m, volume_5m_spike, vdelta_1h, oi_trend, price_trend, funding_rate, change_1d):
    """
    Orion Agent Decision Maker
    Returns: 'BigLong', 'ConservativeLong', 'Short', or 'Avoid'
    
    Parameters:
    - change_5m: float (5 min % change)
    - volume_5m_spike: bool (True if volume spiking, else False)
    - vdelta_1h: float (positive for buy pressure, negative for sell)
    - oi_trend: str ('rising', 'falling', or 'flat')
    - price_trend: str ('up' or 'down')
    - funding_rate: float (e.g. 0.01 = +1%)
    - change_1d: float (24h % change)
    """

    # Avoid extreme daily moves
    if abs(change_1d) > 5:
        return "Avoid"

    # Long conditions
    if change_5m > 1 and volume_5m_spike and vdelta_1h > 0 and oi_trend == "rising" and price_trend == "up":
        if 0 <= funding_rate <= 0.03:
            return "BigLong"
        else:
            return "ConservativeLong"

    # Conservative long (weaker signals)
    if change_5m > 0 and vdelta_1h > 0 and oi_trend in ["rising", "flat"]:
        return "ConservativeLong"

    # Short conditions
    if change_5m < -1 and volume_5m_spike and vdelta_1h < 0 and oi_trend == "rising" and price_trend == "down":
        if funding_rate >= -0.05:
            return "Short"
        else:
            return "Avoid"  # avoid overcrowded shorts

    # Default: No clear setup
    return "Avoid"


# === Example Interactive Test ===
if __name__ == "__main__":
    print("Orion Trading Agent")
    print("Enter your values below:")
    
    change_5m = float(input("5m Change (%): "))
    volume_5m_spike = input("5m Volume Spike (y/n): ").lower() == 'y'
    vdelta_1h = float(input("1h Vdelta (positive=buy, negative=sell): "))
    oi_trend = input("OI Trend (rising/falling/flat): ").lower()
    price_trend = input("Price Trend (up/down): ").lower()
    funding_rate = float(input("Funding Rate (e.g. 0.01 = 1%): "))
    change_1d = float(input("24h Change (%): "))

    decision = orion_agent(change_5m, volume_5m_spike, vdelta_1h, oi_trend, price_trend, funding_rate, change_1d)
    print("\n>>> Trade Decision:", decision)
