"""
Operation History and Undo Management
-------------------------------------
Tracks all successful Stack and Queue operations with timestamps, parameters,
and results, while maintaining a bounded history and snapshot stack for safe undo.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, Tuple


@dataclass
class OperationRecord:
    """
    Represents a single recorded successful operation.
    """
    step_id: int
    structure: str        # "STACK" or "QUEUE"
    operation: str        # "PUSH", "POP", "PEEK", "ENQUEUE", "DEQUEUE", "FRONT", "REAR", "CLEAR"
    value: Any            # Element value or None
    result_message: str   # Human-readable result
    timestamp: str        # e.g., "19:35:12"


@dataclass
class UndoSnapshot:
    """
    Captures complete data state before a mutating operation for safe reversal.
    """
    stack_items: List[Any]
    queue_items: List[Any]
    action_description: str


class HistoryTracker:
    """
    Manages bounded operation history and undo state snapshots.
    """

    def __init__(self, max_history: int = 50, max_undo: int = 20):
        self.max_history: int = max_history
        self.max_undo: int = max_undo
        self._records: List[OperationRecord] = []
        self._undo_stack: List[UndoSnapshot] = []
        self._step_counter: int = 0
        self.total_successful_ops: int = 0

    def record_operation(
        self,
        structure: str,
        operation: str,
        value: Any,
        message: str
    ) -> OperationRecord:
        """
        Record a verified successful operation.
        
        Args:
            structure: "STACK" or "QUEUE"
            operation: Name of operation (e.g. "PUSH", "POP", "ENQUEUE")
            value: Associated value (or "-" if none)
            message: Descriptive outcome
            
        Returns:
            The created OperationRecord
        """
        self._step_counter += 1
        self.total_successful_ops += 1
        time_str = datetime.now().strftime("%H:%M:%S")

        record = OperationRecord(
            step_id=self._step_counter,
            structure=structure.upper(),
            operation=operation.upper(),
            value=value,
            result_message=message,
            timestamp=time_str
        )

        self._records.append(record)
        # Bounded history to prevent memory leaks
        if len(self._records) > self.max_history:
            self._records.pop(0)

        return record

    def push_undo_snapshot(
        self,
        stack_items: List[Any],
        queue_items: List[Any],
        action_description: str
    ) -> None:
        """
        Save a state snapshot prior to executing a mutating operation.
        """
        snapshot = UndoSnapshot(
            stack_items=list(stack_items),
            queue_items=list(queue_items),
            action_description=action_description
        )
        self._undo_stack.append(snapshot)
        if len(self._undo_stack) > self.max_undo:
            self._undo_stack.pop(0)

    def can_undo(self) -> bool:
        """Check if an undo snapshot is available."""
        return len(self._undo_stack) > 0

    def pop_undo_snapshot(self) -> Optional[UndoSnapshot]:
        """Pop and return the latest undo snapshot."""
        if not self._undo_stack:
            return None
        return self._undo_stack.pop()

    def get_recent(self, count: int = 10) -> List[OperationRecord]:
        """Get the most recent N operations (most recent first)."""
        return list(reversed(self._records[-count:]))

    def get_latest(self) -> Optional[OperationRecord]:
        """Return the most recent operation record, if any."""
        return self._records[-1] if self._records else None

    def clear(self) -> None:
        """Clear all records and undo history."""
        self._records.clear()
        self._undo_stack.clear()
        self._step_counter = 0
        self.total_successful_ops = 0
