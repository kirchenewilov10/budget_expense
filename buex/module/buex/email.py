from buex.module.buex.constant import *
from buex.module.glb import email as glb_eml
# ***********************************************************************************
# File Name: email.py
# Author: Dimitar
# Created: 2020-04-20
# Description: Email Module For MTBDashboard
# -----------------------------------------------------------------------------------

email_footer_en = """
    <table align="center" width="690" border="0" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
        <tbody>
          <tr>
            <td height="24"><hr></td>
          </tr>
          <tr>
            <td align="center">Contact Us: info@movethebrain.nl</td>
          </tr>
          <tr>
            <td width="100%" height="8"></td>
          </tr>
          <tr>
            <td height="24"></td>
          </tr>
        </tbody>
    </table>
    """

email_footer_nl = """
    <table align="center" width="690" border="0" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
        <tbody>
          <tr>
            <td height="24"><hr></td>
          </tr>
          <tr>
            <td align="center">Neem Contact Op Met Ons: info@movethebrain.nl</td>
          </tr>
          <tr>
            <td width="100%" height="8"></td>
          </tr>
          <tr>
            <td height="24"></td>
          </tr>
        </tbody>
    </table>
    """

# ***********************************************************************************
# @Function: Get Email Template Html
# @Returns: Html
# -----------------------------------------------------------------------------------
def get_email_template_html(content, language):
    footer = email_footer_en
    if language == 'nl':
        footer = email_footer_nl

    html = """\
    <html>
        <head>
            <style>
                a:link {
                    text-decoration: none;
                }
                a:visited {
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: none;
                }
                a:active {
                    text-decoration: none;
                }
                .btn-001 {
                    color: #fe1d6d !important;
                    font-size: 23px;
                }
            </style>
        </head>
        <body>
            <div style="font-family: Helvetica, Arial, sans-serif, serif, EmojiFont; background-color: white;">
                <table align="center" height="100%" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                    <tbody>
                        <tr>
                            <td>
                                <table width="690" align="center" border="0" cellspacing="0" cellpadding="0">
                                    <tbody>
                                        <tr>
                                            <td width="100%" align="center"></td>
                                        </tr>
                                        <tr>
                                            <td width="100%" align="center" style="text-align:center;"><img data-imagetype="External"
                                                    src=\"""" + SITE_BASE_URL + """/static/mtb/asset/logo/logo.png"
                                                    alt="Move The Brain" width="300" border="0"></a></td>
                                        </tr>
                                        <tr>
                                            <td width="100%" align="center"><table width="690" cellspacing="0" cellpadding="0" border="0" bgcolor="#fff" align="center">
                                                <tbody>
                                                    <tr>
                                                        <td width="100%" align="center">
                                                            <table width="690" cellspacing="0" cellpadding="0" border="0" align="center">
                                                                <tbody>""" + content + """\
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                              </table></td>
                                          </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td>""" + footer + """</td>
                        </tr>              
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    return html


# ***********************************************************************************
# @Function: User Registration Notify Email (English)
# -----------------------------------------------------------------------------------
def send_register_notify_email_en(dest_email, user_name, password):
    subject = 'You are registerd to Move the Brain'
    content = """\
        <tr>
            <td width="30"></td>
            <td colspan="3" style="text-align:left;padding-top:15px">
                <span style="font-size:20px">Dear """ + user_name + """, </span> 
                <br><br>
                <span style="font-size:20px">We would like to let you know that an online account has been created by Move the Brain where you can complete questionnaires and tests.</span> 
                <br><br>
                <span style="font-size:20px">Email: """ + dest_email + """</span>
                <br>
                <span style="font-size:20px">Password: """ + password + """</span>
                <br><br>
                <span style="font-size:20px">Use the details above to log in to Move the Brain by clicking <a href=\"""" + SITE_BASE_URL + """"\">here.</a> After logging in, you can change the password we have created into a personal password.</span>
                <br><br>
                <span style="font-size:20px">If there are questionnaires / tests ready for you, you will receive an email from us and these can be completed via the account.</span>
                <br><br>
                <span style="font-size:20px">Sincerely,</span>
                <br>
                <span style="font-size:20px">Move the Brain</span>
                <br><br>
                <span style="font-size:18px">This is an automatically generated message for questions please contact us at info@movethebrain.nl</span>
                <br><br>
            </td>
        </tr>
        """
    html = get_email_template_html(content, 'en')
    glb_eml.sendEmail(src_email=EMAIL,
                        src_pwd=EMAIL_PWD,
                        dest_email=dest_email,
                        subject=subject,
                        content=html,
                        smtp_server_domain=SMTP_SERVER,
                        smtp_server_port=SMTP_PORT)


# ***********************************************************************************
# @Function: User Registration Notify Email (Dutch)
# -----------------------------------------------------------------------------------
def send_register_notify_email_nl(dest_email, user_name, password):
    subject = 'Je bent geregistreerd bij Move the Brain'
    content = """\
        <tr>
            <td width="30"></td>
            <td colspan="3" style="text-align:left;padding-top:15px">
                <span style="font-size:20px">Beste """ + user_name + """, </span>
                <br><br>
                <span style="font-size:20px">We willen je laten weten dat er een online account is aangemaakt door Move the Brain waar je vragenlijsten en testen in kunt vullen.</span> 
                <br><br>
                <span style="font-size:20px">E-mail: """ + dest_email + """</span>
                <br>
                <span style="font-size:20px">Wachtwoord: """ + password + """</span>
                <br><br>
                <span style="font-size:20px">Gebruik de bovenstaande gegevens om in te loggen bij Move the Brain door hier te <a href=\"""" + SITE_BASE_URL + """"\">klikken.</a>. Na het inloggen kan je het door ons gemaakte wachtwoord wijzigen in een persoonlijk wachtwoord.</span>
                <br><br>
                <span style="font-size:20px">Als er vragenlijsten/testen voor je klaar staan dan ontvang je van ons hier een mail over en kunnen deze ingevuld worden via het account.</span>
                <br><br>
                <span style="font-size:20px">Vriendelijke groet,</span>
                <br>
                <span style="font-size:20px">Move the Brain</span>
                <br><br>
                <span style="font-size:18px">Dit is een automatisch gegenereerd bericht voor vragen kun je contact opnemen via info@movethebrain.nl</span>
                <br><br>
            </td>
        </tr>
        """
    html = get_email_template_html(content, 'nl')
    glb_eml.sendEmail(src_email=EMAIL,
                        src_pwd=EMAIL_PWD,
                        dest_email=dest_email,
                        subject=subject,
                        content=html,
                        smtp_server_domain=SMTP_SERVER,
                        smtp_server_port=SMTP_PORT)


# ***********************************************************************************
# @Function: Send Test Notification Email (English)
# -----------------------------------------------------------------------------------
def send_test_notify_email_en(dest_email, user_name, test_uid, test_title):
    subject = 'There is a test/questionnaire for you'
    test_url = SITE_BASE_URL + 'user/test/start/' + test_uid
    content = """\
    <tr>
        <td width="30"></td>
        <td colspan="3" style="text-align:left;padding-top:15px">
            <span style="font-size:20px">Dear """ + user_name + """, </span>
            <br><br>
            <span style="font-size:20px">Move the Brain has prepared a test/questionnaire for you. Via your personal account you can log in and 
            start the test, by clicking on the link below you will automatically go to the test: <a href=\"""" + test_url + """\" target="_blank">""" + test_url + """</a></span>
            <br><br>
            <span style="font-size:20px">Not all mail programs support the automatic link, in which case you can copy and paste the URL into the address bar of your internet browser.</span>
            <br><br>
            <span style="font-size:20px">Sincerely,</span>
            <br>
            <span style="font-size:20px">Move the Brain</span>
            <br><br>
            <span style="font-size:18px"This is an automatically generated message for questions please contact us at info@movethebrain.nl</span>
            <br><br>
        </td>
    </tr>
    """
    html = get_email_template_html(content, 'en')
    glb_eml.sendEmail(src_email = EMAIL,
                        src_pwd = EMAIL_PWD,
                        dest_email = dest_email,
                        subject = subject,
                        content = html,
                        smtp_server_domain = SMTP_SERVER,
                        smtp_server_port = SMTP_PORT)


