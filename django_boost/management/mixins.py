from io import StringIO


class ConfirmOptionMixin:

    def add_confirm_option(self, parser):
        parser.add_argument('-y', action='store_true')

    def confirm(self, message, **options):
        if not options.get('y', False):
            answer = None
            while not answer or answer not in "yn":
                answer = input(message + " [y/N] ")
                if not answer:
                    answer = "n"
                    break
                else:
                    answer = answer[0].lower()
            return answer == "y"
        return True


class QuitOptionMixin:

    def add_quit_option(self, parser):
        parser.add_argument('-q', '--quit', action='store_true',
                            help="Don't output to standard output.")

    def if_needed_make_quit(self, **options):
        if options.get('quit', False):
            self.stderr = self.stdout = StringIO()
