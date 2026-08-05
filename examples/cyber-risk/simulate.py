#!/usr/bin/env python3
"""Reproduce the synthetic cyber-risk worked example.

The program implements a one-year posterior-predictive generative model for
credential compromise, public-facing exploitation, lateral movement,
ransomware, exfiltration, recovery impairment, and four loss dimensions.

All inputs are synthetic teaching values. They are not estimates for any real
organisation and must not be used as a control baseline or risk acceptance
threshold.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
from dataclasses import asdict, dataclass
from typing import Final

import numpy as np
import scipy
from scipy.special import betaincinv


DEFAULT_SAMPLES: Final = 1_000_000
DEFAULT_SEED: Final = 20260806


@dataclass(frozen=True)
class Scenario:
    key: str
    label: str
    identity_beta_a: float
    identity_beta_b: float
    identity_hardening: bool = False
    exposure_reduction: bool = False
    detection_containment: bool = False
    recovery_resilience: bool = False


SCENARIOS: Final = (
    Scenario("m1_pretest", "M1 pre-test", 3.0, 27.0),
    Scenario("m2_posttest", "M2 post-test", 8.0, 14.0),
    Scenario("identity", "Identity hardening", 1.0, 25.0, identity_hardening=True),
    Scenario("exposure", "Exposure reduction", 8.0, 14.0, exposure_reduction=True),
    Scenario("detection", "Detection + containment", 8.0, 14.0, detection_containment=True),
    Scenario("recovery", "Recovery resilience", 8.0, 14.0, recovery_resilience=True),
    Scenario(
        "combined",
        "Combined programme",
        1.0,
        25.0,
        identity_hardening=True,
        exposure_reduction=True,
        detection_containment=True,
        recovery_resilience=True,
    ),
)


RISK_APPETITE: Final = {
    "p_financial_ge_aud5m": 0.0025,
    "p_outage_ge_24h": 0.0020,
    "p_records_ge_10000": 0.0030,
    "p_care_delay_ge_50": 0.0050,
}


@dataclass(frozen=True)
class Result:
    key: str
    label: str
    identity_bypass_mean: float
    identity_bypass_q05: float
    identity_bypass_q50: float
    identity_bypass_q95: float
    p_identity_compromise: float
    p_public_exploit: float
    p_both_entries: float
    p_lateral_movement: float
    p_ransomware: float
    p_exfiltration: float
    p_material_incident: float
    expected_financial_aud_m: float
    financial_var95_aud_m: float
    financial_es95_aud_m: float
    p_financial_ge_aud5m: float
    p_outage_ge_24h: float
    p_records_ge_10000: float
    p_care_delay_ge_50: float
    passes_all_appetite_limits: bool


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def lognormal_from_standard_normal(
    median: float | np.ndarray,
    sigma: float | np.ndarray,
    standard_normal: np.ndarray,
) -> np.ndarray:
    return np.asarray(median) * np.exp(np.asarray(sigma) * standard_normal)


def build_common_random_draws(samples: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Create fixed, scenario-shared random arrays.

    Uniform rows, in order: campaign, identity parameter quantile, identity
    entry, public exploit, lateral movement, detection blind spot, ransomware,
    exfiltration, and recovery impairment.

    Normal rows, in order: outage duration, record count, common incident
    response cost, rebuild cost, downtime rate, privacy-cost multiplier, and
    care-delay intensity.
    """

    rng = np.random.Generator(np.random.PCG64(seed))
    uniforms = rng.random((9, samples))
    normals = rng.standard_normal((7, samples))
    return uniforms, normals


