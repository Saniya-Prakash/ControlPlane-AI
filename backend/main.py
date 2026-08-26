import uuid

# from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from engines.risk_engine import analyze_prompt

from engines.routing_engine import (
    estimate_complexity,
    select_model
)

from engines.reliability_engine import evaluate_response

from engines.rewrite_engine import rewrite_response

from providers.mock_provider import generate_response

from observability.logger import log_event
from observability.metrics import get_metrics


app = FastAPI(
    title="ControlPlane.ai",
    description="Adaptive AI Reliability Layer",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {
        "service": "ControlPlane.ai",
        "status": "healthy",
        "version": "1.0.0",

        "capabilities": [
            "prompt_injection_detection",
            "pii_detection",
            "safety_detection",
            "risk_scoring",
            "model_routing",
            "response_reliability",
            "grounding_verification",
            "response_rewriting",
            "audit_logging"
        ]
    }


# ============================================================
# MAIN ANALYSIS PIPELINE
# ============================================================

@app.post("/analyze")
def analyze(request: PromptRequest):

    # --------------------------------------------------------
    # 1. Generate unique request ID
    # --------------------------------------------------------

    request_id = str(uuid.uuid4())

    # --------------------------------------------------------
    # 2. PRE-FLIGHT RISK ANALYSIS
    # --------------------------------------------------------

    risk_result = analyze_prompt(
        request.prompt
    )

    # --------------------------------------------------------
    # 3. COMPLEXITY ANALYSIS
    # --------------------------------------------------------

    complexity = estimate_complexity(
        request.prompt
    )

    # --------------------------------------------------------
    # 4. MODEL ROUTING
    # --------------------------------------------------------

    model_result = select_model(
        risk_result["risk_score"],
        complexity
    )

    # --------------------------------------------------------
    # 5. EXTRACT RISK CATEGORIES
    # --------------------------------------------------------

    risk_categories = []

    risks = risk_result["risks"]

    if risks["prompt_injection"]["detected"]:

        risk_categories.append(
            "prompt_injection"
        )

    if risks["privacy"]["detected"]:

        risk_categories.append(
            "privacy"
        )

    if risks["safety"]["detected"]:

        risk_categories.append(
            "safety"
        )

    # --------------------------------------------------------
    # 6. BLOCK HIGH-RISK REQUESTS
    # --------------------------------------------------------

    if risk_result["decision"] == "BLOCK":

        log_event({

            "request_id": request_id,

            "risk_score":
                risk_result["risk_score"],

            "risk_level":
                risk_result["risk_level"],

            "risk_categories":
                risk_categories,

            "model": None,

            "complexity":
                complexity,

            "reliability_risk_score": 0,

            "reliability_risk_level": "N/A",

            "final_decision": "BLOCK"
        })

        return {

            "request_id": request_id,

            "prompt": request.prompt,

            "preflight": {

                "risk_score":
                    risk_result["risk_score"],

                "risk_level":
                    risk_result["risk_level"],

                "decision":
                    risk_result["decision"],

                "risks":
                    risk_result["risks"]
            },

            "routing": {

                "complexity":
                    complexity,

                "model": None
            },

            "generation": {

                "original_response": None
            },

            "reliability": None,

            "final": {

                "decision": "BLOCK",

                "response": None
            },

            "message": (
                "Request blocked by ControlPlane "
                "pre-flight security policy."
            )
        }

    # --------------------------------------------------------
    # 7. GENERATE AI RESPONSE
    # --------------------------------------------------------

    response = generate_response(
        request.prompt,
        model_result["model"]
    )

    # --------------------------------------------------------
    # 8. POST-GENERATION RELIABILITY ANALYSIS
    # --------------------------------------------------------

    reliability_result = evaluate_response(
        response
    )

    reliability_score = (
        reliability_result[
            "reliability_risk_score"
        ]
    )

    # --------------------------------------------------------
    # 9. FINAL DECISION
    # --------------------------------------------------------

    final_decision = "ALLOW"

    final_response = response

    if reliability_score >= 80:

        final_decision = "BLOCK"

        final_response = None

    elif reliability_score >= 30:

        final_decision = "REWRITE"

        final_response = rewrite_response(
            response,
            reliability_result
        )

    # --------------------------------------------------------
    # 10. WRITE AUDIT EVENT
    # --------------------------------------------------------

    log_event({

        "request_id": request_id,

        "risk_score":
            risk_result["risk_score"],

        "risk_level":
            risk_result["risk_level"],

        "risk_categories":
            risk_categories,

        "model":
            model_result["model"],

        "complexity":
            complexity,

        "reliability_risk_score":
            reliability_score,

        "reliability_risk_level":
            reliability_result[
                "reliability_risk_level"
            ],

        "final_decision":
            final_decision
    })

    # --------------------------------------------------------
    # 11. RETURN COMPLETE RESULT
    # --------------------------------------------------------

    return {

        "request_id": request_id,

        "prompt": request.prompt,

        "preflight": {

            "risk_score":
                risk_result["risk_score"],

            "risk_level":
                risk_result["risk_level"],

            "decision":
                risk_result["decision"],

            "risks":
                risk_result["risks"]
        },

        "routing": {

            "complexity":
                complexity,

            "model":
                model_result
        },

        "generation": {

            "original_response":
                response
        },

        "reliability":
            reliability_result,

        "final": {

            "decision":
                final_decision,

            "response":
                final_response
        }
    }


# ============================================================
# METRICS ENDPOINT
# ============================================================

@app.get("/metrics")
def metrics():

    return get_metrics()