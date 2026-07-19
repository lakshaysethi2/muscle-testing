"""Guided muscle testing wizard — multi-step interactive flow.

Step 1: Preparation checklist (hydration, neutrality, centering)
Step 2: Method selection with instructions
Step 3: Enter subject + record result + optional calibration level
Step 4: Result summary + save to database
"""

from django.shortcuts import redirect, render

from apps.accounts.models import User
from apps.calibrations.models import Calibration

STEPS = ["prepare", "method", "test", "result"]


def _get_wizard_state(request):
    """Return session dict for wizard state, initialising if needed."""
    if "wizard" not in request.session:
        request.session["wizard"] = {}
    return request.session["wizard"]


def _clear_wizard_state(request):
    """Remove wizard state from session after completion."""
    request.session.pop("wizard", None)
    request.session.modified = True


def guided_test(request):
    """Multi-step muscle testing wizard.

    GET:  renders the current step template.
    POST: advances to the next step, saving data in session.
    """
    state = _get_wizard_state(request)
    current = state.get("step", "prepare")

    if request.method == "POST":
        return _handle_post(request, state, current)

    return _render_step(request, current, state)


def _handle_post(request, state, current):
    """Process a wizard step submission and advance."""
    request.session.modified = True

    if current == "prepare":
        # User confirms they are ready
        state["step"] = "method"

    elif current == "method":
        method = request.POST.get("method")
        if method in dict(User.TestingMethod.choices):
            state["method"] = method
            state["step"] = "test"
        else:
            state["step"] = "method"  # stay, show error

    elif current == "test":
        subject = request.POST.get("subject", "").strip()
        result = request.POST.get("result", "")
        level_raw = request.POST.get("calibration_level", "")
        notes = request.POST.get("notes", "").strip()
        visibility_raw = request.POST.get("visibility", "private")

        if not subject or result not in ("strong", "weak"):
            state["error"] = "Please enter a subject and select Strong or Weak."
            state["step"] = "test"
            return redirect("start_testing")

        # Save calibration
        calibration = Calibration.objects.create(
            user=request.user if request.user.is_authenticated else None,
            subject=subject,
            result=result,
            calibration_level=_safe_int(level_raw),
            method=state.get("method", User.TestingMethod.O_RING),
            notes=notes,
            visibility=(
                Calibration.Visibility.PUBLIC
                if visibility_raw == "public"
                else Calibration.Visibility.PRIVATE
            ),
        )
        state["saved_pk"] = calibration.pk
        state["step"] = "result"

    elif current == "result":
        _clear_wizard_state(request)
        return redirect("start_testing")

    request.session.modified = True
    return redirect("start_testing")


def _render_step(request, step, state):
    """Render the current wizard step template."""
    template = f"test/{step}.html"
    ctx = _build_context(step, state)
    return render(request, template, ctx)


def _build_context(step, state):
    """Build template context for the current step."""
    ctx = {"step": step, "steps": STEPS}

    if step == "method":
        ctx["methods"] = User.TestingMethod.choices
        ctx["selected_method"] = state.get("method", User.TestingMethod.O_RING)

    if step == "test":
        ctx["method"] = state.get("method", User.TestingMethod.O_RING)
        error = state.get("error", "")
        if error:
            ctx["error"] = error
            state.pop("error", None)  # clear after rendering once

    if step == "result":
        pk = state.get("saved_pk")
        if pk:
            try:
                ctx["calibration"] = Calibration.objects.get(pk=pk)
            except Calibration.DoesNotExist:
                pass

    return ctx


def _safe_int(value):
    """Return an int or None, silently ignoring bad values."""
    try:
        v = int(value)
        if 1 <= v <= 1000:
            return v
    except (ValueError, TypeError):
        pass
    return None
