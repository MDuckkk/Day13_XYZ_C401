from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4

        # Extract docs from prompt and use them as the answer
        answer = "No relevant article found. Please contact helpdesk at ext. 9999 or helpdesk@internal."
        if "Docs=" in prompt:
            docs_part = prompt.split("Docs=", 1)[1].split("\nQuestion=")[0].strip()
            # docs_part looks like "['...article text...']"
            if docs_part and docs_part not in ("[]", "['No matching IT helpdesk article found. Please contact helpdesk at ext. 9999 or helpdesk@internal.']"):
                # Strip list brackets and quotes
                clean = docs_part.strip("[]'\"")
                answer = clean

        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
