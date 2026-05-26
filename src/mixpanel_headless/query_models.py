"""Pydantic input models for Workspace query methods.

Each model mirrors the signature of a ``Workspace.build_*_params()`` method,
providing a single validated object for schema generation and type-safe input.

No ``from __future__ import annotations`` — Pydantic resolves type aliases
(``QueryTimeUnit``, ``MathType``, etc.) eagerly at class-creation time.
"""

from pydantic import BaseModel, ConfigDict, Field

from mixpanel_headless._literal_types import (
    InsightsMode,
    MathType,
    PerUserAggregation,
    QueryTimeUnit,
)
from mixpanel_headless.types import (
    CohortBreakdown,
    CohortMetric,
    Filter,
    Formula,
    FrequencyBreakdown,
    FrequencyFilter,
    GroupBy,
    Metric,
    TimeComparison,
)


class InsightsQuery(BaseModel):
    """Input model for an insights query.

    Bundles all parameters accepted by ``Workspace.build_params()`` and
    ``Workspace.query()`` into a single validated object. Useful as a
    JSON-schema source for MCP tools and other schema-driven consumers.

    Example:
        ```python
        from mixpanel_headless import InsightsQuery, Metric, Filter

        q = InsightsQuery(
            events=[Metric("Login", math="unique")],
            where=[Filter.equals("country", "US")],
            last=7,
        )
        params = ws.build_params(q)
        result = ws.query(q)
        ```
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    events: list[Metric | CohortMetric | Formula] = Field(
        ...,
        description="Events to query. Each is a Metric, CohortMetric, or Formula.",
        min_length=1,
    )
    from_date: str | None = Field(
        None,
        description="Start date (YYYY-MM-DD). Overrides 'last' when set.",
    )
    to_date: str | None = Field(
        None,
        description="End date (YYYY-MM-DD). Requires from_date.",
    )
    last: int = Field(
        30,
        description="Relative time range in days. Default: 30. Ignored if from_date is set.",
    )
    unit: QueryTimeUnit = Field(
        "day",
        description="Time granularity: hour, day, week, month, quarter.",
    )
    math: MathType = Field(
        "total",
        description="Default aggregation for plain-string events.",
    )
    math_property: str | None = Field(
        None,
        description="Property name for property-based math.",
    )
    per_user: PerUserAggregation | None = Field(
        None,
        description="Per-user pre-aggregation.",
    )
    percentile_value: int | float | None = Field(
        None,
        description="Custom percentile value (e.g. 95). Required when math='percentile'.",
    )
    group_by: list[GroupBy | CohortBreakdown | FrequencyBreakdown] | None = Field(
        None,
        description="Break down results by property values, cohort, or event frequency.",
    )
    where: list[Filter | FrequencyFilter] | None = Field(
        None,
        description="Filter results by property conditions.",
    )
    formula: str | None = Field(
        None,
        description="Formula expression referencing events by position letter (A, B, C...).",
    )
    formula_label: str | None = Field(
        None,
        description="Display label for the formula result.",
    )
    rolling: int | None = Field(
        None,
        description="Rolling window size in periods.",
    )
    cumulative: bool = Field(
        False,
        description="Enable cumulative analysis mode.",
    )
    mode: InsightsMode = Field(
        "timeseries",
        description="Result shape: timeseries (per-period), total (single aggregate), table.",
    )
    time_comparison: TimeComparison | None = Field(
        None,
        description="Period-over-period comparison.",
    )
    data_group_id: int | None = Field(
        None,
        description="Data group ID for group-level analytics.",
    )


# TODO: Add FunnelQuery wrapping Workspace.build_funnel_params()
# TODO: Add RetentionQuery wrapping Workspace.build_retention_params()
# TODO: Add FlowQuery wrapping Workspace.build_flow_params()
