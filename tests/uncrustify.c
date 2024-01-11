/* Make sure uncrustify changes don't break existing things
 * This file must not change when run through
 *
 * uncrustify -c ci/gitlab-ci/uncrustify.cfg
 */


typedef struct {
  int       something;
  MpObject  else_;

  MpObject *else2;
};


void
check_vars (void)
{
  g_autofree char *str = NULL;
  g_autoptr (GObject) object = NULL;
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
