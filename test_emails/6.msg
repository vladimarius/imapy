Delivered-To: imapy007@gmail.com
Received: by 10.27.211.66 with SMTP id k63csp276203wlg;
        Wed, 4 Feb 2015 05:49:48 -0800 (PST)
Return-Path: <django-users+bncBCMIZRWC5ENBB5OGZCTAKGQE6LM4N7I@googlegroups.com>
Received-SPF: pass (google.com: domain of django-users+bncBCMIZRWC5ENBB5OGZCTAKGQE6LM4N7I@googlegroups.com designates 10.182.165.4 as permitted sender) client-ip=10.182.165.4
Authentication-Results: mr.google.com;
       spf=pass (google.com: domain of django-users+bncBCMIZRWC5ENBB5OGZCTAKGQE6LM4N7I@googlegroups.com designates 10.182.165.4 as permitted sender) smtp.mail=django-users+bncBCMIZRWC5ENBB5OGZCTAKGQE6LM4N7I@googlegroups.com;
       dkim=pass header.i=@googlegroups.com
X-Received: from mr.google.com ([10.182.165.4])
        by 10.182.165.4 with SMTP id yu4mr2781829obb.26.1423057788661 (num_hops = 1);
        Wed, 04 Feb 2015 05:49:48 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=googlegroups.com; s=20120806;
        h=date:from:to:subject:content-type:mime-version:message-id
         :x-original-sender:x-original-authentication-results:reply-to
         :precedence:mailing-list:list-id:list-post:list-help:list-archive
         :sender:list-subscribe:list-unsubscribe;
        bh=MaSbZeA84f2P8EsKqtAOogTfQtZ4jzIsjKXscasl33g=;
        b=ydvuOKkq1XcxQkc1oXQG2cv1A+RV5umbaNUNnxG0VsgcxDAup+LIS9Xt8zm8PpOCRd
         GEzCH+P7woK+Ec0RkAatAMDd3bWPfmijQ9bflfV1vJ+NPENovrPvGmZpLWkyiBpzlkyH
         48Fw+ambx4EwcX4SWV0HZM8MGP1+cVZ3ObXTD+yDvRpm/qFyXXZBu/v7oBsEmRs+qU1a
         /S6omgzHnMGzvcGxSvwsGAa5d8QbgjBQZiY6KJcHaX7Q2tmC455AZx2n0i0PHVcB5i5R
         oeFvYBelIO9kikC5Y0z4z/ASFq6odfAA+M0neT/GJaR09QI1ccZ4Ogf62qY6UQyB1ORk
         jVgw==
X-Received: by 10.182.165.4 with SMTP id yu4mr200588obb.26.1423057788127;
        Wed, 04 Feb 2015 05:49:48 -0800 (PST)
X-BeenThere: django-users@googlegroups.com
Received: by 10.182.181.66 with SMTP id du2ls30866obc.39.gmail; Wed, 04 Feb
 2015 05:49:41 -0800 (PST)
X-Received: by 10.182.22.45 with SMTP id a13mr7731078obf.5.1423057781135;
        Wed, 04 Feb 2015 05:49:41 -0800 (PST)
Received: from m13-4.163.com (m13-4.163.com. [120.192.14.3])
        by gmr-mx.google.com with ESMTP id x16si1552686igx.0.2015.02.04.05.49.39
        for <django-users@googlegroups.com>;
        Wed, 04 Feb 2015 05:49:41 -0800 (PST)
Received-SPF: pass (google.com: domain of abcdef11@163.com designates 120.192.14.3 as permitted sender) client-ip=120.192.14.3;
Received: from abcdef11$163.com ( [1.85.9.19] ) by ajax-webmail-wmsvr4
 (Coremail) ; Wed, 4 Feb 2015 21:48:47 +0800 (CST)
X-Originating-IP: [1.85.9.19]
Date: Wed, 4 Feb 2015 21:48:47 +0800 (CST)
From: =?GBK?B?wM/VxQ==?= <abcdef11@163.com>
To: django-users@googlegroups.com
Subject: how to put files in different dirs
X-Priority: 3
X-Mailer: Coremail Webmail Server Version SP_ntes V3.5 build
 20150119(59087.7062) Copyright (c) 2002-2015 www.mailtech.cn 163com
X-CM-CTRLDATA: pVMuuGZvb3Rlcl9odG09NTEzOjgx
Content-Type: multipart/alternative;
	boundary="----=_Part_219048_473945711.1423057727005"
