Delivered-To: imapy-test@gmail.com
Received: by 10.27.54.203 with SMTP id d194csp2735858wla;
        Wed, 29 Apr 2015 06:46:50 -0700 (PDT)
X-Received: by 10.52.136.66 with SMTP id py2mr11058560vdb.75.1430315209737;
        Wed, 29 Apr 2015 06:46:49 -0700 (PDT)
Return-Path: <django-users+bncBCBNLDWJ34GBBQGBQOVAKGQEOY5YZDQ@googlegroups.com>
Received: from mail-vn0-x239.google.com (mail-vn0-x239.google.com. [2607:f8b0:400c:c0f::239])
        by mx.google.com with ESMTPS id eq1si35781275vdc.12.2015.04.29.06.46.48
        (version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);
        Wed, 29 Apr 2015 06:46:49 -0700 (PDT)
Received-SPF: pass (google.com: domain of django-users+bncBCBNLDWJ34GBBQGBQOVAKGQEOY5YZDQ@googlegroups.com designates 2607:f8b0:400c:c0f::239 as permitted sender) client-ip=2607:f8b0:400c:c0f::239;
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of django-users+bncBCBNLDWJ34GBBQGBQOVAKGQEOY5YZDQ@googlegroups.com designates 2607:f8b0:400c:c0f::239 as permitted sender) smtp.mail=django-users+bncBCBNLDWJ34GBBQGBQOVAKGQEOY5YZDQ@googlegroups.com;
       dkim=pass header.i=@googlegroups.com;
       dmarc=fail (p=NONE dis=NONE) header.from=gmail.com
Received: by mail-vn0-x239.google.com with SMTP id g62sf20957vnb.0;
        Wed, 29 Apr 2015 06:46:48 -0700 (PDT)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=googlegroups.com; s=20120806;
        h=content-type:mime-version:subject:from:in-reply-to:date
         :content-transfer-encoding:message-id:references:to
         :x-original-sender:x-original-authentication-results:reply-to
         :precedence:mailing-list:list-id:list-post:list-help:list-archive
         :sender:list-subscribe:list-unsubscribe;
        bh=m+gCeGd6K0HVL0l7gXBh4A3lmjqX+toSEnVwBeGWCAk=;
        b=t3zpJltnpfBMAHz4q4AAD4+xcg22oNfOQYSgJPQiD7o2rWVyPYsix6l32KTaipys1R
         8NdVaF56pqRhgzHkGfZULfzV2lJAgH/4jqNpyka5Zo0gCnHraNCyC0a5J9HQiggRKFDM
         T71MFERsNypWRky5TVya4jHRJFCDvUFaop9P+IMrafvb8bStEAvC0oyrXw+zb/6ffjNA
         VtH4CXcLPlPCqWuiSO3DV7Y97uQcpoRq2h4Lb6u6Cb8OBVjeoQHEbcKn3BLdr077Ol5o
         8VTXU+XO4lDDx8VkF/re1KlQe95ZWQSgRNZfOpfARaxbwE5lTijoeDtUeSPSK7LuNkcF
         hODQ==
X-Received: by 10.182.50.201 with SMTP id e9mr120497obo.30.1430315208086;
        Wed, 29 Apr 2015 06:46:48 -0700 (PDT)
X-BeenThere: django-users@googlegroups.com
Received: by 10.182.129.131 with SMTP id nw3ls337769obb.56.gmail; Wed, 29 Apr
 2015 06:46:40 -0700 (PDT)
X-Received: by 10.182.165.5 with SMTP id yu5mr15667760obb.26.1430315200678;
        Wed, 29 Apr 2015 06:46:40 -0700 (PDT)
Received: from mail-vn0-x235.google.com (mail-vn0-x235.google.com. [2607:f8b0:400c:c0f::235])
        by gmr-mx.google.com with ESMTPS id zj5si1305381vdb.1.2015.04.29.06.46.40
        for <django-users@googlegroups.com>
        (version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);
        Wed, 29 Apr 2015 06:46:40 -0700 (PDT)
Received-SPF: pass (google.com: domain of fschiettecatte@gmail.com designates 2607:f8b0:400c:c0f::235 as permitted sender) client-ip=2607:f8b0:400c:c0f::235;
Received: by mail-vn0-x235.google.com with SMTP id g1so3314875vnb.2
        for <django-users@googlegroups.com>; Wed, 29 Apr 2015 06:46:40 -0700 (PDT)