# ***********************************************************************************
# @Function: Send Test Notification Email (Dutch)
# -----------------------------------------------------------------------------------
def send_test_notify_email_nl(dest_email, user_name, test_uid, test_title):
    subject = 'Er is een test/vragenlijst voor jou'
    test_url = SITE_BASE_URL + 'user/test/start/' + test_uid
    content = """\
    <tr>
        <td width="30"></td>
        <td colspan="3" style="text-align:left;padding-top:15px">
            <span style="font-size:20px">Beste """ + user_name + """, </span>
            <br><br>
            <span style="font-size:20px">Move the Brain heeft een test/vragenlijst voor u klaargezet. Via uw persoonlijk account kunt u inloggen en de test starten, 
            door te klikken op onderstaande link gaat u automatisch naar de test: <a href=\"""" + test_url + """\" target="_blank">""" + test_url + """</a></span>
            <br><br>
            <span style="font-size:20px">Niet alle mailprogramma’s ondersteunen de automatische link, u kunt in dat geval de URL kopiëren en plakken in de adresbalk van uw internetbrowser.</span>
            <br><br>
            <span style="font-size:20px">Vriendelijke groet,,</span>
            <br>
            <span style="font-size:20px">Move the Brain</span>
            <br><br>
            <span style="font-size:18px"Dit is een automatisch gegenereerd bericht voor vragen kun je contact opnemen via info@movethebrain.nl</span>
            <br><br>
        </td>
    </tr>
    """
    html = get_email_template_html(content, 'nl')
    glb_eml.sendEmail(src_email = EMAIL,
                        src_pwd = EMAIL_PWD,
                        dest_email = dest_email,
                        subject = subject,
                        content = html,
                        smtp_server_domain = SMTP_SERVER,
                        smtp_server_port = SMTP_PORT)


