class TSpecError(Exception):
    """Base error."""

class SpecVersionError(TSpecError):
    """Spec version negotiation or support-window error."""

class ParseError(TSpecError):
    """Parsing errors."""

class ValidationError(TSpecError):
    """Schema/structure validation errors."""

class ExecutionError(TSpecError):
    """Runtime execution errors."""