X-Received: by 10.52.90.42 with SMTP id bt10mr4177282vdb.13.1430315200500;
        Wed, 29 Apr 2015 06:46:40 -0700 (PDT)
Received: from macpro.local (c-76-127-141-233.hsd1.ma.comcast.net. [76.127.141.233])
        by mx.google.com with ESMTPSA id zb15sm36265837vdb.11.2015.04.29.06.46.39
        for <django-users@googlegroups.com>
        (version=TLSv1 cipher=ECDHE-RSA-RC4-SHA bits=128/128);
        Wed, 29 Apr 2015 06:46:39 -0700 (PDT)
Content-Type: text/plain; charset=UTF-8
Mime-Version: 1.0 (Mac OS X Mail 8.2 \(2098\))
Subject: Re: Require code explaination
From: =?utf-8?Q?Fran=C3=A7ois_Schiettecatte?= <fschiettecatte@gmail.com>
In-Reply-To: <d0fd944b-f5b5-4a91-b228-60612ea7b333@googlegroups.com>
Date: Wed, 29 Apr 2015 09:46:37 -0400
Content-Transfer-Encoding: quoted-printable
Message-Id: <5183A208-0B24-47DC-87BD-18B5BD4ED3D2@gmail.com>
References: <f59471d6-1baa-4a36-9d3c-327684049d65@googlegroups.com> <5D141546-4D98-4ADF-B3C6-CC5D0061DC43@gmail.com> <b29c48fc-cb9d-49dd-869f-140afd5d1b6d@googlegroups.com> <D931862C-ED51-4705-95B1-318BDBEAFF8C@gmail.com> <e158ec09-020a-4b80-9913-c0e2c3eccc8a@googlegroups.com> <13BF64E2-3B83-4100-9FA1-DAFCDE8A0676@gmail.com> <d0fd944b-f5b5-4a91-b228-60612ea7b333@googlegroups.com>
To: django-users@googlegroups.com
X-Mailer: Apple Mail (2.2098)
X-Original-Sender: fschiettecatte@gmail.com
X-Original-Authentication-Results: gmr-mx.google.com;       spf=pass
 (google.com: domain of fschiettecatte@gmail.com designates
 2607:f8b0:400c:c0f::235 as permitted sender) smtp.mail=fschiettecatte@gmail.com;
       dkim=pass header.i=@gmail.com;       dmarc=pass (p=NONE dis=NONE) header.from=gmail.com
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

Well the response does not seem to contain the audio file, to the best of m=
y knowledge Django does not implement X-Accel-Redirect, are you running all=
 this on the same machine? Maybe your browser is getting the file ? Seems u=
nlikely. Have you tried something like =E2=80=98curl=E2=80=99 to make the r=
equest in debug mode to see what is coming over the wire back from Django?

F.

> On Apr 29, 2015, at 8:28 AM, Anubhav Kaushik <anubhavgreen41@gmail.com> w=
rote:
>=20
> yes i am working on this code but  i havnt wrote this code otherwise i wo=
uld not have required the explaination i guess.
>=20
> and for your second question , i am not sure coz  as you said it looked l=
ike nginx directive , but i am running it on default wsgi server included i=
n django . so i am asking how wsgi server is serving what a nginx is suppos=
ed to serve?
>=20
> On Wednesday, April 29, 2015 at 5:35:26 PM UTC+5:30, Fran=C3=A7ois Schiet=
tecatte wrote:
> You need to be a little more specific about what the context is, and what=
 you are observing, rather than just plastering up some code.=20
>=20
> - Is this code in an app you are working with ? Did you write this code ?=
=20
>=20
> - Is the audio file being served by your application through the  default=
 wsgi server included in django?=20
