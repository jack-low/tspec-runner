from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

class Retry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max: int = 0
    backoff_ms: int = 0

class Step(BaseModel):
    model_config = ConfigDict(extra="forbid")
    do: str
    name: Optional[str] = None
    with_: Dict[str, Any] = Field(default_factory=dict, alias="with")
    save: Optional[Union[str, Dict[str, Any]]] = None
    retry: Optional[Retry] = None
    timeout_ms: Optional[int] = None
    when: Optional[str] = None
    skip: Optional[Union[bool, str]] = None

class Fixtures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    before: List[Step] = Field(default_factory=list)
    after: List[Step] = Field(default_factory=list)
    before_each: List[Step] = Field(default_factory=list)
    after_each: List[Step] = Field(default_factory=list)

class Suite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    tags: List[str] = Field(default_factory=list)
    default_timeout_ms: int = 15000
    default_retry: Optional[Retry] = None
    fail_fast: bool = False
    artifact_dir: str = "artifacts"

class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    tags: List[str] = Field(default_factory=list)
    when: Optional[str] = None
    steps: List[Step]
    expect: List[Step] = Field(default_factory=list)
    timeout_ms: Optional[int] = None
    skip: Optional[Union[bool, str]] = None

class Document(BaseModel):
    model_config = ConfigDict(extra="forbid")
    suite: Suite
    vars: Dict[str, Any] = Field(default_factory=dict)
    fixtures: Fixtures = Field(default_factory=Fixtures)
    cases: List[Case] = Field(default_factory=list)
    plugins: Dict[str, Any] = Field(default_factory=dict)
    meta: Dict[str, Any] = Field(default_factory=dict)
