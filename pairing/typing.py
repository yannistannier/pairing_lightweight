from typing import Any, Callable, Dict

__all__ = ("Row", "Rule")


Row = Dict[str, Any]
Rule = Callable[[Row, Row], bool]
