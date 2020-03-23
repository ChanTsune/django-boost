from django_boost.test import TestCase
from django_boost.utils import Loop, isiterable, loop
from django_boost.utils.attribute import (getattr_chain, getattrs,
                                          hasattr_chain, hasattrs)
from django_boost.utils.functions import loopfirst, loopfirstlast, looplast


class TestUtilFunction(TestCase):

    test_list0 = []
    test_list1 = [0]
    test_list2 = [0, 1]
    test_list3 = [0, 1, 2]

    def test_loopfirst(self):
        collect = [True, False, False]
        for is_first, v in loopfirst(self.test_list0):
            self.assertEqual(collect[v], is_first)
        for is_first, v in loopfirst(self.test_list1):
            self.assertEqual(collect[v], is_first)
        for is_first, v in loopfirst(self.test_list2):
            self.assertEqual(collect[v], is_first)
        for is_first, v in loopfirst(self.test_list3):
            self.assertEqual(collect[v], is_first)

    def test_looplast(self):
        for is_last, v in looplast(self.test_list0):
            self.assertEqual([True][v], is_last)
        for is_last, v in looplast(self.test_list1):
            self.assertEqual([True][v], is_last)
        for is_last, v in looplast(self.test_list2):
            self.assertEqual([False, True][v], is_last)
        for is_last, v in looplast(self.test_list3):
            self.assertEqual([False, False, True][v], is_last)

    def test_loopfirstlast(self):
        for is_first_or_last, v in loopfirstlast(self.test_list0):
            self.assertEqual([True][v], is_first_or_last)
        for is_first_or_last, v in loopfirstlast(self.test_list1):
            self.assertEqual([True][v], is_first_or_last)
        for is_first_or_last, v in loopfirstlast(self.test_list2):
            self.assertEqual([True, True][v], is_first_or_last)
        for is_first_or_last, v in loopfirstlast(self.test_list3):
            self.assertEqual([True, False, True][v], is_first_or_last)

    def test_isiterable(self):
        self.assertTrue(isiterable(range(1)))
        self.assertFalse(isiterable(1))


class TestLoop(TestCase):
    items = [0, 1, 2, 3]

    def test_loop_class(self):
        expected_first = [True, False, False, False]
        expected_last = [False, False, False, True]
        expected_counter0 = [0, 1, 2, 3]
        expected_revcounter0 = reversed(expected_counter0)
        for (forloop, _), first, last, counter0, revcounter0 in zip(
            Loop(self.items),
            expected_first,
            expected_last,
            expected_counter0,
                expected_revcounter0):
            self.assertEqual(forloop.first, first)
            self.assertEqual(forloop.last, last)
            self.assertEqual(forloop.counter, counter0 + 1)
            self.assertEqual(forloop.counter0, counter0)
            self.assertEqual(forloop.revcounter, revcounter0 + 1)
            self.assertEqual(forloop.revcounter0, revcounter0)
        for (forloop1, _), (forloop2, _) in zip(
            Loop(self.items),
                loop(self.items)):
            self.assertEqual(forloop1.first, forloop2.first)
            self.assertEqual(forloop1.last, forloop2.last)
            self.assertEqual(forloop1.counter, forloop2.counter)
            self.assertEqual(forloop1.counter0, forloop2.counter0)
            self.assertEqual(forloop1.revcounter, forloop2.revcounter)
            self.assertEqual(forloop1.revcounter0, forloop2.revcounter0)


class TestAttribute(TestCase):

    def test_getattrs(self):
        i = 1

        self.assertEqual(getattrs(i, '__class__', '__doc__'),
                         (i.__class__, i.__doc__))
        self.assertEqual(getattrs(i, '__class__', 'class',
                                  default=None), (i.__class__, None))
        with self.assertRaises(AttributeError):
            getattrs(i, '__class__', 'class')

    def test_getattr_chain(self):
        i = 1
        self.assertEqual(getattr_chain(
            i, '__class__.__name__'), i.__class__.__name__)

        with self.assertRaises(AttributeError):
            getattr(i, '__class__.name')

    def test_hasatttrs(self):
        i = 1
        self.assertTrue(hasattrs(i, '__class__', '__doc__'))
        self.assertFalse(hasattrs(i, '__class__', 'doc'))

    def test_hasatttr_chain(self):
        i = 1
        self.assertTrue(hasattr_chain(i, '__class__.__name__'))
        self.assertFalse(hasattr_chain(i, '__class__.doc'))


class TestItertools(TestCase):

    def test_chunked(self):
        from django_boost.utils.itertools import chunked

        iterable = range(5)

        expect_cases = (
            [0, 1, 2],
            [3, 4]
        )
        for sub_iterable, expect in zip(chunked(iterable, 3), expect_cases):
            self.assertEqual(list(sub_iterable), expect)

    def test_chunked_just(self):
        from django_boost.utils.itertools import chunked

        iterable = range(6)

        expect_cases = (
            [0, 1, 2],
            [3, 4, 5]
        )
        for sub_iterable, expect in zip(chunked(iterable, 3), expect_cases):
            self.assertEqual(list(sub_iterable), expect)

    def test_chunked_single(self):
        from django_boost.utils.itertools import chunked

        iterable = range(2)

        expect_cases = (
            [0, 1],
        )
        for sub_iterable, expect in zip(chunked(iterable, 3), expect_cases):
            self.assertEqual(list(sub_iterable), expect)


