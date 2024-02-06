/* Make sure uncrustify changes don't break existing things
 * This file must not change when run through
 *
 * uncrustify -c ci/gitlab-ci/uncrustify.cfg
 */

/* Minimal indent should stay as is */
typedef struct _FooType {
  int       something;
  MpObject  else_;

  MpObject *else2;
} FooType;

/* Don't overalign */
typedef struct _FooType2 {
  Foo child;

  SomethingElse          whatever;
  const somethinglong   *a;
  const somethinglonger *b;
} FooType2;


void
check_vars (void)
{
  g_autofree char *str = NULL;
  g_autoptr (GObject) object = NULL;
  int a;

  a = 3 + 4;
  a += -3;
  a %= *str;
}


void
check_if_else (void)
{
  /* Single line statements don't get braces */
  if (TRUE)
    g_printf ("foo");
  else
    g_printf ("bar");

  /* Multiline statements do */
  if (FALSE) {
    func (with, a, lot,
          of, arguments);
  } else if (TRUE) {
    /* only single line but first if () has multiple lines */
  } else {
    g_assert (TRUE);
  }
}


void
check_while (void)
{
  /* Single line statements don't get braces */
  while (TRUE)
    g_printf ("foo");

  /* Multiline statements do */
  while (FALSE) {
    func (with, a, lot,
          of, arguments);
  }
}


gboolean
check_goto (void)
{
  goto label;

 label:
  return TRUE;
}


void
check_switch (GObject      *object,
              guint         property_id,
              const GValue *value,
              GParamSpec   *pspec)
{
  switch (property_id) {
  case PROP_ACTIVE:
    phosh_quick_setting_set_active (self, g_value_get_boolean (value));
    break;
  default:
    G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
    break;
  }
}


static void
check_i18n ()
{
  _("Foo");
  N_("Bar");
}