MIME-Version: 1.0
Message-ID: <432f4709.db54.14b54d9ae1d.Coremail.abcdef11@163.com>
X-CM-TRANSID: BMGowADX3LhAI9JUmAtOAA--.18149W
X-CM-SenderInfo: 5sdlx2qtruqiywtou0bp/xtbBDgCWS1QGwSclkAAAsS
X-Coremail-Antispam: 1U5529EdanIXcx71UUUUU7vcSsGvfC2KfnxnUU==
X-Original-Sender: abcdef11@163.com
X-Original-Authentication-Results: gmr-mx.google.com;       spf=pass
 (google.com: domain of abcdef11@163.com designates 120.192.14.3 as permitted
 sender) smtp.mail=abcdef11@163.com;       dkim=pass header.i=@163.com
Reply-To: django-users@googlegroups.com
Precedence: list
Mailing-list: list django-users@googlegroups.com; contact django-users+owners@googlegroups.com
List-ID: <django-users.googlegroups.com>
X-Google-Group-Id: 338756077141
List-Post: <http://groups.google.com/group/django-users/post>, <mailto:django-users@googlegroups.com>
List-Help: <http://groups.google.com/support/>, <mailto:django-users+help@googlegroups.com>
List-Archive: <http://groups.google.com/group/django-users
Sender: django-users@googlegroups.com
List-Subscribe: <http://groups.google.com/group/django-users/subscribe>, <mailto:django-users+subscribe@googlegroups.com>
List-Unsubscribe: <mailto:googlegroups-manage+338756077141+unsubscribe@googlegroups.com>,
 <http://groups.google.com/group/django-users/subscribe>

------=_Part_219048_473945711.1423057727005
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

hi . Guys
i'm designing a django web site,which produce many files.
if all these files are in ONE directory=E3=80=82i'm afraid that performance=
 is a problem.
even i can put many entries in  stattic-dirs in setting.py.but it seems onl=
y one entry in stattic-dirs be used
Can anyone tell me how  i  can put files in different dirs , or in differen=
t dirs with same parent dir ?
Thanks !



--=20
You received this message because you are subscribed to the Google Groups "=
Django users" group.
To unsubscribe from this group and stop receiving emails from it, send an e=
mail to django-users+unsubscribe@googlegroups.com.
To post to this group, send email to django-users@googlegroups.com.
Visit this group at http://groups.google.com/group/django-users.
To view this discussion on the web visit https://groups.google.com/d/msgid/=
django-users/432f4709.db54.14b54d9ae1d.Coremail.abcdef11%40163.com.
For more options, visit https://groups.google.com/d/optout.

------=_Part_219048_473945711.1423057727005
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

<div style=3D"line-height:1.7;color:#000000;font-size:14px;font-family:Aria=
l"><div>hi . Guys<br>i'm designing a django web site,which produce many fil=
es.<br>if all these files are in ONE directory=E3=80=82i'm afraid that perf=
ormance is a problem.<br>even i can put many entries in&nbsp; stattic-dirs =
in setting.py.but it seems only one entry in stattic-dirs be used<br>Can an=
yone tell me how&nbsp; i&nbsp; can put files in different dirs , or in diff=
erent dirs with same parent dir ?<br>Thanks !<br><br><br><br></div></div><b=
r><br><span title=3D"neteasefooter"><span id=3D"netease_mail_footer"></span=
></span>

<p></p>

-- <br />
You received this message because you are subscribed to the Google Groups &=
quot;Django users&quot; group.<br />
To unsubscribe from this group and stop receiving emails from it, send an e=
mail to <a href=3D"mailto:django-users+unsubscribe@googlegroups.com">django=
-users+unsubscribe@googlegroups.com</a>.<br />
To post to this group, send email to <a href=3D"mailto:django-users@googleg=
roups.com">django-users@googlegroups.com</a>.<br />
Visit this group at <a href=3D"http://groups.google.com/group/django-users"=
>http://groups.google.com/group/django-users</a>.<br />
To view this discussion on the web visit <a href=3D"https://groups.google.c=
om/d/msgid/django-users/432f4709.db54.14b54d9ae1d.Coremail.abcdef11%40163.c=
om?utm_medium=3Demail&utm_source=3Dfooter">https://groups.google.com/d/msgi=
d/django-users/432f4709.db54.14b54d9ae1d.Coremail.abcdef11%40163.com</a>.<b=
r />
For more options, visit <a href=3D"https://groups.google.com/d/optout">http=
s://groups.google.com/d/optout</a>.<br />

------=_Part_219048_473945711.1423057727005--

