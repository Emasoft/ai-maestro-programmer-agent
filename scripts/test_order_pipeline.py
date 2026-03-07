#!/usr/bin/env python3
"""
test_order_pipeline.py

Manual integration test for an order processing pipeline implementation.

This script verifies that an order processing pipeline works correctly
end-to-end, including:
- Order creation and validation
- Async pipeline stage execution with retry logic
- Batch processing (orders processed in batches of configurable size)
- Error handling and pipeline recovery
- Completion status reporting

Referenced in the AMPA orchestrator-communication skill as the manual
test companion for the "Order Processing Pipeline" example
(see: skills/ampa-orchestrator-communication/references/op-notify-completion.md).

Usage:
    python3 scripts/test_order_pipeline.py
    python3 scripts/test_order_pipeline.py --batch-size 50
    python3 scripts/test_order_pipeline.py --verbose
    python3 scripts/test_order_pipeline.py --json
    python3 scripts/test_order_pipeline.py --report-file /tmp/report.md

Exit codes:
    0 - All pipeline tests passed
    1 - One or more pipeline tests failed
    2 - Pipeline configuration or setup error
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ==============================================================================
# Order and Pipeline Data Model
# ==============================================================================


class OrderStatus(Enum):
    """Status of an individual order within the pipeline."""

    PENDING = "pending"
    VALIDATING = "validating"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class PipelineStage(Enum):
    """Stages in the order processing pipeline."""

    INTAKE = "intake"
    VALIDATION = "validation"
    ENRICHMENT = "enrichment"
    PROCESSING = "processing"
    FULFILLMENT = "fulfillment"
    NOTIFICATION = "notification"


@dataclass
class Order:
    """Represents a single order in the pipeline."""

    order_id: str
    customer_id: str
    items: list[dict[str, Any]]
    total: float
    status: OrderStatus = OrderStatus.PENDING
    current_stage: PipelineStage = PipelineStage.INTAKE
    retry_count: int = 0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize order to dictionary for reporting."""
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "total": self.total,
            "status": self.status.value,
            "current_stage": self.current_stage.value,
            "retry_count": self.retry_count,
            "error": self.error,
        }


@dataclass
class PipelineResult:
    """Result of processing a batch of orders through the pipeline."""

    total_orders: int = 0
    completed: int = 0
    failed: int = 0
    retried: int = 0
    stages_executed: list[str] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)
    duration_ms: float = 0.0


# ==============================================================================
# Pipeline Implementation (simulated for testing purposes)
# ==============================================================================


