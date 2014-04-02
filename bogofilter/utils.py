from email.mime.text import MIMEText
from email.header import Header
from subprocess import Popen, PIPE
from django.utils.encoding import smart_bytes, smart_text


class BogofilterException(Exception):
    pass

def make_email_header(header):
    if header is None:
        header = ''
    return Header(header.encode('utf-8', errors='replace'), 'utf-8')

def make_email_msg(from_email, subject, body, extra_headers=None):
    if body is None:
        body = ''
    msg = MIMEText(body.encode('utf-8', errors='replace'), _charset='utf-8')
    msg['From'] = make_email_header(from_email)
    msg['Subject'] = make_email_header(subject)
    if extra_headers != None:
        for name, header in extra_headers.items():
            msg[name] = make_email_header(header)
    return msg.as_string()

def run_bogofilter(msg_str, bogofilter_args=None):
    """
    raises:
        subprocess.CalledProcessError
        bogofilter.utils.BogofilterException
    """
    args = ['bogofilter', '-e']
    if bogofilter_args is not None:
        args.extend(bogofilter_args)
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    res = p.communicate(input=smart_bytes(msg_str))
    if p.returncode != 0 and res[1]:
        raise BogofilterException(smart_text(res[1]))
    return smart_text(res[0])

def mark_spam(msg_str, bogofilter_args=None):
    """
    raises:
        subprocess.CalledProcessError
        bogofilter.utils.BogofilterException
    """
    if bogofilter_args is None:
        bogofilter_args = []
    bogofilter_args.append('-s')
    run_bogofilter(msg_str, bogofilter_args)

def mark_ham(msg_str, bogofilter_args=None):
    """
    raises:
        subprocess.CalledProcessError
        bogofilter.utils.BogofilterException
    """
    if bogofilter_args is None:
        bogofilter_args = []
    bogofilter_args.append('-n')
    run_bogofilter(msg_str, bogofilter_args)

def classify_msg(msg_str, bogofilter_args=None):
    """
    raises:
        subprocess.CalledProcessError
        bogofilter.utils.BogofilterException
    """
    if bogofilter_args is None:
        bogofilter_args = []
    bogofilter_args.append('-T')
    res = run_bogofilter(msg_str, bogofilter_args)
    bogotype, score = res.strip().split()[:2]
    return [bogotype, float(score)]