def simulate_scenario(
    scenario: Scenario,
    uniforms: np.ndarray,
    normals: np.ndarray,
) -> Result:
    samples = uniforms.shape[1]

    # Epistemic draw: uncertainty in bypass probability for the active
    # help-desk identity-recovery regime. The same uniform quantile is mapped
    # through each scenario's Beta law to support paired comparisons.
    identity_bypass = betaincinv(
        scenario.identity_beta_a,
        scenario.identity_beta_b,
        uniforms[1],
    )

    # Aleatory annual state and entry events. Conditional Poisson thinning
    # gives P(at least one successful identity attack) = 1 - exp(-lambda*q).
    campaign = uniforms[0] < 0.18
    identity_attempt_rate = np.where(campaign, 1.20, 0.25)
    p_identity_entry = 1.0 - np.exp(-identity_attempt_rate * identity_bypass)
    identity_compromise = uniforms[2] < p_identity_entry

    p_public_exploit = np.where(campaign, 0.14, 0.03)
    if scenario.exposure_reduction:
        p_public_exploit = np.where(campaign, 0.03, 0.005)
    public_exploit = uniforms[3] < p_public_exploit

    both_entries = identity_compromise & public_exploit
    entry_conditions = [
        both_entries,
        identity_compromise & ~public_exploit,
        ~identity_compromise & public_exploit,
    ]
    if scenario.identity_hardening:
        p_lateral = np.select(
            entry_conditions,
            [0.32, 0.16, 0.22],
            default=0.001,
        )
    else:
        p_lateral = np.select(
            entry_conditions,
            [0.58, 0.40, 0.32],
            default=0.002,
        )
    lateral_movement = uniforms[4] < p_lateral

    # The blind-spot state is a second common cause: when active it increases
    # both ransomware and exfiltration conditional on lateral movement.
    p_blind_spot = 0.05 if scenario.detection_containment else 0.18
    detection_blind_spot = uniforms[5] < p_blind_spot
    p_ransomware = np.where(detection_blind_spot, 0.62, 0.38) + np.where(campaign, 0.06, 0.0)
    p_exfiltration = np.where(detection_blind_spot, 0.52, 0.26) + np.where(campaign, 0.05, 0.0)
    ransomware = lateral_movement & (uniforms[6] < np.minimum(p_ransomware, 0.95))
    exfiltration = lateral_movement & (uniforms[7] < np.minimum(p_exfiltration, 0.95))

    p_recovery_impairment = 0.06 if scenario.recovery_resilience else 0.28
    recovery_impairment = ransomware & (uniforms[8] < p_recovery_impairment)

    # Loss vector. Only financial components are added. Outage hours, records,
    # and care-delay episodes remain separate coordinates.
    outage_median = np.where(
        recovery_impairment,
        36.0 if scenario.recovery_resilience else 72.0,
        8.0 if scenario.recovery_resilience else 14.0,
    )
    outage_sigma = np.where(recovery_impairment, 0.55, 0.50)
    outage_hours = np.where(
        ransomware,
        lognormal_from_standard_normal(outage_median, outage_sigma, normals[0]),
        0.0,
    )
    records_exposed = np.where(
        exfiltration,
        np.clip(lognormal_from_standard_normal(30_000.0, 1.0, normals[1]), 100.0, 500_000.0),
        0.0,
    )
    material_incident = ransomware | exfiltration
    incident_response_cost = np.where(
        material_incident,
        lognormal_from_standard_normal(0.75, 0.55, normals[2]),
        0.0,
    )
    rebuild_cost = np.where(
        ransomware,
        lognormal_from_standard_normal(1.40, 0.60, normals[3]),
        0.0,
    )
    downtime_rate = lognormal_from_standard_normal(0.055, 0.35, normals[4])
    privacy_cost_multiplier = lognormal_from_standard_normal(1.0, 0.30, normals[5])
    privacy_response_cost = np.where(
        exfiltration,
        0.35 + records_exposed * 0.00004 * privacy_cost_multiplier,
        0.0,
    )
    financial_loss = (
        incident_response_cost
        + rebuild_cost
        + outage_hours * downtime_rate
        + privacy_response_cost
    )
    care_delay_episodes = np.where(
        ransomware,
        np.rint(outage_hours * lognormal_from_standard_normal(12.0, 0.40, normals[6])),
        0.0,
    )

    sorted_financial = np.sort(financial_loss)
    var95_index = max(0, math.ceil(0.95 * samples) - 1)
    tail_count = max(1, math.ceil(0.05 * samples))
    financial_var95 = float(sorted_financial[var95_index])
    financial_es95 = float(np.mean(sorted_financial[-tail_count:]))

    threshold_probabilities = {
        "p_financial_ge_aud5m": float(np.mean(financial_loss >= 5.0)),
        "p_outage_ge_24h": float(np.mean(outage_hours >= 24.0)),
        "p_records_ge_10000": float(np.mean(records_exposed >= 10_000.0)),
        "p_care_delay_ge_50": float(np.mean(care_delay_episodes >= 50.0)),
    }
    appetite_pass = all(
        threshold_probabilities[key] <= limit
        for key, limit in RISK_APPETITE.items()
    )

    identity_quantiles = np.quantile(
        identity_bypass,
        [0.05, 0.50, 0.95],
        method="inverted_cdf",
    )

    return Result(
        key=scenario.key,
        label=scenario.label,
        identity_bypass_mean=float(np.mean(identity_bypass)),
        identity_bypass_q05=float(identity_quantiles[0]),
        identity_bypass_q50=float(identity_quantiles[1]),
        identity_bypass_q95=float(identity_quantiles[2]),
        p_identity_compromise=float(np.mean(identity_compromise)),
        p_public_exploit=float(np.mean(public_exploit)),
        p_both_entries=float(np.mean(both_entries)),
        p_lateral_movement=float(np.mean(lateral_movement)),
        p_ransomware=float(np.mean(ransomware)),
        p_exfiltration=float(np.mean(exfiltration)),
        p_material_incident=float(np.mean(material_incident)),
        expected_financial_aud_m=float(np.mean(financial_loss)),
        financial_var95_aud_m=financial_var95,
        financial_es95_aud_m=financial_es95,
        passes_all_appetite_limits=appetite_pass,
        **threshold_probabilities,
    )


