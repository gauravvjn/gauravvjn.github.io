---
title: Security in the Django Application
date: 2020-05-28
category: Django
tags: clickjacking-attack, crlf-injection, cross-site-request-forgery, cross-site-scripting, csrf, django, security, sql-injection, timing-attack, web-security, xss
authors: Gaurav Jain
summary: 
coverimage: /images/security_in_django.png
---

Security is the one the most common and critical aspect of an application yet we don't give due importance to this. In this post we'll go through most common web security vulnerabilities and practices and how can we prevent/mitigate them in a Django app elegantly.

- [SQL Injection](#sql-injection)
- [CRLF Injection](#crlf-injection)
- [Timing Attack](#timing-attack)
- [Clickjacking Attack](#clickjacking-attack)
- [Cross-Site Scripting (XSS)](#cross-site-scripting)
- [Cross-Site Request Forgery (CSRF)](#csrf)
- [HTTP Strict Transport Security (SSL)](#hsts)

#### 1\. SQL Injection

SQL injection is a type of attack where a malicious user is able to execute arbitrary SQL code on a database. This can result in records being deleted/updated or data leakage.  
Django provides a way to write raw or custom SQL queries along with the ORM. But using raw SQL queries can make your web application vulnerable to SQL injection. Consider below example -

```python
from django.db import connection
cursor = connection.cursor()

username = request.GET['username']
sql_query = "SELECT * FROM users WHERE username = '%s';" % username
cursor.execute(sql_query)
```

At first glance, it seems it's going to retrieve the user object from the table but what if an attacker pass below string in the username parameter.

```sql
''; DROP TABLE users;
```

OR

```sql
''; UPDATE users SET is_superuser = true WHERE username = 'hacker';
```

Yes, you are correct, it's going give the superuser permission to user 'hacker' and with the superuser permission an attacker can do anything with the database.

To prevent this, always use Django's inbuilt ORM for DB querying. If, for some reason, you can't do that, always make sure you validate/sanitize user-controlled data and pass it as a param instead of by doing string formatting. Above example can be re-written as -

```python
sql_query = "SELECT * FROM users WHERE username = %s;"
cursor.execute(sql_query, username)
```

Similarly, you can make `.**extra()**` and **`RawSQL()`** more secure in Django by using parameterized queries.

#### 2\. CRLF Injection

Web servers return a response containing both the HTTP response headers and the response body. Headers and main content are separated by a combination of **carriage return** and a **line feed**(CR-LF) characters. In a CRLF injection attack, the attacker inserts CRLF characters into user input form or an HTTP request to trick the web server or web application into thinking that header ends here and main content begins.   
  
There are 2 most common uses of CRLF injection attacks:  
**a) Log poisoning**. In this attack, the attacker modifies the log file entries by inserting '\\n' and an extra line of text. This can be used to hide other attacks or to confuse system administrators by damaging the structure or formatting of the log file.  
Take the example of a log file which has a pattern IPAddress - time - URL.  
`106.217.24.193 - 07:26 - /author/book/?sort_by=rating  
`and an attacker managed to inserts CLRF characters in the URL, above log file would look like below  
`106.217.24.193 - 07:26 - /author/book/?sort_by=rating&%0d%0a87.200.169.16 - 13:45 - /author/profile`

**b)** **HTTP response splitting** (AKA **header injection**)  
Web application frameworks and servers might also allow attackers to inject newline characters in headers to create a malformed HTTP response. In this case, the application would be vulnerable to attacks like HTTP Response Splitting/Smuggling.

Consider below examples-

```python
from django.http import HttpResponse

def my_view(request):
    content_type = request.META.get("CONTENT_TYPE")
    response = HttpResponse()
    response['Content-Type'] = content_type  #
    return response
```

Here `content_type` hasn't been validated and an attacker can pass any malicious header that includes '\\n' in it. As a best practice, applications that use user-provided data to construct the response header should always validate the data first. So instead of the above implementation, we'd use below approach.

```python
from django.http import HttpResponse

def my_view(request):
    content_type = request.META.get("CONTENT_TYPE")
    response = HttpResponse()
    if content_type in ALLOWED_CONTENT_TYPES:
        response['Content-Type'] = content_type
    else: # default content type
        response['Content-Type'] = "application/json"
    return response
```

By exploiting a CRLF injection an attacker can also insert HTTP headers which could be used to defeat security mechanisms such as a browser's XSS filter or the same-origin-policy.  
Django handles header injection out of the box If any  `subject`, `from_email` or `recipient_list`  contains a newline, the email function (e.g. [`send_mail()`](https://docs.djangoproject.com/en/3.0/topics/email/#django.core.mail.send_mail)) will raise `BadHeaderError`

```python
from django.core.mail import BadHeaderError, send_mail
try:
    send_mail(subject, message, from_email, to_emails)
except BadHeaderError:
    return HttpResponse('Invalid header found.')
```

Alternatively you can explicitly check for these characters. [This is what Django does under the hood](https://github.com/django/django/blob/ccb1cfb64e919e163c51995ed99bff3c92d7d006/django/core/mail/message.py#L55).

```python
if '\n' in input_text or '\r' in input_text:
    raise BadHeaderError('Header cannot contain CLRF characters')
```

CRLF injection vulnerabilities are usually mitigated by Django automatically. Even if the vulnerability is not mitigated, it is easy to fix by following below steps.

- Update the code so that content provided by the user is never used directly in the HTTP stream.
- Remove any CR-LF characters before passing content into the HTTP headers.
- Encode the data that you pass into HTTP headers. This will encode the CR & LF if the attacker attempts to inject them.

#### 3\. Timing Attack

As per Wikipedia, _a timing attack is an attack in which the attacker attempts to compromise a cryptosystem by analyzing the time taken to execute cryptographic algorithms_. What does that mean? Basically an attacker would supply different inputs to the system and observe the precise time taken by the system to respond for each input. Let's understand this by a simple example.

Suppose you have a function that check the API key or token provided by user.

```python
def is_valid_key(api_key):
    return api_key == SECURELY_STORED_API_KEY
```

Here problem is in **\==** operator. The way python compare string under the hood is byte by byte(or character by character) and it gets terminated as soon as it finds a non-matching byte before iterating over the whole string. If the first character(or byte) of the input **api\_key** string is different than the first character of **STORED\_API\_KEY** string, it will return the result comparatively faster than the case where both strings are equal.  
In layman terms, the comparison between '**abcdefgh**' and '****xbcdefgh****' would return result faster than comparison between '****abcdefgh****' and '****abcdefgh****'.  
Attackers can use this to determine the bytes one by one and eventually a valid string. How can you make sure that your function always takes constant time no matter what input user provides? Again, Django to the rescue! Django provides a nice utility function for that [constant\_time\_compare](https://github.com/django/django/blob/stable/3.0.x/django/utils/crypto.py#L49). Django internally uses this function to compare the password for authentication.

```python
from django.utils.crypto import constant_time_compare
constant_time_compare(string1, string2)
```

If you want to, for some reason, implement it by yourself in Python, you can do -

```python
def compare(string1, string2):
    if len(string1) != len(string2):
        return False
    result = 0
    for a, b in zip(string1, string2):
        result |= ord(a) ^ ord(b)  # XOR of Ascii value of characters
        # We are doing an OR operation between the `result` and XOR result.
        # If both strings are equal, XOR will be 0 for all characters and thus result would be 0

    return not result   # Equivalent to: return result == 0
```

This loop will keep running even if it finds the non-matching character and hence will always take the same time to compute and return the result.

Read also: [https://docs.python.org/3/library/hmac.html#hmac.compare\_digest](https://docs.python.org/3/library/hmac.html#hmac.compare_digest)

#### 4\. Clickjacking Attack

Clickjacking (click + hijacking), AKA **User Interface redress attack**, **UI redress attack**, **UI redressing**, is a type of attack where a malicious site wraps another site in an invisible frame. This attack can trick the user into clicking a webpage element which is invisible or disguised as another element for malicious purpose.  
Modern browsers use the [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options) HTTP header that indicates whether or not a resource is allowed to load within a frame or iframe.

Django provides a middleware to guard against it.

```python
MIDDLEWARE = (
    ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ...
)
```

In Django 3.0 or above, by default, it will set the **X-Frame-Options** header to **DENY**. On the other hand, in Django < 3.0, the default value for this header is **SAMEORIGIN**.  
**DENY** means, your site cannot be used in any frame/iframe on any site.  
**SAMEORIGIN** means, only your site is allowed to use itself in a frame.  
Nevertheless, if you want to change the value, you can use X\_FRAME\_OPTIONS setting to set the desired value.

```python
X_FRAME_OPTIONS = 'DENY'  # in settings.py
```

Django also provides some decorators to do it per view basis. This is extremely useful when you want custom behaviour per view. These decorators will override the middleware setting.

```python
from django.views.decorators.clickjacking import (
    xframe_options_deny,
    xframe_options_exempt,
    xframe_options_sameorigin
)

@xframe_options_exempt
def view1(request):
    return HttpResponse("This pages is safe to load in a frame on any site.")

@xframe_options_deny
def view2(request):
    return HttpResponse("Don't display in any frame, anywhere!")

@xframe_options_sameorigin
def view3(request):
    return HttpResponse("Display in a frame if it's from the same origin as me.")
```

As a best security practice always set this value to DENY.

#### 5\. Cross-Site Scripting (XSS)

XSS attacks allow an attacker to inject scripts into the browsers of other users. This is usually achieved by storing the malicious scripts in the database and then serve to other users when they make a request to the database. We'll see different approaches Django provides to prevent these attacks.

**a) Validating user input / HTML escaping  
**By default, Django templates protect you against the majority of XSS attacks by applying HTML escaping to the output of all template variables but that's not enough and you should always explicitly sanitize user-provided data. Consider the below example -

```python
name = request.GET.get('name')
html = '<p>Hello, My name is %s</p>' % name
```

If the user provides below JS code in the **name** param, this will be executed on the page where we are rendering this HTML.

```javascript
<script type="text/javascript">alert("Error")</script>
```

**b) Enable browser detector**  
If your application still supports old browsers, you should consider having [SECURE\_BROWSER\_XSS\_FILTER](https://docs.djangoproject.com/en/3.0/ref/settings/#secure-browser-xss-filter) setting turn on. This header basically tells the browser to enable the auto XSS attack detector feature. This is redundant in modern browsers because they don't consider **X-XSS-Protection** HTTP header anymore.

**c) Protect Cookies**  
Another small step you can take is by enabling [SESSION\_COOKIE\_HTTPONLY](https://docs.djangoproject.com/en/3.0/ref/settings/#session-cookie-httponly) settings. By default, it's True so no need to do anything here but if in the past, you have disabled it for some reason it's a good time to revisit it. Having this setting enables allow cookies to be accessible on only HTTP(S) requests, Javascript can't access cookies.

But wouldn't it be great if there was a way that allows us to execute only our site's(verified) JavaScripts?

**d) Content-Security-Policy**  
You can do that by setting the [Content-Security-Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) HTTP header. Browsers will not load any JS, CSS, Images that are not permitted by CSP header, including inline JS. How can we do that using Django?  
Django doesn't have any inbuilt support for this but you can use a very popular 3rd party package called [django-csp](https://github.com/mozilla/django-csp), maintained by Mozilla.

Add CSP middleware provided by this library

```python
MIDDLEWARE = (
    # ...
    'csp.middleware.CSPMiddleware',
    # ...
)
```

And add below configuration to your site's setting. Note that this can vary based on your site's requirements.

```python
CSP_DEFAULT_SRC = ("'self'", 'cdn.example.net')
CSP_STYLE_SRC = ("'self'", 'fonts.googleapis.com')
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)
# More CSP settings go here ... https://django-csp.readthedocs.io/en/latest/configuration.html#policy-settings
```

In the end, I'd say preventing XSS attack is tricky and no single approach will fully protect you instead use a combination of multiple approaches mentioned above.

#### 6\. Cross-Site Request Forgery (CSRF)

AKA **one-click attack** or **session riding** or **XSRF**, sometimes pronounced "sea-surf", is an attack where a user is tricked by an attacker into submitting a web request that they did not intend.

Consider a simple example where you can send money from your bank account to another by simply filling a form that takes two fields, receiver's account number and the amount you want to send. In this case, an attacker can send you a hidden form through an email or a web link and If you click on that link while you are logged in your bank account, you un-intentionally sent money to the attacker's account. Similarly, The attacker can trick you to send your active cookies and later attacker can use them to gain access to the vulnerable site.

Using CSRF token is a robust safeguard against this attack. A CSRF token is a unique token generated by the application for each session, request or ID. Django provides a very easy way to Include CSRF token in your forms. There is middleware for this in Django that by default will be added to your MIDDLEWARE setting. **"django.middleware.csrf.CsrfViewMiddleware"**. What else you need to do is, if you are using Django's templating system, use **csrf\_token** (for Jinja2 it's **csrf\_input**) tag inside the form.

```django
<form method="post">
{% csrf_token %}
...
</form>
```

Additionally you can turn on below settings to protect CSRF cookies.

```python
CSRF_COOKIE_SECURE = True  # cookie will only be sent over an HTTPS connection
CSRF_COOKIE_HTTPONLY = True  # only accessible through http(s) request, JS not allowed to access csrf cookies
```

To read more about CSRF protection in Ajax, exempting specific views from CSRF protection and other limitations, please visit [official csrf docs](https://docs.djangoproject.com/en/3.0/ref/csrf/).

_Note: Django updated the [CSRF token generation mechanism in version 1.10](https://docs.djangoproject.com/en/3.0/releases/1.10/#csrf) to protect against the [BREACH attack](https://en.wikipedia.org/wiki/BREACH). If you are using an older version, I suggest upgrading to at least 1.10._

#### 7\. HTTP Strict Transport Security (HSTS)

Always serve your site over a secure connection, Always use SSL!!!  
Django provides a security middleware that can help you set a few things up quickly.

```python
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    # ...
)
```

We are going to discuss particularly 3 important settings this middleware offer.

**a) SECURE\_SSL\_REDIRECT  
**If True, the SecurityMiddleware redirects all non-HTTPS requests to HTTPS. Default is False.

```python
SECURE_SSL_REDIRECT = True
```

But the problem is, the user had already initiated the insecure request(HTTP) that we redirected to HTTPS. If an attacker managed to intercept that insecure request, things can go wrong. How can we prevent that request from happening altogether?

HSTS is the way to go!

**b) SECURE\_HSTS\_SECONDS**  
Whenever a user makes an HTTP request to your site, HSTS send a [header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) in the response that tells the browsers to always use an HTTPS connection to your site. Although as a prerequisite for this, It requires all your statics, scripts, media, fonts, everything to be served over HTTPS, otherwise users won't be able to connect to the site. The default value of this setting is Zero.

```python
SECURE_HSTS_SECONDS = 31536000  # seconds in a year:  365*24*60*60
```

Ideally, you should set a large value such as 31536000 seconds which is equal to 1 year. But if you already don't have its recommended to start with a low value e.g 86400 because if something is not right with your sites, browsers won't be able to connect to your site for this long. You can always update this number once you are sure everything is fine. Before making any changes go through the [documentation](https://docs.djangoproject.com/en/3.0/ref/settings/#secure-hsts-seconds).

**c) SECURE\_HSTS\_INCLUDE\_SUBDOMAINS**  
Setting it to True will ensure that all subdomains, not just top-level domain, can only be accessed over a secure connection. Default is False.

```python
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

What we learn from these vulnerabilities is, always validate and sanitize the user-provided data, such as URL parameters, POST data payloads, headers or cookies. Thumb rule of the security is user-provided data should always be considered untrusted and sanitized/escaped accordingly.

I hope you enjoyed the post. In the future post, I'll talk about more security features that Django provides. If you think this can be useful to others, Don't forget to share with them. Write a comment if you want to see Django in action for a specific web vulnerability.
