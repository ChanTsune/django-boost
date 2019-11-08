try:
    import qrcode
except ImportError:
    import sys
    sys.stderr.write("""qrcode is not installed.
please install "qrcode"
run command "python -m pip install qrcode"
""")
    sys.exit(-1)