>=20
> F.=20
>=20
> > On Apr 29, 2015, at 7:55 AM, Anubhav Kaushik <anubhav...@gmail.com> wro=
te:=20
> >=20
> >  but i am not running ny nginx server , m just running default wsgi ser=
ver with django ,and files are still served file ,can you explain how that =
is happening?=20
> >=20
> > On Wednesday, April 29, 2015 at 5:10:56 PM UTC+5:30, Fran=C3=A7ois Schi=
ettecatte wrote:=20
> > I found this page which was pretty clear I think:=20
> >=20
> >         http://wiki.nginx.org/XSendfile=20
> >  =20
> > Looks like an nginx directive to serve a file as the content of the res=
ponse.=20
> >=20
> > F.=20
> >=20
> > > On Apr 29, 2015, at 7:28 AM, Anubhav Kaushik <anubhav...@gmail.com> w=
rote:=20
> > >=20
> > > yes francois ,when i searched the term ,all i got was links related t=
o nginx.=20
> > >=20
> > > On Wednesday, April 29, 2015 at 4:55:58 PM UTC+5:30, Fran=C3=A7ois Sc=
hiettecatte wrote:=20
> > > Which part do you mean? The 'X-Accel-Redirect=E2=80=99 ?=20
> > >=20
> > > Fran=C3=A7ois=20
> > >=20
> > > > On Apr 29, 2015, at 6:08 AM, Anubhav Kaushik <anubhav...@gmail.com>=
 wrote:=20
> > > >=20
> > > >     response =3D HttpResponse()=20
> > > >    =20
> > > >     protected =3D settings.PROTECTED_AUDIO_ROOT + path=20
> > > >=20
> > > >     logger.info('Protected path: %s', protected)=20
> > > >=20
> > > >     response["X-Accel-Redirect"] =3D protected=20
> > > >=20
> > > >     response["Content-Type"] =3D "audio/mpeg"=20
> > > >    =20
> > > >     return response=20
> > > >=20
> > > > --=20
> > > > You received this message because you are subscribed to the Google =
Groups "Django users" group.=20
> > > > To unsubscribe from this group and stop receiving emails from it, s=
end an email to django-users...@googlegroups.com.=20
> > > > To post to this group, send email to django...@googlegroups.com.=20
> > > > Visit this group at http://groups.google.com/group/django-users.=20
> > > > To view this discussion on the web visit https://groups.google.com/=
d/msgid/django-users/f59471d6-1baa-4a36-9d3c-327684049d65%40googlegroups.co=
m.=20
> > > > For more options, visit https://groups.google.com/d/optout.=20
> > >=20
> > >=20
> > > --=20
> > > You received this message because you are subscribed to the Google Gr=
oups "Django users" group.=20
> > > To unsubscribe from this group and stop receiving emails from it, sen=
d an email to django-users...@googlegroups.com.=20
> > > To post to this group, send email to django...@googlegroups.com.=20
> > > Visit this group at http://groups.google.com/group/django-users.=20
> > > To view this discussion on the web visit https://groups.google.com/d/=
msgid/django-users/b29c48fc-cb9d-49dd-869f-140afd5d1b6d%40googlegroups.com.=
=20
> > > For more options, visit https://groups.google.com/d/optout.=20
> >=20
> >=20
> > --=20
> > You received this message because you are subscribed to the Google Grou=
ps "Django users" group.=20
> > To unsubscribe from this group and stop receiving emails from it, send =
an email to django-users...@googlegroups.com.=20
> > To post to this group, send email to django...@googlegroups.com.=20
> > Visit this group at http://groups.google.com/group/django-users.=20
> > To view this discussion on the web visit https://groups.google.com/d/ms=
gid/django-users/e158ec09-020a-4b80-9913-c0e2c3eccc8a%40googlegroups.com.=
=20
> > For more options, visit https://groups.google.com/d/optout.=20
>=20
>=20
> --=20
> You received this message because you are subscribed to the Google Groups=
 "Django users" group.
> To unsubscribe from this group and stop receiving emails from it, send an=
 email to django-users+unsubscribe@googlegroups.com.
> To post to this group, send email to django-users@googlegroups.com.
> Visit this group at http://groups.google.com/group/django-users.
> To view this discussion on the web visit https://groups.google.com/d/msgi=
d/django-users/d0fd944b-f5b5-4a91-b228-60612ea7b333%40googlegroups.com.
> For more options, visit https://groups.google.com/d/optout.

--=20
You received this message because you are subscribed to the Google Groups "=
Django users" group.
To unsubscribe from this group and stop receiving emails from it, send an e=
mail to django-users+unsubscribe@googlegroups.com.
To post to this group, send email to django-users@googlegroups.com.
Visit this group at http://groups.google.com/group/django-users.
To view this discussion on the web visit https://groups.google.com/d/msgid/=
django-users/5183A208-0B24-47DC-87BD-18B5BD4ED3D2%40gmail.com.
For more options, visit https://groups.google.com/d/optout.
