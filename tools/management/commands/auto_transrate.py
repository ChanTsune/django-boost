import os
from time import sleep
from json.decoder import JSONDecodeError

from django.core.management import call_command
from django_boost.core.management import AppCommand


class Command(AppCommand):
    BASE_URL = "https://script.google.com/macros/s/AKfycby8YkD_bF_GMmJ4tHjjeH6ah8XRdAAr1ihR5ZTFGsM6dnJNOu0/exec"

    # key is from, value is to
    LANG_CODE_CVT_TABLE = {'zh_Hans': 'zh_CN',
                           'zh_Hant': 'zh_TW',
                           'sr_Latn': 'sr@latin'}

    def convert_lng_code(self, code):
        return self.LANG_CODE_CVT_TABLE.get(code, code)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--make', '-m', action='store_true',
                            help='Execute makemessages command')
        parser.add_argument('--source', default='en')
        parser.add_argument('--exclude-locale', default=[], action='append')
        parser.add_argument('--exclude-id', default=[], action='append')
        parser.add_argument('--interval', default=1, type=int)

    def handle_app_config(self, app_config, **options):
        try:
            import polib
            import requests
        except ImportError:
            self.stderr.write(
                'auto_transrate command required `polib` and `requests`.\nPlease `pip install polib requests`.')
            return
        app_path = app_config.path
        existing_locales = os.listdir(os.path.join(app_path, 'locale'))

        interval = options['interval']
        failed = {}
        exclude_locals = options['exclude_locale'] + [options['source']]
        exclude_id = options['exclude_id'] + [""]
        locales = [l for l in existing_locales if not l in exclude_locals]

        if options['make']:
            call_command('makemessages', locale=existing_locales)

        for lng in existing_locales:
            lng = self.convert_lng_code(lng)
            po_file_path = os.path.join(app_path, 'locale',
                                        lng, 'LC_MESSAGES', 'django.po')
            po = polib.pofile(po_file_path)
            for i, entry in enumerate(po):
                if entry.msgid in exclude_id:
                    continue
                request_url = self.BASE_URL + '?text={}&source={}&target={}'.format(
                    entry.msgid, options['source'], lng)
                response = requests.get(request_url)
                try:
                    if response.status_code == 200:
                        result = response.json()
                        self.stdout.write(entry.msgid)
                        self.stdout.write(' -> ')
                        self.stdout.write(result['text'])
                        self.stdout.write('\n')
                        entry.msgstr = result['text']
                        po[i] = entry
                    else:
                        failed[lng] = response.status_code
                except JSONDecodeError:
                    failed[lng] = response.status_code
                sleep(interval)
            po.save(po_file_path)
        self.stdout.write('failed :')
        self.stdout.write(str(failed))
