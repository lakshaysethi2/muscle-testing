"""Guided muscle testing wizard — multi-step interactive flow.

Step 1: Preparation (thymic thump, quiet environment, neutrality, mudra)
Step 2: Method selection with instructions
Step 3: Enter subject + record result + optional calibration level
Step 4: Result summary + save to database

Supports back/forward navigation. State stored in session.
"""

from django import forms
from django.shortcuts import redirect, render

from apps.accounts.models import User
from apps.calibrations.models import Calibration

STEPS = ["prepare", "method", "test", "result"]

# Step index lookup for back/forward navigation
_STEP_ORDER = {name: i for i, name in enumerate(STEPS)}


class TestForm(forms.Form):
    """Validates the test-step input before saving."""

    subject = forms.CharField(min_length=1, max_length=300)
    result = forms.ChoiceField(choices=Calibration.Result.choices)
    calibration_level = forms.IntegerField(required=False, min_value=1, max_value=1000)
    notes = forms.CharField(required=False, max_length=2000)
    visibility = forms.ChoiceField(choices=Calibration.Visibility.choices)


def _get_wizard_state(request):
    """Return session dict for wizard state, initialising if needed."""
    if "wizard" not in request.session:
        request.session["wizard"] = {}
    return request.session["wizard"]


def _clear_wizard_state(request):
    """Remove wizard state from session after completion."""
    request.session.pop("wizard", None)
    request.session.modified = True


def _mark_session_dirty(request):
    """Ensure Django persists the session mutation."""
    request.session.modified = True


def guided_test(request):
    """Multi-step muscle testing wizard.

    GET:  renders the current step template.
    POST: advances / goes back, saving data in session.
          A 'back' parameter moves to the previous step.
    """
    state = _get_wizard_state(request)
    current = state.get("step", "prepare")

    if request.method == "POST":
        return _handle_post(request, state, current)

    # GET — clear one-shot error and render
    state.pop("error", None)
    _mark_session_dirty(request)
    return _render_step(request, current, state)


def _handle_post(request, state, current):
    """Process a wizard step submission."""
    _mark_session_dirty(request)

    # ── Back navigation ──
    if request.POST.get("action") == "back":
        idx = _STEP_ORDER.get(current, 0)
        state["step"] = STEPS[max(0, idx - 1)]
        return redirect("start_testing")

    # ── Step handlers ──
    if current == "prepare":
        state["step"] = "method"

    elif current == "method":
        method = request.POST.get("method")
        if method in dict(User.TestingMethod.choices):
            state["method"] = method
            state["step"] = "test"
        # else: stay on method page (invalid selection)

    elif current == "test":
        form = TestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            calibration = Calibration.objects.create(
                user=request.user if request.user.is_authenticated else None,
                subject=data["subject"],
                result=data["result"],
                calibration_level=data["calibration_level"],
                method=state.get("method", User.TestingMethod.O_RING),
                notes=data.get("notes", ""),
                visibility=data["visibility"],
            )
            state["saved_pk"] = calibration.pk
            state.pop("error", None)
            state["step"] = "result"
        else:
            state["error"] = _format_form_errors(form)
            state["step"] = "test"
            return redirect("start_testing")

    elif current == "result":
        _clear_wizard_state(request)
        return redirect("start_testing")

    return redirect("start_testing")


def _format_form_errors(form):
    """Return the first human-readable error from a form."""
    for field, errors in form.errors.items():
        for err in errors:
            return f"{field}: {err}" if field != "__all__" else err
    return "Please fix the errors below."


def _render_step(request, step, state):
    """Render the current wizard step template."""
    template = f"test/{step}.html"
    ctx = _build_context(step, state)
    return render(request, template, ctx)


def _build_context(step, state):
    """Build template context for the current step."""
    ctx = {
        "step": step,
        "steps": STEPS,
        "can_go_back": _STEP_ORDER.get(step, 0) > 0,
    }

    if step == "method":
        ctx["methods"] = User.TestingMethod.choices
        ctx["selected_method"] = state.get("method", User.TestingMethod.O_RING)

    if step == "test":
        ctx["method"] = state.get("method", User.TestingMethod.O_RING)
        ctx["error"] = state.get("error", "")

    if step == "result":
        pk = state.get("saved_pk")
        if pk:
            try:
                ctx["calibration"] = Calibration.objects.get(pk=pk)
            except Calibration.DoesNotExist:
                pass

    return ctx