def probability_mcse(probability: float, samples: int) -> float:
    return math.sqrt(probability * (1.0 - probability) / samples)


def render_markdown(results: list[Result], samples: int, seed: int) -> str:
    manifest = (
        f"Manifest: samples={samples:,}; seed={seed}; NumPy={np.__version__}; "
        f"SciPy={scipy.__version__}; Python={platform.python_version()}"
    )
    header = (
        "| Scenario | P(material incident) | E[financial] A$M | VaR95 A$M | "
        "ES95 A$M | P(financial ≥ A$5M) | P(outage ≥24h) | "
        "P(records ≥10k) | P(care delay ≥50) | Appetite |"
    )
    row_template = (
        "| {label} | {incident:.3%} | {mean:.3f} | {var:.3f} | {es:.3f} | "
        "{fin:.3%} | {outage:.3%} | {records:.3%} | {care:.3%} | {appetite} |"
    )
    lines = [
        manifest,
        "",
        header,
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            row_template.format(
                label=result.label,
                incident=result.p_material_incident,
                mean=result.expected_financial_aud_m,
                var=result.financial_var95_aud_m,
                es=result.financial_es95_aud_m,
                fin=result.p_financial_ge_aud5m,
                outage=result.p_outage_ge_24h,
                records=result.p_records_ge_10000,
                care=result.p_care_delay_ge_50,
                appetite="Pass" if result.passes_all_appetite_limits else "Fail",
            )
        )

    lines.extend(
        [
            "",
            "Maximum binomial Monte Carlo standard errors for the four appetite probabilities:",
        ]
    )
    for result in results:
        probabilities = (
            result.p_financial_ge_aud5m,
            result.p_outage_ge_24h,
            result.p_records_ge_10000,
            result.p_care_delay_ge_50,
        )
        max_mcse = max(probability_mcse(value, samples) for value in probabilities)
        lines.append(f"- {result.label}: {max_mcse:.6f} ({max_mcse:.4%})")
    return "\n".join(lines)


def render_json(results: list[Result], samples: int, seed: int) -> str:
    payload = {
        "manifest": {
            "samples": samples,
            "seed": seed,
            "rng": "NumPy PCG64",
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python": platform.python_version(),
            "quantile_method": "inverted_cdf",
            "expected_shortfall": (
                "arithmetic mean of exactly ceil(0.05*n) largest "
                "financial-loss draws"
            ),
            "common_random_numbers": True,
        },
        "risk_appetite": RISK_APPETITE,
        "results": [asdict(result) for result in results],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=positive_int, default=DEFAULT_SAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    uniforms, normals = build_common_random_draws(args.samples, args.seed)
    results = [simulate_scenario(scenario, uniforms, normals) for scenario in SCENARIOS]

    if args.format == "json":
        print(render_json(results, args.samples, args.seed))
    else:
        print(render_markdown(results, args.samples, args.seed))


if __name__ == "__main__":
    main()
