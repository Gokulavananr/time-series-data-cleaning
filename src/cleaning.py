"""Reusable helpers for cleaning time series data."""
import numpy as np
import pandas as pd


def load_series(path, date_col="Month", value_col="Passengers", freq="MS"):
    """Load a CSV into a clean, sorted, regular-frequency Series.

    Parses dates, sorts, drops duplicate timestamps and inserts NaN for
    missing timestamps so the index is complete.
    """
    df = pd.read_csv(path, parse_dates=[date_col])
    s = df.set_index(date_col)[value_col].sort_index()
    s = s[~s.index.duplicated(keep="first")]
    return s.asfreq(freq)


def missing_report(s):
    """Return count and percentage of missing values."""
    n = int(s.isna().sum())
    return {"missing": n, "percent": round(100 * n / len(s), 2)}


def fill_missing(s, method="time"):
    """Fill NaNs using 'ffill', 'bfill', 'linear' or 'time' interpolation."""
    if method == "ffill":
        return s.ffill()
    if method == "bfill":
        return s.bfill()
    if method in ("linear", "time"):
        return s.interpolate(method=method)
    raise ValueError(f"Unknown method: {method}")


def outliers_zscore(s, threshold=3.0):
    """Boolean mask of points whose |z-score| exceeds threshold."""
    z = (s - s.mean()) / s.std()
    return z.abs() > threshold


def outliers_iqr(s, k=1.5):
    """Boolean mask of points outside [Q1 - k*IQR, Q3 + k*IQR]."""
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (s < q1 - k * iqr) | (s > q3 + k * iqr)


def outliers_rolling_median(s, window=12, threshold=3.5):
    """Mask of points far from the rolling median (robust to trend/seasonality).

    Distance is scaled by the rolling median absolute deviation (MAD).
    """
    med = s.rolling(window, center=True, min_periods=1).median()
    resid = s - med
    mad = resid.abs().rolling(window, center=True, min_periods=1).median()
    return (resid.abs() / (1.4826 * mad.replace(0, np.nan))) > threshold


def treat_outliers(s, mask):
    """Replace flagged outliers with NaN and interpolate over them."""
    out = s.copy()
    out[mask] = np.nan
    return out.interpolate(method="time")


def smooth(s, window=3):
    """Centered rolling-mean smoothing."""
    return s.rolling(window, center=True, min_periods=1).mean()


def resample_series(s, rule="QS", agg="sum"):
    """Resample to a new frequency (e.g. 'QS' quarterly, 'YS' yearly)."""
    return getattr(s.resample(rule), agg)()


def clean_pipeline(path, window=12):
    """Full pipeline: load -> fill gaps -> flag outliers -> interpolate."""
    s = fill_missing(load_series(path), "time")
    return treat_outliers(s, outliers_rolling_median(s, window=window))
