# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Review domain: a CONFIG knob, never chat input (like ``REVIEW_MODEL``).

The pipeline is field-agnostic — scope, search, and ranking all derive from the
user's own CV/keywords, and the only search filter is a publication date. What
ties the *framing* to a field is text: the prompts, the per-paper "domain
question" label, the page title, and the localStorage namespace. This module
collects that text into one overridable profile.

Defaults reproduce the shipped **computational-biology** demo exactly (no env =
compbio). Point the app at any field by setting ``REVIEW_DOMAIN_NAME`` (and,
optionally, the finer knobs below) in ``.env`` or the environment:

    REVIEW_DOMAIN_NAME="Materials Science"
    REVIEW_DOMAIN_QUESTION_LABEL="Materials question"     # per-paper card label
    # optional, else derived from NAME:
    REVIEW_DOMAIN_ADJ="materials-science"                  # inline adjective in prompts
    REVIEW_DOMAIN_SLUG="matsci"                            # storage-key / UA namespace
    REVIEW_DOMAIN_QUESTION_DESC="The materials question the paper answers."

Resolved lazily from ``os.environ`` at point of use so a late ``load_dotenv()``
still applies, mirroring ``app.models.model_id()``.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Domain:
    """Field-specific framing for one review app."""

    name: str  # display / prompt proper noun, e.g. "Computational Biology"
    adjective: str  # inline adjective in prompts, e.g. "computational-biology"
    slug: str  # storage-key / UA namespace, e.g. "compbio"
    question_label: str  # per-paper card + export label, e.g. "Biological question"
    question_desc: str  # schema/prompt description of that field

    @property
    def question_hint(self) -> str:
        """Lower-case inline hint for prompts, e.g. 'the biological question it answers'."""
        lbl = self.question_label[:1].lower() + self.question_label[1:]
        return f"the {lbl} it answers"


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower()) or "review"


def get_domain() -> Domain:
    """Build the active :class:`Domain` from the environment (compbio by default)."""
    name = os.getenv("REVIEW_DOMAIN_NAME")
    if name:
        # Custom field: derive the finer knobs from NAME unless overridden.
        return Domain(
            name=name,
            adjective=os.getenv("REVIEW_DOMAIN_ADJ") or name.lower(),
            slug=os.getenv("REVIEW_DOMAIN_SLUG") or _slugify(name),
            question_label=os.getenv("REVIEW_DOMAIN_QUESTION_LABEL", "Core question"),
            question_desc=os.getenv(
                "REVIEW_DOMAIN_QUESTION_DESC",
                "The core question in the field the paper addresses.",
            ),
        )
    # Default demo: computational biology (unchanged behaviour, no env needed).
    return Domain(
        name="Computational Biology",
        adjective=os.getenv("REVIEW_DOMAIN_ADJ", "computational-biology"),
        slug=os.getenv("REVIEW_DOMAIN_SLUG", "compbio"),
        question_label=os.getenv("REVIEW_DOMAIN_QUESTION_LABEL", "Biological question"),
        question_desc=os.getenv(
            "REVIEW_DOMAIN_QUESTION_DESC", "The biological question the paper answers."
        ),
    )