# ***********************************************************************************
# @Function: Send Password Reset Url Email (English)
# -----------------------------------------------------------------------------------
def send_password_reset_url_email_en(dest_email, user_name, password_reset_url):
    subject = 'Password Reset Link'
    content = """\
    <tr>
        <td width="30"></td>
        <td colspan="3" style="text-align:left;padding-top:15px">
            <span style="font-size:20px">Dear """ + user_name + """,</span>
            <br><br>
            <span style="font-size:20px">Please click below url to reset your password.</span> <br>
            <span style="font-size:20px"><a href=\"""" + password_reset_url + """\" target="_blank">""" + password_reset_url + """</a></span>
            <br><br>
            <span style="font-size:20px">Sincerely,</span>
            <br>
            <span style="font-size:20px">Move the Brain</span>
            <br><br>
            <span style="font-size:18px"This is an automatically generated message for questions please contact us at info@movethebrain.nl</span>
            <br><br>
        </td>
    </tr>
    """
    html = get_email_template_html(content, 'en')
    glb_eml.sendEmail(src_email = EMAIL,
                        src_pwd = EMAIL_PWD,
                        dest_email = dest_email,
                        subject = subject,
                        content = html,
                        smtp_server_domain = SMTP_SERVER,
                        smtp_server_port = SMTP_PORT)


# ***********************************************************************************
# @Function: Send Password Reset Url Email (Dutch)
# -----------------------------------------------------------------------------------
def send_password_reset_url_email_nl(dest_email, user_name, password_reset_url):
    subject = 'Link voor opnieuw instellen van wachtwoord'
    content = """\
    <tr>
        <td width="30"></td>
        <td colspan="3" style="text-align:left;padding-top:15px">
            <span style="font-size:20px">Beste """ + user_name + """,</span><br><br>
            <span style="font-size:20px">Klik op onderstaande url om uw wachtwoord opnieuw in te stellen.</span> <br>
            <span style="font-size:20px"><a href=\"""" + password_reset_url + """\" target="_blank">""" + password_reset_url + """</a></span>
            <br><br>
            <span style="font-size:20px">Vriendelijke groet,,</span>
            <br>
            <span style="font-size:20px">Move the Brain</span>
            <br><br>
            <span style="font-size:18px"Dit is een automatisch gegenereerd bericht voor vragen kun je contact opnemen via info@movethebrain.nl</span>
            <br><br>
        </td>
    </tr>
    """
    html = get_email_template_html(content, 'nl')
    glb_eml.sendEmail(src_email = EMAIL,
                        src_pwd = EMAIL_PWD,
                        dest_email = dest_email,
                        subject = subject,
                        content = html,
                        smtp_server_domain = SMTP_SERVER,
                        smtp_server_port = SMTP_PORT)