class OrderPipeline:
    """Simulated async order processing pipeline with retry logic.

    This is a self-contained test implementation that validates the pipeline
    contract without requiring external services. The AMPA programmer agent
    would replace this with the actual implementation being tested.
    """

    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100

    def __init__(self, batch_size: int = DEFAULT_BATCH_SIZE, verbose: bool = False):
        self.batch_size = batch_size
        self.verbose = verbose
        self.stages = list(PipelineStage)
        self._processed_count = 0

    def _log(self, msg: str) -> None:
        """Print a log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  [pipeline] {msg}")

    def validate_order(self, order: Order) -> bool:
        """Validate that an order has all required fields and sane values."""
        if not order.order_id:
            order.error = "Missing order_id"
            return False
        if not order.customer_id:
            order.error = "Missing customer_id"
            return False
        if not order.items or len(order.items) == 0:
            order.error = "Order has no items"
            return False
        if order.total <= 0:
            order.error = "Order total must be positive"
            return False
        return True

    def process_stage(self, order: Order, stage: PipelineStage) -> bool:
        """Process a single order through one pipeline stage.

        Returns True if the stage succeeded, False if it failed.
        """
        order.current_stage = stage

        # Simulate stage-specific validation
        if stage == PipelineStage.VALIDATION:
            if not self.validate_order(order):
                order.status = OrderStatus.FAILED
                return False
            order.status = OrderStatus.VALIDATING

        elif stage == PipelineStage.ENRICHMENT:
            # Enrich order with metadata (simulated)
            order.metadata["enriched_at"] = time.time()
            order.metadata["pipeline_version"] = "1.0.0"

        elif stage == PipelineStage.PROCESSING:
            order.status = OrderStatus.PROCESSING
            # Simulate processing - orders with negative item quantities fail
            for item in order.items:
                if item.get("quantity", 0) < 0:
                    order.error = f"Invalid quantity for item: {item.get('name', 'unknown')}"
                    order.status = OrderStatus.FAILED
                    return False

        elif stage == PipelineStage.FULFILLMENT:
            # Mark as completed after fulfillment
            order.status = OrderStatus.COMPLETED

        elif stage == PipelineStage.NOTIFICATION:
            # Final notification stage - record completion time
            order.metadata["completed_at"] = time.time()

        self._log(f"Order {order.order_id}: stage {stage.value} complete")
        return True

    def process_with_retry(self, order: Order, stage: PipelineStage) -> bool:
        """Process a stage with retry logic up to MAX_RETRIES attempts."""
        for attempt in range(1, self.MAX_RETRIES + 1):
            success = self.process_stage(order, stage)
            if success:
                return True
            # On failure, check if retryable
            if order.status == OrderStatus.FAILED and attempt < self.MAX_RETRIES:
                order.status = OrderStatus.RETRYING
                order.retry_count += 1
                self._log(
                    f"Order {order.order_id}: retrying stage {stage.value} "
                    f"(attempt {attempt + 1}/{self.MAX_RETRIES})"
                )
                order.error = None  # Clear error for retry
            else:
                return False
        return False

    def process_batch(self, orders: list[Order]) -> PipelineResult:
        """Process a batch of orders through the entire pipeline.

        Orders are processed in batches of self.batch_size for efficiency.
        Each order goes through all pipeline stages sequentially.
        """
        result = PipelineResult(total_orders=len(orders))
        start_time = time.monotonic()

        # Process in batches
        for batch_start in range(0, len(orders), self.batch_size):
            batch = orders[batch_start : batch_start + self.batch_size]
            self._log(
                f"Processing batch {batch_start // self.batch_size + 1} "
                f"({len(batch)} orders)"
            )

            for order in batch:
                order_success = True
                for stage in self.stages:
                    if not self.process_with_retry(order, stage):
                        order_success = False
                        result.failed += 1
                        result.errors.append(
                            {
                                "order_id": order.order_id,
                                "stage": stage.value,
                                "error": order.error or "Unknown error",
                            }
                        )
                        break

                if order_success:
                    result.completed += 1

                if order.retry_count > 0:
                    result.retried += 1

                self._processed_count += 1

        result.stages_executed = [s.value for s in self.stages]
        result.duration_ms = (time.monotonic() - start_time) * 1000
        return result


# ==============================================================================
# Test Cases
# ==============================================================================


@dataclass
class TestResult:
    """Result of a single test case."""

    name: str
    description: str
    passed: bool
    duration_ms: float = 0.0
    error: str | None = None


def _make_order(
    order_id: str | None = None,
    customer_id: str = "CUST-001",
    items: list[dict[str, Any]] | None = None,
    total: float = 99.99,
) -> Order:
    """Helper to create a test order with sensible defaults."""
    if order_id is None:
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    if items is None:
        items = [{"name": "Widget A", "quantity": 2, "price": 49.995}]
    return Order(
        order_id=order_id,
        customer_id=customer_id,
        items=items,
        total=total,
    )


def test_single_valid_order(verbose: bool = False) -> TestResult:
    """A single valid order should complete all pipeline stages successfully."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order()
    result = pipeline.process_batch([order])

    passed = (
        result.total_orders == 1
        and result.completed == 1
        and result.failed == 0
        and order.status == OrderStatus.COMPLETED
        and "completed_at" in order.metadata
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 1 completed, got {result.completed} completed / {result.failed} failed. "
        f"Order status: {order.status.value}"
    )
    return TestResult(
        name="test_single_valid_order",
        description="A single valid order should complete all pipeline stages successfully.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_batch_processing(verbose: bool = False) -> TestResult:
    """Multiple orders should be processed in batches of the configured size."""
    start = time.monotonic()
    batch_size = 10
    pipeline = OrderPipeline(batch_size=batch_size, verbose=verbose)
    orders = [_make_order() for _ in range(25)]
    result = pipeline.process_batch(orders)

    passed = (
        result.total_orders == 25
        and result.completed == 25
        and result.failed == 0
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 25 completed, got {result.completed} completed / {result.failed} failed."
    )
    return TestResult(
        name="test_batch_processing",
        description="Multiple orders should be processed in batches of the configured size.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_order_validation_rejects_empty_items(verbose: bool = False) -> TestResult:
    """An order with no items should fail at the validation stage."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order(items=[])
    result = pipeline.process_batch([order])

    passed = (
        result.failed == 1
        and result.completed == 0
        and order.status == OrderStatus.FAILED
        and order.error is not None
        and "no items" in order.error.lower()
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 1 failed with 'no items' error, got: status={order.status.value}, error={order.error}"
    )
    return TestResult(
        name="test_order_validation_rejects_empty_items",
        description="An order with no items should fail at the validation stage.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_order_validation_rejects_zero_total(verbose: bool = False) -> TestResult:
    """An order with zero or negative total should fail validation."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order(total=0.0)
    result = pipeline.process_batch([order])

    passed = (
        result.failed == 1
        and order.status == OrderStatus.FAILED
        and order.error is not None
        and "total" in order.error.lower()
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 1 failed with 'total' error, got: status={order.status.value}, error={order.error}"
    )
    return TestResult(
        name="test_order_validation_rejects_zero_total",
        description="An order with zero or negative total should fail validation.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_order_validation_rejects_missing_customer(verbose: bool = False) -> TestResult:
    """An order with empty customer_id should fail validation."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order(customer_id="")
    result = pipeline.process_batch([order])

    passed = (
        result.failed == 1
        and order.status == OrderStatus.FAILED
        and order.error is not None
        and "customer_id" in order.error.lower()
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 1 failed with 'customer_id' error, got: status={order.status.value}, error={order.error}"
    )
    return TestResult(
        name="test_order_validation_rejects_missing_customer",
        description="An order with empty customer_id should fail validation.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_negative_quantity_fails_processing(verbose: bool = False) -> TestResult:
    """An order with a negative item quantity should fail at the processing stage."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order(
        items=[{"name": "Bad Widget", "quantity": -1, "price": 10.0}],
        total=10.0,
    )
    result = pipeline.process_batch([order])

    passed = (
        result.failed == 1
        and order.status == OrderStatus.FAILED
        and order.error is not None
        and "quantity" in order.error.lower()
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 1 failed with 'quantity' error, got: status={order.status.value}, error={order.error}"
    )
    return TestResult(
        name="test_negative_quantity_fails_processing",
        description="An order with a negative item quantity should fail at the processing stage.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_pipeline_stages_execute_in_order(verbose: bool = False) -> TestResult:
    """The pipeline should execute all stages in the correct order."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order()
    result = pipeline.process_batch([order])

    expected_stages = [s.value for s in PipelineStage]
    passed = result.stages_executed == expected_stages
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected stages {expected_stages}, got {result.stages_executed}"
    )
    return TestResult(
        name="test_pipeline_stages_execute_in_order",
        description="The pipeline should execute all stages in the correct order.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_enrichment_adds_metadata(verbose: bool = False) -> TestResult:
    """After enrichment stage, order metadata should contain pipeline version."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order()
    pipeline.process_batch([order])

    passed = (
        "enriched_at" in order.metadata
        and "pipeline_version" in order.metadata
        and order.metadata["pipeline_version"] == "1.0.0"
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected metadata to have enriched_at and pipeline_version, got: {order.metadata}"
    )
    return TestResult(
        name="test_enrichment_adds_metadata",
        description="After enrichment stage, order metadata should contain pipeline version.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_retry_count_tracked(verbose: bool = False) -> TestResult:
    """Failed orders that were retried should have retry_count > 0."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    # This order fails at processing due to negative quantity - retries are attempted
    order = _make_order(
        items=[{"name": "Retry Widget", "quantity": -1, "price": 5.0}],
        total=5.0,
    )
    result = pipeline.process_batch([order])

    # Order should have been retried (MAX_RETRIES - 1 retries before final failure)
    passed = (
        order.retry_count > 0
        and result.retried >= 1
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected retry_count > 0, got: retry_count={order.retry_count}, result.retried={result.retried}"
    )
    return TestResult(
        name="test_retry_count_tracked",
        description="Failed orders that were retried should have retry_count > 0.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_mixed_batch_partial_success(verbose: bool = False) -> TestResult:
    """A batch with a mix of valid and invalid orders should report partial success."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=5, verbose=verbose)
    orders = [
        _make_order(),  # valid
        _make_order(),  # valid
        _make_order(items=[]),  # invalid: no items
        _make_order(),  # valid
        _make_order(total=-10.0),  # invalid: negative total
    ]
    result = pipeline.process_batch(orders)

    passed = (
        result.total_orders == 5
        and result.completed == 3
        and result.failed == 2
        and len(result.errors) == 2
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected 3 completed / 2 failed, got: {result.completed} completed / {result.failed} failed, "
        f"errors={len(result.errors)}"
    )
    return TestResult(
        name="test_mixed_batch_partial_success",
        description="A batch with a mix of valid and invalid orders should report partial success.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_large_batch_performance(verbose: bool = False) -> TestResult:
    """Processing 500 orders in batches of 100 should complete within 5 seconds."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=100, verbose=verbose)
    orders = [_make_order() for _ in range(500)]
    result = pipeline.process_batch(orders)

    duration = (time.monotonic() - start) * 1000
    max_allowed_ms = 5000.0
    passed = (
        result.completed == 500
        and result.failed == 0
        and duration < max_allowed_ms
    )
    error = None if passed else (
        f"Expected 500 completed in <{max_allowed_ms}ms, got: "
        f"{result.completed} completed, {result.failed} failed, {duration:.1f}ms"
    )
    return TestResult(
        name="test_large_batch_performance",
        description="Processing 500 orders in batches of 100 should complete within 5 seconds.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_empty_batch(verbose: bool = False) -> TestResult:
    """An empty batch should return zero counts without errors."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=10, verbose=verbose)
    result = pipeline.process_batch([])

    passed = (
        result.total_orders == 0
        and result.completed == 0
        and result.failed == 0
        and len(result.errors) == 0
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected all zeros for empty batch, got: total={result.total_orders}, "
        f"completed={result.completed}, failed={result.failed}"
    )
    return TestResult(
        name="test_empty_batch",
        description="An empty batch should return zero counts without errors.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_pipeline_result_has_duration(verbose: bool = False) -> TestResult:
    """Pipeline result should track total processing duration in milliseconds."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    orders = [_make_order()]
    result = pipeline.process_batch(orders)

    passed = result.duration_ms > 0
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected duration_ms > 0, got: {result.duration_ms}"
    )
    return TestResult(
        name="test_pipeline_result_has_duration",
        description="Pipeline result should track total processing duration in milliseconds.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


def test_error_report_contains_stage_info(verbose: bool = False) -> TestResult:
    """Error entries in the pipeline result should include the failing stage name."""
    start = time.monotonic()
    pipeline = OrderPipeline(batch_size=1, verbose=verbose)
    order = _make_order(items=[])
    result = pipeline.process_batch([order])

    passed = (
        len(result.errors) == 1
        and "stage" in result.errors[0]
        and result.errors[0]["stage"] == PipelineStage.VALIDATION.value
        and "order_id" in result.errors[0]
        and "error" in result.errors[0]
    )
    duration = (time.monotonic() - start) * 1000
    error = None if passed else (
        f"Expected error with stage='validation', got: {result.errors}"
    )
    return TestResult(
        name="test_error_report_contains_stage_info",
        description="Error entries in the pipeline result should include the failing stage name.",
        passed=passed,
        duration_ms=duration,
        error=error,
    )


# ==============================================================================
# Test Runner and Reporting
# ==============================================================================

# Registry of all test functions
ALL_TESTS = [
    test_single_valid_order,
    test_batch_processing,
    test_order_validation_rejects_empty_items,
    test_order_validation_rejects_zero_total,
    test_order_validation_rejects_missing_customer,
    test_negative_quantity_fails_processing,
    test_pipeline_stages_execute_in_order,
    test_enrichment_adds_metadata,
    test_retry_count_tracked,
    test_mixed_batch_partial_success,
    test_large_batch_performance,
    test_empty_batch,
    test_pipeline_result_has_duration,
    test_error_report_contains_stage_info,
]


def _print_table(results: list[TestResult]) -> None:
    """Print a formatted table of test results with unicode borders."""
    # Column widths
    name_w = max(len(r.name) for r in results)
    desc_w = max(len(r.description) for r in results)
    status_w = 8  # "PASSED" / "FAILED"
    time_w = 10  # "1234.5 ms"

    # Clamp description width to terminal-friendly size
    max_desc = 60
    if desc_w > max_desc:
        desc_w = max_desc

    # Header
    h_top = (
        "\u2501" * (name_w + 2)
        + "\u2533"
        + "\u2501" * (desc_w + 2)
        + "\u2533"
        + "\u2501" * (status_w + 2)
        + "\u2533"
        + "\u2501" * (time_w + 2)
    )
    h_mid = (
        "\u2501" * (name_w + 2)
        + "\u254B"
        + "\u2501" * (desc_w + 2)
        + "\u254B"
        + "\u2501" * (status_w + 2)
        + "\u254B"
        + "\u2501" * (time_w + 2)
    )
    h_bot = (
        "\u2501" * (name_w + 2)
        + "\u253B"
        + "\u2501" * (desc_w + 2)
        + "\u253B"
        + "\u2501" * (status_w + 2)
        + "\u253B"
        + "\u2501" * (time_w + 2)
    )

    # Colors (ANSI)
    GREEN = "\033[32m"
    RED = "\033[31m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"\n\u250F{h_top}\u2513")
    print(
        f"\u2503 {BOLD}{'Test Name':<{name_w}}{RESET} "
        f"\u2503 {BOLD}{'Description':<{desc_w}}{RESET} "
        f"\u2503 {BOLD}{'Status':<{status_w}}{RESET} "
        f"\u2503 {BOLD}{'Time':<{time_w}}{RESET} \u2503"
    )
    print(f"\u2523{h_mid}\u252B")

    for r in results:
        desc = r.description[:max_desc] if len(r.description) > max_desc else r.description
        if r.passed:
            status_str = f"{GREEN}PASSED{RESET}  "
        else:
            status_str = f"{RED}FAILED{RESET}  "
        time_str = f"{r.duration_ms:>7.1f} ms"
        print(
            f"\u2503 {r.name:<{name_w}} "
            f"\u2503 {desc:<{desc_w}} "
            f"\u2503 {status_str} "
            f"\u2503 {time_str:<{time_w}} \u2503"
        )

    print(f"\u2517{h_bot}\u251B")


def _print_failures(results: list[TestResult]) -> None:
    """Print detailed failure information."""
    failures = [r for r in results if not r.passed]
    if not failures:
        return
    print("\n--- FAILURE DETAILS ---")
    for r in failures:
        print(f"\n  {r.name}:")
        print(f"    {r.error}")


def _print_json(results: list[TestResult]) -> None:
    """Print results in JSON format."""
    data = {
        "total": len(results),
        "passed": sum(1 for r in results if r.passed),
        "failed": sum(1 for r in results if not r.passed),
        "results": [
            {
                "name": r.name,
                "description": r.description,
                "passed": r.passed,
                "duration_ms": round(r.duration_ms, 2),
                "error": r.error,
            }
            for r in results
        ],
    }
    print(json.dumps(data, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manual integration test for order processing pipeline."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size used by the pipeline (default: 100)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose pipeline execution logs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--report-file",
        type=str,
        default=None,
        help="Write full report to this file; print only a concise summary to stdout",
    )
    args = parser.parse_args()

    # Run all tests
    results: list[TestResult] = []
    for test_fn in ALL_TESTS:
        try:
            result = test_fn(verbose=args.verbose)
            results.append(result)
        except Exception as exc:
            # If a test function itself raises, capture as failure
            results.append(
                TestResult(
                    name=test_fn.__name__,
                    description=test_fn.__doc__ or "No description",
                    passed=False,
                    error=f"Unhandled exception: {exc}",
                )
            )

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    total_ms = sum(r.duration_ms for r in results)
    all_passed = all(r.passed for r in results)

    # When --report-file is given, write full output to file and print concise summary
    if args.report_file:
        import io
        buf = io.StringIO()
        if args.json:
            data = {
                "total": total, "passed": passed, "failed": failed,
                "results": [
                    {"name": r.name, "description": r.description,
                     "passed": r.passed, "duration_ms": round(r.duration_ms, 2),
                     "error": r.error}
                    for r in results
                ],
            }
            buf.write(json.dumps(data, indent=2))
        else:
            # Capture table and failures into buffer using temporary stdout redirect
            old_stdout = sys.stdout
            sys.stdout = buf
            _print_table(results)
            _print_failures(results)
            print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
            if all_passed:
                print("\nAll pipeline tests PASSED.")
            else:
                print(f"\n{failed} pipeline test(s) FAILED.")
            sys.stdout = old_stdout

        from pathlib import Path
        Path(args.report_file).write_text(buf.getvalue(), encoding="utf-8")

        # Concise terminal summary (2-3 lines max)
        tag = "[PASS]" if all_passed else "[FAIL]"
        print(f"{tag} {passed}/{total} tests passed ({total_ms:.1f}ms). Report: {args.report_file}")
    else:
        # Default behavior: full output to terminal
        if args.json:
            _print_json(results)
        else:
            _print_table(results)
            _print_failures(results)
            print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
            if all_passed:
                print("\nAll pipeline tests PASSED.")
            else:
                print(f"\n{failed} pipeline test(s) FAILED.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
