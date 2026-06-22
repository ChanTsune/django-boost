from django.template import Context, Engine, engines
from django.test import override_settings

from django_boost.template import StrictInvalidTemplateVariable
from django_boost.test import TestCase


class TemplateError(Exception):
    pass


class TestStrictInvalidTemplateVariable(TestCase):

    def test_render_existing_variable(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("{{ name }}")

        self.assertEqual(template.render(Context({"name": "django-boost"})), "django-boost")

    def test_raise_value_error_for_missing_variable(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("{{ missing }}")

        with self.assertRaisesMessage(
                ValueError,
                "Template variable or property 'missing' is invalid or missing."):
            template.render(Context({}))

    def test_custom_message(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable(
            message="Missing template variable: {name}"
        ))
        template = engine.from_string("{{ user.name }}")

        with self.assertRaisesMessage(ValueError, "Missing template variable: user.name"):
            template.render(Context({}))

    def test_custom_exception_class(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable(
            exception_class=TemplateError
        ))
        template = engine.from_string("{{ missing }}")

        with self.assertRaises(TemplateError):
            template.render(Context({}))

    def test_non_exception_class_raises_at_construction(self):
        with self.assertRaises(TypeError):
            StrictInvalidTemplateVariable(exception_class=str)

    def test_message_with_unknown_placeholder_raises_at_construction(self):
        with self.assertRaises(ValueError):
            StrictInvalidTemplateVariable(message="Missing {unknown}")

    def test_message_with_stray_brace_raises_at_construction(self):
        with self.assertRaises(ValueError):
            StrictInvalidTemplateVariable(message="json {} here")

    def test_variable_placeholder_is_not_supported(self):
        with self.assertRaises(ValueError):
            StrictInvalidTemplateVariable(message="Missing {variable}")

    def test_dotted_lookup_reported_with_full_path(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("{{ user.name }}")

        with self.assertRaisesMessage(
                ValueError,
                "Template variable or property 'user.name' is invalid or missing."):
            template.render(Context({}))

    def test_filter_on_missing_variable_raises(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("{{ missing|upper }}")

        with self.assertRaises(ValueError):
            template.render(Context({}))

    def test_default_filter_does_not_suppress_missing_variable(self):
        # The variable resolves through ``string_if_invalid`` before the
        # ``default`` filter runs, so a missing value still raises.
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string('{{ missing|default:"fallback" }}')

        with self.assertRaises(ValueError):
            template.render(Context({}))

    def test_existing_falsy_values_render_without_raising(self):
        # "Invalid" means unresolvable, not falsy: empty string and 0 render.
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("[{{ empty }}][{{ zero }}]")

        self.assertEqual(template.render(Context({"empty": "", "zero": 0})), "[][0]")

    def test_if_tag_with_missing_variable_does_not_raise(self):
        # Tags that resolve with ignore_failures bypass string_if_invalid.
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("{% if missing %}yes{% else %}no{% endif %}")

        self.assertEqual(template.render(Context({})), "no")

    def test_for_tag_with_missing_iterable_does_not_raise(self):
        engine = Engine(string_if_invalid=StrictInvalidTemplateVariable())
        template = engine.from_string("{% for x in missing %}{{ x }}{% endfor %}")

        self.assertEqual(template.render(Context({})), "")

    @override_settings(TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {"string_if_invalid": StrictInvalidTemplateVariable()},
    }])
    def test_raises_through_templates_setting(self):
        template = engines["django"].from_string("{{ missing }}")

        with self.assertRaises(ValueError):
            template.render({})