HTML_TEXT = """
<!DOCTYPE html>
<html>

<head>
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>[Django] カスタムユーザーを利用する | エンジニアもどきの技術メモ</title>
    

    
<meta name="format-detection" content="telephone=no">
<meta name="description" content="Djangoのユーザー認証をDjango標準のUserモデルではなく自分で定義したものを利用するメモです。  
カスタムユーザー
Djangoでカスタムユーザーを利用する場合は大きく以下の三つに...">
<meta name="author" content="@iniad_0425">
<link rel="canonical" href="https://e-tec-memo.herokuapp.com/article/124/">
<meta property="og:description" content="Djangoのユーザー認証をDjango標準のUserモデルではなく自分で定義したものを利用するメモです。  
カスタムユーザー
Djangoでカスタムユーザーを利用する場合は大きく以下の三つに...">
<meta property="og:site_name" content="e-tec-memo">
<meta property="og:title" content="[Django] カスタムユーザーを利用する">
<meta property="og:type" content="article">
<meta property="og:url" content="/article/124/">
<meta property="og:image" content="https://e-tec-memo.herokuapp.com/static/icon/icon.a8cdea720323.png" />
<meta name="twitter:site" content="@iniad_0425">
<meta name="twitter:card" content="summary">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="技術メモ">
<link rel="apple-touch-icon" href="/static/icon/icon.a8cdea720323.png">
<link rel="shortcut icon" href="/static/icon/icon.a8cdea720323.png">
<link href="https://e-tec-memo.herokuapp.com/rss/latest/feed/" title="RSS" type="application/rss+xml" rel="alternate">

    

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
  integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<link rel="stylesheet" type="text/css" href="/static/css/style.dd57639b0990.css" />
<link rel="stylesheet" type="text/css" href="/static/css/social-icon.56761d3179df.css">

<link rel="stylesheet" href="/static/css/highlight.min.c638ff1a24aa.css">
<style>
.p-relative {
    position: relative;
}
.markdown-body .highlight{
    margin-right:-1rem;
    margin-left:-1rem;
    border-left: 3px solid var(--color-primary);
}
</style>

    
</head>
<body>

<nav class="navbar navbar-expand-sm sticky-top navbar-inverse bg-inverse navbar-header py-0">
  <a href="/"><img src="/static/icon/icon.a8cdea720323.png" alt="icon" class="icon rotate-hover"></a>
  <input type="checkbox" id="navbar-toggler">
  <label for="navbar-toggler" class="navbar-toggler border-0 p-0">
    <span class="menu-text" id="text-m"></span>
    <span class="box"><span class="bar"></span><span class="bar"></span><span class="bar"></span></span>
    <span class="menu-text" id="text-n"></span>
    <span class="menu-text" id="text-u"></span>
  </label>
  <div class="navbar-collapse" id="navbarNav">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item ">
        <a class="nav-link" href="/">エンジニアもどきの技術メモ</a>
      </li>
      <li class="nav-item ">
        <a class="nav-link" href="/article/">すべてのメモ</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/tools/">ツール</a>
      </li>
      
    </ul>
    <form class="search_container" method="GET" action="/search/">
      <input name="q" type="text" size="25" placeholder=" keyword search">
      <input type="submit" value="  " style="background-image: url('/static/svgs/solid/search.55473c271992.svg');">
    </form>
  </div>
</nav>



<div class="breadcrumb-container">
  <ul class="breadcrumb-list" vocab="https://schema.org/" typeof="BreadcrumbList">
    

    <li class="" property="itemListElement" typeof="ListItem">
      <a class="breadcrumb-link" href="/" property="item" typeof="WebPage">
        <span class="svg-as-font"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31A12 12 0 0 0 45.15 301l235.22-193.74a12.19 12.19 0 0 1 15.3 0L530.9 301a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"/></svg></span>
      </a>
    </li>
    
<li property="itemListElement" typeof="ListItem">
    <a class="breadcrumb-link" href="/article/" property="item" typeof="WebPage">
        <span property="name">すべてのメモ</span>
    </a>
</li>
<li property="itemListElement" typeof="ListItem">
    <a class="breadcrumb-link" href="/article/124/" property="item" typeof="WebPage">
        <span property="name">[Django] カスタムユーザーを利用する</span>
    </a>
</li>

  </ul>
</div>


<div class="content-container">

<div class="content">
    <div class="article-container">
        
<div class="article bg-white p-3 p-relative">
    <div class="article-info">
        <small>2020年3月18日12:31に更新</small>
        <small>30views</small>
    </div>
    <div class="article-tool-box">
        <input type="checkbox" id="article-tool-box-check" class="article-tool-box-check">
        <label for="article-tool-box-check">
            <i class="tool-box-button-dot"></i>
            <i class="tool-box-button-dot"></i>
            <i class="tool-box-button-dot"></i>
        </label>
        <div class="tool-box-list shadow">
            <div>
                <a href="/article/124.md">Markdownで本文を見る</a>
            </div>
            <div>
                <a href="/form/opinion/?text=[Django] カスタムユーザーを利用するに関する問題報告">このメモに関する問題を報告する</a>
            </div>
            
        </div>
    </div>
    <h2 id="[Django] カスタムユーザーを利用する">[Django] カスタムユーザーを利用する</h2>
    <div>
        
        <a class="badge badge-danger" href="/tag/django/">django</a>
        
    </div>
</div>

<div class="markdown-body bg-white p-3">
        <p>Djangoのユーザー認証をDjango標準の<code>User</code>モデルではなく自分で定義したものを利用するメモです。  </p>
<h2 id="カスタムユーザー">カスタムユーザー</h2>
<p>Djangoでカスタムユーザーを利用する場合は大きく以下の三つに分類できます。  </p>
<ul>
<li>データベースのリレーションを利用する  </li>
<li><code>AbstractUser</code>を継承する  </li>
<li><code>AbstractBaseUser</code>を継承する  </li>
</ul>
<p>一つ目はDjango標準の<code>User</code>モデルに<code>OneToOneField</code>や<code>ForeignKey</code>を利用してリレーションを持たせる方法です。<br />
厳密にはカスタムユーザーではありませんが、お手軽に実装できます。  </p>
<p>二つ目は<code>AbstractUser</code>を継承する方法です。<br />
こちらは標準<code>User</code>モデルが持っているフィールドは全て持っているので、フィールドを追加したい場合におススメです。  </p>
<p>三つ目は<code>AbstractBaseUser</code>を継承する方法です。<br />
こちらは最低限のフィールド、機能以外は持っていないのでフィールドを削りたい場合や動作を柔軟に定義したい場合におススメです。<br />
ただし、柔軟に定義できる分記述する量も増えてきます。  </p>
<h2 id="メールアドレスでログインするユーザー">メールアドレスでログインするユーザー</h2>
<p>今回は、ログイン時、登録時にユーザー名ではなくメールアドレスを利用するケースを考えます。  </p>
<h3 id="AbstractUser">AbstractUser</h3>
<p>まずは、お手軽な<code>AbstractUser</code>を継承する方法から  </p>
<h3 id="実装">実装</h3>
<h4 id="モデル">モデル</h4>
<div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">AbstractUser</span><span class="p">,</span> <span class="n">UnicodeUsernameValidator</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
<span class="kn">from</span> <span class="nn">django.utils.translation</span> <span class="kn">import</span> <span class="n">gettext_lazy</span> <span class="k">as</span> <span class="n">_</span>

<span class="k">class</span> <span class="nc">User</span><span class="p">(</span><span class="n">AbstractUser</span><span class="p">):</span>

    <span class="n">username_validator</span> <span class="o">=</span> <span class="n">UnicodeUsernameValidator</span><span class="p">()</span>
    <span class="n">username</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span>
        <span class="n">_</span><span class="p">(</span><span class="s1">&#39;username&#39;</span><span class="p">),</span>
        <span class="n">max_length</span><span class="o">=</span><span class="mi">150</span><span class="p">,</span>
        <span class="n">help_text</span><span class="o">=</span><span class="n">_</span><span class="p">(</span>
            <span class="s1">&#39;Required. 150 characters or fewer.&#39;</span>
            <span class="s1">&#39; Letters, digits and @/./+/-/_ only.&#39;</span><span class="p">),</span>
        <span class="n">validators</span><span class="o">=</span><span class="p">[</span><span class="n">username_validator</span><span class="p">],</span>
    <span class="p">)</span>
    <span class="n">email</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">EmailField</span><span class="p">(</span>
        <span class="n">_</span><span class="p">(</span><span class="s1">&#39;email address&#39;</span><span class="p">),</span>
        <span class="n">unique</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span>
        <span class="n">error_messages</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;unique&#39;</span><span class="p">:</span> <span class="n">_</span><span class="p">(</span><span class="s2">&quot;A user with that email address already exists.&quot;</span><span class="p">),</span>
        <span class="p">},</span>
    <span class="p">)</span>
    <span class="n">EMAIL_FIELD</span> <span class="o">=</span> <span class="s1">&#39;email&#39;</span>
    <span class="n">USERNAME_FIELD</span> <span class="o">=</span> <span class="s1">&#39;email&#39;</span>
    <span class="n">REQUIRED_FIELDS</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;username&#39;</span><span class="p">]</span>

    <span class="k">class</span> <span class="nc">Meta</span><span class="p">(</span><span class="n">AbstractUser</span><span class="o">.</span><span class="n">Meta</span><span class="p">):</span>
        <span class="n">swappable</span> <span class="o">=</span> <span class="s1">&#39;AUTH_USER_MODEL&#39;</span>
</pre></div>


<p>クラス変数の<code>USERNAME_FIELD</code>を<code>'email'</code>にする事でログイン時に要求されるユーザー名をメールアドレスに変更しています。  </p>
<div class="highlight"><pre><span></span>    <span class="k">class</span> <span class="n">Meta</span>(<span class="n">AbstractUser</span>.<span class="n">Meta</span>):
        <span class="n">swappable</span> = <span class="s">&#39;AUTH_USER_MODEL&#39;</span>
</pre></div>


<p>部分でDjango標準のユーザーと重複利用されるのを防いでいます。  </p>
<h3 id="AbstractBaseUser">AbstractBaseUser</h3>
<p>次に、<code>AbstractBaseUser</code>を継承する方法を紹介します。  </p>
<h3 id="実装">実装</h3>
<h4 id="モデル">モデル</h4>
<div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">django.contrib.auth.base_user</span> <span class="kn">import</span> <span class="n">AbstractBaseUser</span>
<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">PermissionsMixin</span>

<span class="k">class</span> <span class="nc">AbstractUser</span><span class="p">(</span><span class="n">AbstractBaseUser</span><span class="p">,</span> <span class="n">PermissionsMixin</span><span class="p">):</span>
    <span class="n">username_validator</span> <span class="o">=</span> <span class="n">UnicodeUsernameValidator</span><span class="p">()</span>

    <span class="n">username</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span>
        <span class="n">_</span><span class="p">(</span><span class="s1">&#39;username&#39;</span><span class="p">),</span>
        <span class="n">max_length</span><span class="o">=</span><span class="mi">150</span><span class="p">,</span>
        <span class="n">help_text</span><span class="o">=</span><span class="n">_</span><span class="p">(</span><span class="s1">&#39;Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.&#39;</span><span class="p">),</span>
        <span class="n">validators</span><span class="o">=</span><span class="p">[</span><span class="n">username_validator</span><span class="p">],</span>
        <span class="n">error_messages</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;unique&#39;</span><span class="p">:</span> <span class="n">_</span><span class="p">(</span><span class="s2">&quot;A user with that username already exists.&quot;</span><span class="p">),</span>
        <span class="p">},</span>
        <span class="n">blank</span><span class="o">=</span><span class="bp">True</span>
    <span class="p">)</span>
    <span class="n">first_name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">&#39;first name&#39;</span><span class="p">),</span> <span class="n">max_length</span><span class="o">=</span><span class="mi">30</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">last_name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">&#39;last name&#39;</span><span class="p">),</span> <span class="n">max_length</span><span class="o">=</span><span class="mi">150</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">email</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">EmailField</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">&#39;email address&#39;</span><span class="p">),</span> <span class="n">unique</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    <span class="n">is_staff</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span>
        <span class="n">_</span><span class="p">(</span><span class="s1">&#39;staff status&#39;</span><span class="p">),</span>
        <span class="n">default</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span>
        <span class="n">help_text</span><span class="o">=</span><span class="n">_</span><span class="p">(</span><span class="s1">&#39;Designates whether the user can log into this admin site.&#39;</span><span class="p">),</span>
    <span class="p">)</span>
    <span class="n">is_active</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span>
        <span class="n">_</span><span class="p">(</span><span class="s1">&#39;active&#39;</span><span class="p">),</span>
        <span class="n">default</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span>
        <span class="n">help_text</span><span class="o">=</span><span class="n">_</span><span class="p">(</span>
            <span class="s1">&#39;Designates whether this user should be treated as active. &#39;</span>
            <span class="s1">&#39;Unselect this instead of deleting accounts.&#39;</span>
        <span class="p">),</span>
    <span class="p">)</span>
    <span class="n">date_joined</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">&#39;date joined&#39;</span><span class="p">),</span> <span class="n">default</span><span class="o">=</span><span class="n">timezone</span><span class="o">.</span><span class="n">now</span><span class="p">)</span>

    <span class="n">objects</span> <span class="o">=</span> <span class="n">UserManager</span><span class="p">()</span>

    <span class="n">EMAIL_FIELD</span> <span class="o">=</span> <span class="s1">&#39;email&#39;</span>
    <span class="n">USERNAME_FIELD</span> <span class="o">=</span> <span class="s1">&#39;email&#39;</span>
    <span class="n">REQUIRED_FIELDS</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;email&#39;</span><span class="p">]</span>

    <span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
        <span class="n">verbose_name</span> <span class="o">=</span> <span class="n">_</span><span class="p">(</span><span class="s1">&#39;user&#39;</span><span class="p">)</span>
        <span class="n">verbose_name_plural</span> <span class="o">=</span> <span class="n">_</span><span class="p">(</span><span class="s1">&#39;users&#39;</span><span class="p">)</span>
        <span class="n">swappable</span> <span class="o">=</span> <span class="s1">&#39;AUTH_USER_MODEL&#39;</span>

    <span class="k">def</span> <span class="nf">clean</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">clean</span><span class="p">()</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">email</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="vm">__class__</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">normalize_email</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">email</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">get_full_name</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="n">full_name</span> <span class="o">=</span> <span class="s1">&#39;</span><span class="si">%s</span><span class="s1"> </span><span class="si">%s</span><span class="s1">&#39;</span> <span class="o">%</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">first_name</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">last_name</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">full_name</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span>

    <span class="k">def</span> <span class="nf">get_short_name</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">first_name</span>

    <span class="k">def</span> <span class="nf">email_user</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">subject</span><span class="p">,</span> <span class="n">message</span><span class="p">,</span> <span class="n">from_email</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="n">send_mail</span><span class="p">(</span><span class="n">subject</span><span class="p">,</span> <span class="n">message</span><span class="p">,</span> <span class="n">from_email</span><span class="p">,</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">email</span><span class="p">],</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
</pre></div>


<p>こちらの<code>AbstractBaseUser</code>は、パーミッション関連の機能を持っていないので、パーミッションの機能を利用したい場合は、<code>PermissionsMixin</code>を同時に継承しておく必要があります。  </p>
<p>Django標準のパーミッション機能は、実際にサービスを作る場合だと微妙に要件を満たさないことが多いので、あまり必要だと感じる機会はありませんが今回は一応継承しています。  </p>
<h4 id="マネージャー">マネージャー</h4>
<div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">django.contrib.auth.base_user</span> <span class="kn">import</span> <span class="n">BaseUserManager</span>

<span class="k">class</span> <span class="nc">UserManager</span><span class="p">(</span><span class="n">BaseUserManager</span><span class="p">):</span>
    <span class="n">use_in_migrations</span> <span class="o">=</span> <span class="bp">True</span>

    <span class="k">def</span> <span class="nf">_create_user</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">email</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">):</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">email</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s1">&#39;The given email must be set&#39;</span><span class="p">)</span>
        <span class="n">email</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">normalize_email</span><span class="p">(</span><span class="n">email</span><span class="p">)</span>
        <span class="n">username</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">model</span><span class="o">.</span><span class="n">normalize_username</span><span class="p">(</span><span class="n">username</span><span class="p">)</span>
        <span class="n">user</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">model</span><span class="p">(</span><span class="n">username</span><span class="o">=</span><span class="n">username</span><span class="p">,</span> <span class="n">email</span><span class="o">=</span><span class="n">email</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">)</span>
        <span class="n">user</span><span class="o">.</span><span class="n">set_password</span><span class="p">(</span><span class="n">password</span><span class="p">)</span>
        <span class="n">user</span><span class="o">.</span><span class="n">save</span><span class="p">(</span><span class="n">using</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">_db</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">user</span>

    <span class="k">def</span> <span class="nf">create_user</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">email</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">):</span>
        <span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">&#39;is_staff&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span>
        <span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">&#39;is_superuser&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_create_user</span><span class="p">(</span><span class="n">username</span><span class="p">,</span> <span class="n">email</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">create_superuser</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">email</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">):</span>
        <span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">&#39;is_staff&#39;</span><span class="p">,</span> <span class="bp">True</span><span class="p">)</span>
        <span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">&#39;is_superuser&#39;</span><span class="p">,</span> <span class="bp">True</span><span class="p">)</span>

        <span class="k">if</span> <span class="n">extra_fields</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;is_staff&#39;</span><span class="p">)</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">True</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s1">&#39;Superuser must have is_staff=True.&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">extra_fields</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;is_superuser&#39;</span><span class="p">)</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">True</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s1">&#39;Superuser must have is_superuser=True.&#39;</span><span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_create_user</span><span class="p">(</span><span class="n">username</span><span class="p">,</span> <span class="n">email</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">)</span>
</pre></div>


<p><code>create_superuser</code>メソッドは<code>python manage.py createsuperuser</code>コマンドの時に実行されます。  </p>
<p>今回の要件の場合は、わざわざ面倒な<code>AbstractBaseUser</code>を継承する必要はありませんでしたが、登録時に色々な操作を挟む場合はこちらの方が有用な場合があります。  </p>
<h2 id="ログイン時に利用するユーザーを変更する">ログイン時に利用するユーザーを変更する</h2>
<p>せっかく自分でカスタムユーザーを作成しても利用することを宣言しないとログイン時に利用してくれません。<br />
なのでプロジェクトの設定に先ほど作成したカスタムユーザーモデルを利用するように設定を加えます。  </p>
<div class="highlight"><pre><span></span><span class="n">AUTH_USER_MODEL</span> <span class="o">=</span> <span class="s1">&#39;アプリケーション名.User&#39;</span>
</pre></div>


<p><code>アプリケーション名</code>部分は、カスタムユーザーモデルを定義したアプリケーションの名前に置き換えてください。  </p>
<p>あとは、適宜マイグレーションを実行してください。  </p>
<h2 id="まとめ">まとめ</h2>
<ul>
<li>カスタムユーザーにフィールドを追加したい場合は<code>AbstractUser</code>を継承する  </li>
<li>カスタムユーザーをより細かくカスタムするのなら<code>AbstractBaseUser</code>を継承する</li>
<li><code>AUTH_USER_MODEL</code>の設定を忘れずに！</li>
</ul>
</div>

<ul class="social bg-white p-3">
    <li>
        <a href="https://twitter.com/intent/tweet?original_referer=https://e-tec-memo.herokuapp.com/article/124/&text=%5BDjango%5D%20%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B&url=https://e-tec-memo.herokuapp.com/article/124/" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z"/></svg>
        </a>
    </li>
    <li>
        <a href="https://getpocket.com/edit?url=https://e-tec-memo.herokuapp.com/article/124/&title=%5BDjango%5D%20%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B" target="_blank" onclick="javascript:window.open(this.href, 'pkwindow', 'width=600, height=600, personalbar=0, toolbar=0, scrollbars=1');return false;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M407.6 64h-367C18.5 64 0 82.5 0 104.6v135.2C0 364.5 99.7 464 224.2 464c124 0 223.8-99.5 223.8-224.2V104.6c0-22.4-17.7-40.6-40.4-40.6zm-162 268.5c-12.4 11.8-31.4 11.1-42.4 0C89.5 223.6 88.3 227.4 88.3 209.3c0-16.9 13.8-30.7 30.7-30.7 17 0 16.1 3.8 105.2 89.3 90.6-86.9 88.6-89.3 105.5-89.3 16.9 0 30.7 13.8 30.7 30.7 0 17.8-2.9 15.7-114.8 123.2z"/></svg>
        </a>
    </li>
    <li>
        <a href="https://b.hatena.ne.jp/entry/s/e-tec-memo.herokuapp.com/article/124/" target="_blank" onclick="javascript:window.open(this.href, 'pkwindow', 'width=600, height=600, personalbar=0, toolbar=0, scrollbars=1');return false;">
            <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Hatena Bookmark icon</title><path d="M20.47 0C22.42 0 24 1.58 24 3.53v16.94c0 1.95-1.58 3.53-3.53 3.53H3.53C1.58 24 0 22.42 0 20.47V3.53C0 1.58 1.58 0 3.53 0h16.94zm-3.705 14.47c-.78 0-1.41.63-1.41 1.41s.63 1.414 1.41 1.414 1.41-.645 1.41-1.425-.63-1.41-1.41-1.41zM8.61 17.247c1.2 0 2.056-.042 2.58-.12.526-.084.976-.222 1.32-.412.45-.232.78-.564 1.02-.99s.36-.915.36-1.48c0-.78-.21-1.403-.63-1.87-.42-.48-.99-.734-1.74-.794.66-.18 1.156-.45 1.456-.81.315-.344.465-.824.465-1.424 0-.48-.103-.885-.3-1.26-.21-.36-.493-.645-.883-.87-.345-.195-.735-.315-1.215-.405-.464-.074-1.29-.12-2.474-.12H5.654v10.486H8.61zm.736-4.185c.705 0 1.185.088 1.44.262.27.18.39.495.39.93 0 .405-.135.69-.42.855-.27.18-.765.254-1.44.254H8.31v-2.297h1.05zm8.656.706v-7.06h-2.46v7.06H18zM8.925 9.08c.71 0 1.185.08 1.432.24.245.16.367.435.367.83 0 .38-.13.646-.39.804-.265.154-.747.232-1.452.232h-.57V9.08h.615z"/></svg>
        </a>
    </li>
    <li>
        <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A//e-tec-memo.herokuapp.com/article/124/&t=[Django] カスタムユーザーを利用する">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h137.25V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.27c-30.81 0-40.42 19.12-40.42 38.73V256h68.78l-11 71.69h-57.78V480H400a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48z"/></svg>
        </a>
    </li>
    <li>
        <a href="https://timeline.line.me/social-plugin/share?url=https%3A//e-tec-memo.herokuapp.com/article/124/">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M272.1 204.2v71.1c0 1.8-1.4 3.2-3.2 3.2h-11.4c-1.1 0-2.1-.6-2.6-1.3l-32.6-44v42.2c0 1.8-1.4 3.2-3.2 3.2h-11.4c-1.8 0-3.2-1.4-3.2-3.2v-71.1c0-1.8 1.4-3.2 3.2-3.2H219c1 0 2.1.5 2.6 1.4l32.6 44v-42.2c0-1.8 1.4-3.2 3.2-3.2h11.4c1.8-.1 3.3 1.4 3.3 3.1zm-82-3.2h-11.4c-1.8 0-3.2 1.4-3.2 3.2v71.1c0 1.8 1.4 3.2 3.2 3.2h11.4c1.8 0 3.2-1.4 3.2-3.2v-71.1c0-1.7-1.4-3.2-3.2-3.2zm-27.5 59.6h-31.1v-56.4c0-1.8-1.4-3.2-3.2-3.2h-11.4c-1.8 0-3.2 1.4-3.2 3.2v71.1c0 .9.3 1.6.9 2.2.6.5 1.3.9 2.2.9h45.7c1.8 0 3.2-1.4 3.2-3.2v-11.4c0-1.7-1.4-3.2-3.1-3.2zM332.1 201h-45.7c-1.7 0-3.2 1.4-3.2 3.2v71.1c0 1.7 1.4 3.2 3.2 3.2h45.7c1.8 0 3.2-1.4 3.2-3.2v-11.4c0-1.8-1.4-3.2-3.2-3.2H301v-12h31.1c1.8 0 3.2-1.4 3.2-3.2V234c0-1.8-1.4-3.2-3.2-3.2H301v-12h31.1c1.8 0 3.2-1.4 3.2-3.2v-11.4c-.1-1.7-1.5-3.2-3.2-3.2zM448 113.7V399c-.1 44.8-36.8 81.1-81.7 81H81c-44.8-.1-81.1-36.9-81-81.7V113c.1-44.8 36.9-81.1 81.7-81H367c44.8.1 81.1 36.8 81 81.7zm-61.6 122.6c0-73-73.2-132.4-163.1-132.4-89.9 0-163.1 59.4-163.1 132.4 0 65.4 58 120.2 136.4 130.6 19.1 4.1 16.9 11.1 12.6 36.8-.7 4.1-3.3 16.1 14.1 8.8 17.4-7.3 93.9-55.3 128.2-94.7 23.6-26 34.9-52.3 34.9-81.5z"/></svg>
        </a>
    </li>
    
    <li>
        <a href="https://feedly.com/i/subscription/feed/https%3A%2F%2Fe-tec-memo.herokuapp.com/rss/latest/feed/">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"/></svg>
        </a>
    </li>
    
</ul>

<div class="bg-white mt-3 flex-center">
    
        <div class="w-50">
            <a class="p-3 page-link text-left h-100" href="/article/123/"><span>&laquo;</span>[Django] ユーザー登録とログインを同時に行う</a>
        </div>
    
    
        <div class="w-50">
            <a class="p-3 page-link text-right h-100" href="/article/127/">UNIXプログラミング入門~ファイル編(1/2)~<span>&raquo;</span></a>
        </div>
    
</div>

<div class="bg-white">
    <div class="m-2">
        <span class="h5">関連するメモ</span>
    </div>
    <div class="media-list">
    
        <a class="media-card shadow"
           href="/article/18/">
            <img class="media-card-image filter-img"
                 src="/static/img/title-bg.a233068bd60b.png"
                 alt="bg"
                 style="width:5rem;min-height:5rem;object-fit:cover;">
            <span class="media-card-badge h5">Djangoのtemplateでifをすっきり書いてみる(yesnoフィルター)</span>
            <small class="media-card-body">
                <small>Djangoで開発を続けていくうちにだんだんとtemplateが複雑になり読みづらくなることが...</small>
            </small>
        </a>
        
        <a class="media-card shadow"
           href="/article/61/">
            <img class="media-card-image filter-img"
                 src="/static/img/title-bg.a233068bd60b.png"
                 alt="bg"
                 style="width:5rem;min-height:5rem;object-fit:cover;">
            <span class="media-card-badge h5">Djangoの404ページをカスタマイズする</span>
            <small class="media-card-body">
                <small>Djangoで存在しないURLにアクセスすると以下のような404ページが表示されます。
デバッ...</small>
            </small>
        </a>
        
        <a class="media-card shadow"
           href="/article/123/">
            <img class="media-card-image filter-img"
                 src="/static/img/title-bg.a233068bd60b.png"
                 alt="bg"
                 style="width:5rem;min-height:5rem;object-fit:cover;">
            <span class="media-card-badge h5">[Django] ユーザー登録とログインを同時に行う</span>
            <small class="media-card-body">
                <small>Djangoでのユーザー登録完了と同時にログイン状態にする方法をメモ  
自動的にログインしな...</small>
            </small>
        </a>
        
        <a class="media-card shadow"
           href="/article/71/">
            <img class="media-card-image filter-img"
                 src="/static/img/title-bg.a233068bd60b.png"
                 alt="bg"
                 style="width:5rem;min-height:5rem;object-fit:cover;">
            <span class="media-card-badge h5">[Django] データベース(モデル)の設定</span>
            <small class="media-card-body">
                <small>前回までにビューとURLディスパッチャの設定を行ったので今回はデータベース(モデル)の設定をし...</small>
            </small>
        </a>
        
        <a class="media-card shadow"
           href="/article/12/">
            <img class="media-card-image filter-img"
                 src="/static/img/title-bg.a233068bd60b.png"
                 alt="bg"
                 style="width:5rem;min-height:5rem;object-fit:cover;">
            <span class="media-card-badge h5">Djangoでjsonを送受信する</span>
            <small class="media-card-body">
                <small>Djangoでのjsonの送受信についてメモ、送信はいいけど受信は割と忘れそう。  
送信
f...</small>
            </small>
        </a>
        
        <a class="media-card shadow"
           href="/article/197/">
            <img class="media-card-image filter-img"
                 src="/static/img/title-bg.a233068bd60b.png"
                 alt="bg"
                 style="width:5rem;min-height:5rem;object-fit:cover;">
            <span class="media-card-badge h5">django-herokuがインストール出来ない</span>
            <small class="media-card-body">
                <small>pipでdjango-herokuをインストールしようとするとdjango-herokuが依存...</small>
            </small>
        </a>
        
    </div>
</div>




    </div>
    <div class="sidebar-container">
        

<div class="sidebar">

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-2164456517159304"
     data-ad-slot="8407881908"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


</div>

<ul class="sticky-index d-none d-md-block index-box">
    <li class="ind-1"><a href="#[Django] カスタムユーザーを利用する" id="index-[Django] カスタムユーザーを利用する">[Django] カスタムユーザーを利用する</a></li>
    
        <li class="ind-2"><a href="#カスタムユーザー" id="index-カスタムユーザー">カスタムユーザー</a></li>
    
        <li class="ind-2"><a href="#メールアドレスでログインするユーザー" id="index-メールアドレスでログインするユーザー">メールアドレスでログインするユーザー</a></li>
    
        <li class="ind-3"><a href="#AbstractUser" id="index-AbstractUser">AbstractUser</a></li>
    
        <li class="ind-3"><a href="#実装" id="index-実装">実装</a></li>
    
        <li class="ind-4"><a href="#モデル" id="index-モデル">モデル</a></li>
    
        <li class="ind-3"><a href="#AbstractBaseUser" id="index-AbstractBaseUser">AbstractBaseUser</a></li>
    
        <li class="ind-4"><a href="#マネージャー" id="index-マネージャー">マネージャー</a></li>
    
        <li class="ind-2"><a href="#ログイン時に利用するユーザーを変更する" id="index-ログイン時に利用するユーザーを変更する">ログイン時に利用するユーザーを変更する</a></li>
    
        <li class="ind-2"><a href="#まとめ" id="index-まとめ">まとめ</a></li>
    
</ul>

<div class="simple-list mb-3">
    <span class="simple-list-item title">最近のメモ</span>
    
    <a class="simple-list-item" href="/article/124/">[Django] カスタムユーザーを利用する</a>
    
    <a class="simple-list-item" href="/article/82/">Swiftにインクリメント(++)、デクリメント(--)を復活させる</a>
    
    <a class="simple-list-item" href="/article/305/">UbuntuにswiftenvでSwiftの環境を構築する</a>
    
    <a class="simple-list-item" href="/article/65/">PNGイメージのデータ構造を知ってみる(2)</a>
    
    <a class="simple-list-item" href="/article/192/">Android OSをMacでビルドしようと思ったらglob: fcntl: too many open filesって言われた話</a>
    
    <a class="simple-list-item" href="/article/186/">[Django] プロジェクトの作成にカスタムテンプレートを利用する</a>
    
    <a class="simple-list-item" href="/article/281/">herokuのアプリケーションを複製する</a>
    
    <a class="simple-list-item" href="/article/83/">[Django] Http Headerを取得、追加する方法</a>
    
    <a class="simple-list-item" href="/article/285/">[Django] FormViewについて詳しく見てみる</a>
    
    <a class="simple-list-item" href="/article/197/">django-herokuがインストール出来ない</a>
    
</div>
<div class="archive-box mb-3">
    <span class="font-weight-bold">アーカイブ</span>
    
    
    <input type="checkbox" id="id__2020" class="archive-month-switch">
    <div class="archive-year">
        <label for="id__2020" class="triangle"></label>
        <a href="/archive/2020/">2020年</a>
    </div>
    <div class="archive-month">
        
        <a class="pl-5" href="/archive/2020/3/">3月</a>
        
        <a class="pl-5" href="/archive/2020/2/">2月</a>
        
        <a class="pl-5" href="/archive/2020/1/">1月</a>
        
    </div>
    
    <input type="checkbox" id="id__2019" class="archive-month-switch">
    <div class="archive-year">
        <label for="id__2019" class="triangle"></label>
        <a href="/archive/2019/">2019年</a>
    </div>
    <div class="archive-month">
        
        <a class="pl-5" href="/archive/2019/12/">12月</a>
        
        <a class="pl-5" href="/archive/2019/11/">11月</a>
        
        <a class="pl-5" href="/archive/2019/10/">10月</a>
        
        <a class="pl-5" href="/archive/2019/9/">9月</a>
        
        <a class="pl-5" href="/archive/2019/8/">8月</a>
        
        <a class="pl-5" href="/archive/2019/7/">7月</a>
        
        <a class="pl-5" href="/archive/2019/6/">6月</a>
        
        <a class="pl-5" href="/archive/2019/5/">5月</a>
        
        <a class="pl-5" href="/archive/2019/4/">4月</a>
        
        <a class="pl-5" href="/archive/2019/3/">3月</a>
        
        <a class="pl-5" href="/archive/2019/2/">2月</a>
        
        <a class="pl-5" href="/archive/2019/1/">1月</a>
        
    </div>
    
    <input type="checkbox" id="id__2018" class="archive-month-switch">
    <div class="archive-year">
        <label for="id__2018" class="triangle"></label>
        <a href="/archive/2018/">2018年</a>
    </div>
    <div class="archive-month">
        
        <a class="pl-5" href="/archive/2018/12/">12月</a>
        
        <a class="pl-5" href="/archive/2018/11/">11月</a>
        
        <a class="pl-5" href="/archive/2018/10/">10月</a>
        
        <a class="pl-5" href="/archive/2018/9/">9月</a>
        
    </div>
    
</div>
<div class="tag-list">
    
    <a class="tag-list-item normal" href="/tag/django/">
        django
        <span class="float-right">(50)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/python/">
        python
        <span class="float-right">(36)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/swift/">
        swift
        <span class="float-right">(9)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/heroku/">
        heroku
        <span class="float-right">(9)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/html/">
        html
        <span class="float-right">(8)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/javascript/">
        javascript
        <span class="float-right">(8)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/c/c++/">
        c/c++
        <span class="float-right">(7)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/pip/">
        pip
        <span class="float-right">(6)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Mac/">
        Mac
        <span class="float-right">(5)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/unix/">
        unix
        <span class="float-right">(5)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/markdown/">
        markdown
        <span class="float-right">(4)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/bootstrap/">
        bootstrap
        <span class="float-right">(3)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/CocoaPods/">
        CocoaPods
        <span class="float-right">(3)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/pyenv/">
        pyenv
        <span class="float-right">(3)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/GitHub/">
        GitHub
        <span class="float-right">(3)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/%E3%83%87%E3%83%BC%E3%82%BF%E6%A7%8B%E9%80%A0/">
        データ構造
        <span class="float-right">(2)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Swift%20Package%20Manager/">
        Swift Package Manager
        <span class="float-right">(2)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/gitlab/">
        gitlab
        <span class="float-right">(2)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/c++/">
        c++
        <span class="float-right">(2)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/SwiftUI/">
        SwiftUI
        <span class="float-right">(2)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/kotlin/">
        kotlin
        <span class="float-right">(2)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/ssh/">
        ssh
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/OCaml/">
        OCaml
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Travis%20CI/">
        Travis CI
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92/">
        機械学習
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Raspberry%20Pi/">
        Raspberry Pi
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/OpenCV/">
        OpenCV
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/CSS/">
        CSS
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/%E3%81%9D%E3%81%AE%E4%BB%96/">
        その他
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Android/">
        Android
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Carthage/">
        Carthage
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/homebrew/">
        homebrew
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/pypi/">
        pypi
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Django%20Rest%20Framework/">
        Django Rest Framework
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item normal" href="/tag/Ubuntu/">
        Ubuntu
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item series" href="/tag/Django%E3%81%A7%E3%83%96%E3%83%AD%E3%82%B0%E3%82%92%E4%BD%9C%E3%82%8D%E3%81%86/">
        Djangoでブログを作ろう
        <span class="float-right">(10)</span>
    </a>
    
    <a class="tag-list-item series" href="/tag/Django%E3%82%AF%E3%83%A9%E3%82%B9%E3%83%99%E3%83%BC%E3%82%B9%E3%83%93%E3%83%A5%E3%83%BC%E3%81%AE%E3%81%99%E3%83%BD%E3%82%81/">
        Djangoクラスベースビューのすヽめ
        <span class="float-right">(3)</span>
    </a>
    
    <a class="tag-list-item products" href="/tag/Django-Boost/">
        Django-Boost
        <span class="float-right">(3)</span>
    </a>
    
    <a class="tag-list-item products" href="/tag/SwiftyPyString/">
        SwiftyPyString
        <span class="float-right">(1)</span>
    </a>
    
    <a class="tag-list-item products" href="/tag/py_string/">
        py_string
        <span class="float-right">(1)</span>
    </a>
    
</div>



    </div>
</div>

</div>





<footer class="footer-container">
  <div class="footer">
    <section class="vertical-stack">
      <span class="text-light" style="font-size: 1.2rem;padding: .3rem;">エンジニアもどきの技術メモ</span>
      <small class="text-muted" style="padding: .3rem;">C++とPythonが大好きなエンジニアもどきの備忘録</small>
      <div>
        <a class="text-light svg-as-font" style="padding: .3rem;" href="https://twitter.com/iniad_0425">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z"/></svg>
        </a>
        <a class="text-light svg-as-font" style="padding: .3rem;" href="https://github.com/ChanTsune">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>
        </a>
      </div>
    </section>
    <section class="vertical-stack" style="padding: .3rem;">
      <a class="text-light svg-as-font" href="/rss/latest/feed/">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"/></svg> RSS
      </a>
      <a class="text-light" href="/sitemap/">サイトマップ</a>
      <a class="text-light" href="/privacypolicy/">プライバシーポリシー</a>
      <a class="text-light" href="/form/opinion/">お問い合わせ</a>
      <a class="text-light" href="/advertisement/">広告について</a>
    </section>
  </div>
  <div class="copyright text-center">
    <span>Copyright © 2018-2020 ChanTsune All Rights Reserved.</span>
  </div>
</footer>



</body>




<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
    (adsbygoogle = window.adsbygoogle || []).push({
        google_ad_client: "ca-pub-2164456517159304",
        enable_page_level_ads: true
    });
</script>




<script async src="https://www.googletagmanager.com/gtag/js?id=UA-157456952-1"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {
        dataLayer.push(arguments);
    }
    gtag('js', new Date());
    gtag('config', 'UA-157456952-1');
</script>






<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script>
    function selectorEscape(val) {
        return val.replace(/[ !"$%&'()*+,.\/:;<=>?@\[\\\]^`{|}~]/g, '\\$&');
    }
    $(function () {
            $('a[id^="index"]').click(function () {
                var time = 300;
                var href = $(this).attr("href");
                var target = $(href == "#" || href == "" ? 'html' : selectorEscape(href));
                var position = target.offset().top-60;
                $("html,body").animate({ scrollTop: position }, time, "swing");
                return false;
            });
        });
    var index_ids = [document.getElementById("[Django] カスタムユーザーを利用する")];
    var list = [document.getElementById("index-[Django] カスタムユーザーを利用する")];
    
    index_ids.push(document.getElementById("カスタムユーザー"));
    list.push(document.getElementById("index-カスタムユーザー"));
    
    index_ids.push(document.getElementById("メールアドレスでログインするユーザー"));
    list.push(document.getElementById("index-メールアドレスでログインするユーザー"));
    
    index_ids.push(document.getElementById("AbstractUser"));
    list.push(document.getElementById("index-AbstractUser"));
    
    index_ids.push(document.getElementById("実装"));
    list.push(document.getElementById("index-実装"));
    
    index_ids.push(document.getElementById("モデル"));
    list.push(document.getElementById("index-モデル"));
    
    index_ids.push(document.getElementById("AbstractBaseUser"));
    list.push(document.getElementById("index-AbstractBaseUser"));
    
    index_ids.push(document.getElementById("マネージャー"));
    list.push(document.getElementById("index-マネージャー"));
    
    index_ids.push(document.getElementById("ログイン時に利用するユーザーを変更する"));
    list.push(document.getElementById("index-ログイン時に利用するユーザーを変更する"));
    
    index_ids.push(document.getElementById("まとめ"));
    list.push(document.getElementById("index-まとめ"));
    
    $(window).on('load scroll', function () {
        add_class_in_scrolling();
    });
    function add_class_in_scrolling() {
        let flag = true;
        for (let index = list.length - 1; index != -1; --index) {
            let target = list[index];
            if (flag && index_ids[index].getBoundingClientRect().top < 70)
            {
                target.className = "active";
                flag = false;
            }
            else
            {
                target.className = "";
            }
        }
    }
</script>





</html>
"""

class TestHTMLSpaceLessCompressor(TestCase):

    def test_compress(self):
        from django_boost.utils.html import HTMLSpaceLessCompressor
        complesser = HTMLSpaceLessCompressor()
        print(complesser.compress(HTML_TEXT))
